#!/usr/bin/env python3
"""
MCP Protocol Compliance Tests

Tests actual MCP protocol compliance by sending JSON-RPC messages
and validating responses according to the MCP specification.

MCP Spec Version: 2025-06-18
Tests all protocol messages defined in the specification.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import httpx
import pytest


class MCPProtocolTester:
    """Test MCP protocol compliance via HTTP transport."""

    def __init__(self, base_url: str = "http://localhost:8000/mcp"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=10.0)
        self.request_id = 0

    def get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id

    def send_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Send a JSON-RPC request and return the response.

        MCP Spec: All requests must follow JSON-RPC 2.0 format
        """
        request_id = self.get_next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {},
        }

        response = self.client.post(self.base_url, json=payload)
        response.raise_for_status()

        data = response.json()

        # MCP Spec: Response must have jsonrpc and id fields
        assert data.get("jsonrpc") == "2.0", "Response must have jsonrpc: 2.0"
        assert data.get("id") == request_id, f"Response id must match request id ({request_id})"

        return data

    def send_notification(self, method: str, params: dict[str, Any] | None = None) -> None:
        """
        Send a JSON-RPC notification (no response expected).

        MCP Spec: Notifications have no id field
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }

        response = self.client.post(self.base_url, json=payload)
        response.raise_for_status()

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()


@pytest.fixture(scope="module")
def server_process():
    """Start the full MCP server for testing."""
    example_path = Path(__file__).parent.parent / "examples" / "11_full_server.py"

    # Start server in background
    process = subprocess.Popen(
        [sys.executable, str(example_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(3)

    yield process

    # Cleanup
    process.terminate()
    process.wait(timeout=5)


@pytest.fixture(scope="module")
def mcp_client(server_process):
    """Create MCP protocol tester client."""
    client = MCPProtocolTester()
    yield client
    client.close()


class TestLifecycle:
    """
    Test MCP Lifecycle Protocol

    MCP Spec Reference: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle
    """

    def test_initialize_request(self, mcp_client: MCPProtocolTester):
        """
        Test initialize request/response.

        MCP Spec: Client sends initialize with protocolVersion and capabilities
        Server responds with protocolVersion, capabilities, and serverInfo
        """
        response = mcp_client.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {},
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0",
                },
            },
        )

        # Check response structure
        assert "result" in response, "Initialize must return result"
        result = response["result"]

        # MCP Spec: Must include protocolVersion
        assert "protocolVersion" in result, "Response must include protocolVersion"

        # MCP Spec: Must include capabilities
        assert "capabilities" in result, "Response must include capabilities"
        capabilities = result["capabilities"]

        # MCP Spec: Must include serverInfo
        assert "serverInfo" in result, "Response must include serverInfo"
        server_info = result["serverInfo"]
        assert "name" in server_info, "serverInfo must include name"
        assert "version" in server_info, "serverInfo must include version"

        # Validate server advertises expected capabilities
        assert "tools" in capabilities or "resources" in capabilities or "prompts" in capabilities

    def test_initialized_notification(self, mcp_client: MCPProtocolTester):
        """
        Test initialized notification.

        MCP Spec: After initialize, client sends initialized notification
        This is a notification (no response expected)
        """
        # Should not raise an error
        mcp_client.send_notification("notifications/initialized")

    def test_ping_request(self, mcp_client: MCPProtocolTester):
        """
        Test ping request.

        MCP Spec: Ping can be sent by either client or server
        Response should be empty object
        """
        response = mcp_client.send_request("ping")

        assert "result" in response, "Ping must return result"
        result = response["result"]

        # MCP Spec: Ping response is empty object
        assert isinstance(result, dict), "Ping result must be object"


class TestTools:
    """
    Test MCP Tools Protocol

    MCP Spec Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
    """

    def test_tools_list(self, mcp_client: MCPProtocolTester):
        """
        Test tools/list request.

        MCP Spec: Returns list of available tools with schemas
        """
        response = mcp_client.send_request("tools/list")

        assert "result" in response, "tools/list must return result"
        result = response["result"]

        # MCP Spec: Must include tools array
        assert "tools" in result, "Result must include tools array"
        tools = result["tools"]
        assert isinstance(tools, list), "tools must be array"

        # Validate tool structure
        if len(tools) > 0:
            tool = tools[0]
            # MCP Spec: Each tool must have name, description, inputSchema
            assert "name" in tool, "Tool must have name"
            assert "description" in tool, "Tool must have description"
            assert "inputSchema" in tool, "Tool must have inputSchema"

            # MCP Spec: inputSchema must be valid JSON Schema
            schema = tool["inputSchema"]
            assert "type" in schema, "inputSchema must have type"

    def test_tools_call(self, mcp_client: MCPProtocolTester):
        """
        Test tools/call request.

        MCP Spec: Executes a tool with arguments, returns content array
        """
        # First get available tools
        list_response = mcp_client.send_request("tools/list")
        tools = list_response["result"]["tools"]

        assert len(tools) > 0, "Server must have at least one tool for this test"

        # Find the calculate tool
        calculate_tool = None
        for tool in tools:
            if tool["name"] == "calculate":
                calculate_tool = tool
                break

        assert calculate_tool is not None, "Server should have calculate tool"

        # Call the tool
        response = mcp_client.send_request(
            "tools/call",
            {
                "name": "calculate",
                "arguments": {"expression": "2 + 2"},
            },
        )

        assert "result" in response, "tools/call must return result"
        result = response["result"]

        # MCP Spec: Tool result must include content array
        assert "content" in result, "Tool result must include content"
        content = result["content"]
        assert isinstance(content, list), "content must be array"
        assert len(content) > 0, "content array must not be empty"

        # MCP Spec: Each content item must have type
        content_item = content[0]
        assert "type" in content_item, "Content item must have type"
        assert content_item["type"] in ["text", "image", "resource"], "Content type must be valid"

        # For text content, must have text field
        if content_item["type"] == "text":
            assert "text" in content_item, "Text content must have text field"
            # Verify calculation result
            assert "4" in content_item["text"], "Calculate 2+2 should return 4"

    def test_tools_call_invalid_tool(self, mcp_client: MCPProtocolTester):
        """
        Test tools/call with non-existent tool.

        MCP Spec: Should return error for unknown tool
        """
        response = mcp_client.send_request(
            "tools/call",
            {
                "name": "nonexistent_tool",
                "arguments": {},
            },
        )

        # MCP Spec: Error response must have error field
        assert "error" in response, "Invalid tool should return error"
        error = response["error"]
        assert "code" in error, "Error must have code"
        assert "message" in error, "Error must have message"


class TestResources:
    """
    Test MCP Resources Protocol

    MCP Spec Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
    """

    def test_resources_list(self, mcp_client: MCPProtocolTester):
        """
        Test resources/list request.

        MCP Spec: Returns list of available resources
        """
        response = mcp_client.send_request("resources/list")

        assert "result" in response, "resources/list must return result"
        result = response["result"]

        # MCP Spec: Must include resources array
        assert "resources" in result, "Result must include resources array"
        resources = result["resources"]
        assert isinstance(resources, list), "resources must be array"

        # Validate resource structure
        if len(resources) > 0:
            resource = resources[0]
            # MCP Spec: Each resource must have uri
            assert "uri" in resource, "Resource must have uri"
            # MCP Spec: Resources should have name and mimeType
            assert "name" in resource or "uri" in resource, "Resource must have name or uri"

    def test_resources_read(self, mcp_client: MCPProtocolTester):
        """
        Test resources/read request.

        MCP Spec: Reads resource content by URI
        """
        # First get available resources
        list_response = mcp_client.send_request("resources/list")
        resources = list_response["result"]["resources"]

        assert len(resources) > 0, "Server must have at least one resource for this test"

        # Read the first resource
        resource_uri = resources[0]["uri"]
        response = mcp_client.send_request(
            "resources/read",
            {"uri": resource_uri},
        )

        assert "result" in response, "resources/read must return result"
        result = response["result"]

        # MCP Spec: Resource contents must include contents array
        assert "contents" in result, "Result must include contents"
        contents = result["contents"]
        assert isinstance(contents, list), "contents must be array"
        assert len(contents) > 0, "contents must not be empty"

        # Validate content structure
        content = contents[0]
        assert "uri" in content, "Content must have uri"
        assert "mimeType" in content or "text" in content or "blob" in content

    def test_resources_read_json(self, mcp_client: MCPProtocolTester):
        """
        Test reading JSON resource.

        MCP Spec: JSON resources should be readable
        """
        response = mcp_client.send_request(
            "resources/read",
            {"uri": "config://server-info"},
        )

        result = response["result"]
        contents = result["contents"]
        content = contents[0]

        # Should have mimeType application/json
        if "mimeType" in content:
            assert "json" in content["mimeType"].lower()

        # Should have text that is valid JSON
        if "text" in content:
            # Should be valid JSON
            data = json.loads(content["text"])
            assert isinstance(data, dict)

    def test_resources_read_markdown(self, mcp_client: MCPProtocolTester):
        """
        Test reading Markdown resource.

        MCP Spec: Text resources should be readable
        """
        response = mcp_client.send_request(
            "resources/read",
            {"uri": "docs://readme"},
        )

        result = response["result"]
        contents = result["contents"]
        content = contents[0]

        # Should have text content
        assert "text" in content, "Markdown resource should have text"

        # Should have mimeType text/markdown
        if "mimeType" in content:
            assert "markdown" in content["mimeType"].lower()


class TestPrompts:
    """
    Test MCP Prompts Protocol

    MCP Spec Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
    """

    def test_prompts_list(self, mcp_client: MCPProtocolTester):
        """
        Test prompts/list request.

        MCP Spec: Returns list of available prompts
        """
        response = mcp_client.send_request("prompts/list")

        assert "result" in response, "prompts/list must return result"
        result = response["result"]

        # MCP Spec: Must include prompts array
        assert "prompts" in result, "Result must include prompts array"
        prompts = result["prompts"]
        assert isinstance(prompts, list), "prompts must be array"

        # Validate prompt structure
        if len(prompts) > 0:
            prompt = prompts[0]
            # MCP Spec: Each prompt must have name and description
            assert "name" in prompt, "Prompt must have name"
            assert "description" in prompt, "Prompt must have description"

    def test_prompts_get(self, mcp_client: MCPProtocolTester):
        """
        Test prompts/get request.

        MCP Spec: Gets prompt with arguments
        """
        # First get available prompts
        list_response = mcp_client.send_request("prompts/list")
        prompts = list_response["result"]["prompts"]

        assert len(prompts) > 0, "Server must have at least one prompt for this test"

        # Find a prompt with arguments
        prompt_name = prompts[0]["name"]
        prompt_args = prompts[0].get("arguments", [])

        # Build arguments dict
        arguments = {}
        for arg in prompt_args:
            arg_name = arg["name"]
            # Provide test values
            if arg_name == "language":
                arguments[arg_name] = "python"
            elif arg_name == "code":
                arguments[arg_name] = "def hello(): pass"
            elif arg_name == "concept":
                arguments[arg_name] = "MCP"
            elif arg_name == "level":
                arguments[arg_name] = "beginner"
            elif arg_name == "error_message":
                arguments[arg_name] = "Test error"
            else:
                arguments[arg_name] = "test value"

        # Get the prompt
        response = mcp_client.send_request(
            "prompts/get",
            {
                "name": prompt_name,
                "arguments": arguments,
            },
        )

        assert "result" in response, "prompts/get must return result"
        result = response["result"]

        # MCP Spec: Prompt result must include messages
        assert "messages" in result, "Prompt result must include messages"
        messages = result["messages"]
        assert isinstance(messages, list), "messages must be array"
        assert len(messages) > 0, "messages must not be empty"

        # Validate message structure
        message = messages[0]
        assert "role" in message, "Message must have role"
        assert "content" in message, "Message must have content"

        # Role must be valid
        assert message["role"] in ["user", "assistant", "system"]

        # Content must be valid
        content = message["content"]
        assert "type" in content, "Content must have type"


class TestErrorHandling:
    """
    Test MCP Error Handling

    MCP Spec Reference: https://modelcontextprotocol.io/specification/2025-06-18/basic/messages
    """

    def test_invalid_method(self, mcp_client: MCPProtocolTester):
        """
        Test error response for invalid method.

        MCP Spec: Method not found should return -32601 error
        """
        response = mcp_client.send_request("invalid/method")

        assert "error" in response, "Invalid method should return error"
        error = response["error"]

        # MCP Spec: Error must have code and message
        assert "code" in error, "Error must have code"
        assert "message" in error, "Error must have message"

        # Method not found is -32601
        assert error["code"] == -32601, "Method not found should be error -32601"

    def test_invalid_params(self, mcp_client: MCPProtocolTester):
        """
        Test error response for invalid params.

        MCP Spec: Invalid params should return -32602 error
        """
        response = mcp_client.send_request(
            "tools/call",
            {
                # Missing required 'name' parameter
                "arguments": {},
            },
        )

        assert "error" in response, "Invalid params should return error"
        error = response["error"]

        assert "code" in error, "Error must have code"
        assert "message" in error, "Error must have message"

        # Invalid params is -32602
        assert error["code"] == -32602, "Invalid params should be error -32602"


class TestJSONRPC:
    """
    Test JSON-RPC 2.0 Compliance

    MCP Spec: MCP uses JSON-RPC 2.0 as base protocol
    Reference: https://www.jsonrpc.org/specification
    """

    def test_jsonrpc_version(self, mcp_client: MCPProtocolTester):
        """All responses must have jsonrpc: 2.0."""
        response = mcp_client.send_request("ping")
        assert response.get("jsonrpc") == "2.0"

    def test_request_id_preserved(self, mcp_client: MCPProtocolTester):
        """Response id must match request id."""
        request_id = 12345
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "ping",
            "params": {},
        }

        response = mcp_client.client.post(mcp_client.base_url, json=payload)
        data = response.json()

        assert data.get("id") == request_id

    def test_notification_no_response(self, mcp_client: MCPProtocolTester):
        """Notifications should not return a response."""
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
            # Note: No id field = notification
        }

        response = mcp_client.client.post(mcp_client.base_url, json=payload)
        # Should succeed but not return JSON-RPC response
        assert response.status_code == 200


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
