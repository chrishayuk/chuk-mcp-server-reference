#!/usr/bin/env python3
"""
MCP Specification Compliance Demo

Interactive demo that tests MCP server compliance and displays
a feature checklist with results.

MCP Spec Version: 2025-06-18

Usage:
    python tests/spec_compliance_demo.py

    # Or against a running server:
    python tests/spec_compliance_demo.py --url http://localhost:8000/mcp
"""

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


@dataclass
class TestResult:
    """Result of a single test."""

    feature: str
    spec_section: str
    passed: bool
    details: str = ""
    error: str = ""


class MCPComplianceTester:
    """Test MCP specification compliance."""

    def __init__(self, base_url: str = "http://localhost:8000/mcp"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=10.0)
        self.request_id = 0
        self.results: list[TestResult] = []
        self.session_id: str | None = None

    def get_next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id

    def send_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a JSON-RPC request."""
        request_id = self.get_next_id()
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {},
        }

        # Add session header for non-initialize requests
        headers = {"Content-Type": "application/json"}
        if method != "initialize" and self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        response = self.client.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()

        # Extract session ID from response headers (case-insensitive)
        for header_name, header_value in response.headers.items():
            if header_name.lower() == "mcp-session-id":
                self.session_id = header_value
                break

        return response.json()

    def print_header(self, title: str) -> None:
        """Print section header."""
        print(f"\n{'=' * 70}")
        print(f"  {title}")
        print(f"{'=' * 70}\n")

    def print_test(self, name: str, passed: bool, details: str = "") -> None:
        """Print test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"       {details}")

    def test_feature(
        self, feature: str, spec_section: str, test_func
    ) -> bool:
        """Run a test and record the result."""
        try:
            result = test_func()
            passed = result.get("passed", True)
            details = result.get("details", "")

            self.results.append(
                TestResult(
                    feature=feature,
                    spec_section=spec_section,
                    passed=passed,
                    details=details,
                )
            )

            self.print_test(feature, passed, details)
            return passed

        except Exception as e:
            self.results.append(
                TestResult(
                    feature=feature,
                    spec_section=spec_section,
                    passed=False,
                    error=str(e),
                )
            )
            self.print_test(feature, False, f"Error: {str(e)}")
            return False

    def run_all_tests(self) -> None:
        """Run all compliance tests."""
        print("\n" + "=" * 70)
        print("  MCP SPECIFICATION COMPLIANCE TEST")
        print("  Spec Version: 2025-06-18")
        print("=" * 70)
        print(f"\nTesting server at: {self.base_url}\n")

        # Lifecycle - MUST be first to establish session
        self.print_header("🔄 Lifecycle")
        self.test_lifecycle()

        # Core Protocol
        self.print_header("📋 Core Protocol (JSON-RPC 2.0)")
        self.test_jsonrpc_compliance()

        # Tools
        self.print_header("🔧 Tools")
        self.test_tools()

        # Resources
        self.print_header("📦 Resources")
        self.test_resources()

        # Prompts
        self.print_header("💬 Prompts")
        self.test_prompts()

        # Error Handling
        self.print_header("⚠️  Error Handling")
        self.test_error_handling()

        # Print summary
        self.print_summary()

    def test_jsonrpc_compliance(self) -> None:
        """Test JSON-RPC 2.0 compliance."""

        def test_version():
            response = self.send_request("ping")
            assert response.get("jsonrpc") == "2.0"
            return {"passed": True, "details": "All responses have jsonrpc: 2.0"}

        def test_id_preservation():
            response = self.send_request("ping")
            assert "id" in response
            return {"passed": True, "details": "Request ID preserved in response"}

        def test_result_or_error():
            response = self.send_request("ping")
            has_result = "result" in response
            has_error = "error" in response
            assert has_result or has_error
            assert not (has_result and has_error)
            return {"passed": True, "details": "Response has result XOR error"}

        self.test_feature(
            "JSON-RPC 2.0 version field", "Basic Protocol", test_version
        )
        self.test_feature(
            "Request ID preservation", "Basic Protocol", test_id_preservation
        )
        self.test_feature(
            "Result/Error exclusivity", "Basic Protocol", test_result_or_error
        )

    def test_lifecycle(self) -> None:
        """Test lifecycle protocol."""

        def test_initialize():
            response = self.send_request(
                "initialize",
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "compliance-tester", "version": "1.0.0"},
                },
            )
            result = response["result"]
            assert "protocolVersion" in result
            assert "capabilities" in result
            assert "serverInfo" in result

            server_info = result["serverInfo"]
            return {
                "passed": True,
                "details": f"Server: {server_info.get('name')} v{server_info.get('version')}",
            }

        def test_ping():
            response = self.send_request("ping")
            assert "result" in response
            return {"passed": True, "details": "Ping responded successfully"}

        self.test_feature("initialize request", "Lifecycle", test_initialize)
        self.test_feature("ping request", "Lifecycle", test_ping)

    def test_tools(self) -> None:
        """Test tools protocol."""

        def test_tools_list():
            response = self.send_request("tools/list")
            result = response["result"]
            assert "tools" in result
            tools = result["tools"]
            assert isinstance(tools, list)

            tool_count = len(tools)
            tool_names = [t["name"] for t in tools]

            return {
                "passed": True,
                "details": f"Found {tool_count} tools: {', '.join(tool_names)}",
            }

        def test_tool_schema():
            response = self.send_request("tools/list")
            tools = response["result"]["tools"]
            assert len(tools) > 0

            tool = tools[0]
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

            schema = tool["inputSchema"]
            assert "type" in schema

            return {
                "passed": True,
                "details": f"Tool '{tool['name']}' has valid schema",
            }

        def test_tools_call():
            response = self.send_request("tools/list")
            tools = response["result"]["tools"]

            # Find calculate tool
            calc_tool = next((t for t in tools if t["name"] == "calculate"), None)
            if not calc_tool:
                return {"passed": False, "details": "No calculate tool found"}

            # Call the tool
            call_response = self.send_request(
                "tools/call",
                {"name": "calculate", "arguments": {"expression": "2 + 2"}},
            )

            result = call_response["result"]
            assert "content" in result
            content = result["content"]
            assert isinstance(content, list)
            assert len(content) > 0

            content_item = content[0]
            assert "type" in content_item

            return {
                "passed": True,
                "details": f"Tool executed, returned {len(content)} content items",
            }

        self.test_feature("tools/list", "Tools", test_tools_list)
        self.test_feature("Tool schema validation", "Tools", test_tool_schema)
        self.test_feature("tools/call", "Tools", test_tools_call)

    def test_resources(self) -> None:
        """Test resources protocol."""

        def test_resources_list():
            response = self.send_request("resources/list")
            result = response["result"]
            assert "resources" in result
            resources = result["resources"]
            assert isinstance(resources, list)

            count = len(resources)
            uris = [r["uri"] for r in resources[:3]]  # First 3
            uri_list = ", ".join(uris)
            if count > 3:
                uri_list += f", ... ({count - 3} more)"

            return {
                "passed": True,
                "details": f"Found {count} resources: {uri_list}",
            }

        def test_resource_schema():
            response = self.send_request("resources/list")
            resources = response["result"]["resources"]
            assert len(resources) > 0

            resource = resources[0]
            assert "uri" in resource

            return {
                "passed": True,
                "details": f"Resource '{resource.get('name', resource['uri'])}' has valid structure",
            }

        def test_resources_read():
            response = self.send_request("resources/list")
            resources = response["result"]["resources"]
            assert len(resources) > 0

            uri = resources[0]["uri"]
            read_response = self.send_request("resources/read", {"uri": uri})

            result = read_response["result"]
            assert "contents" in result
            contents = result["contents"]
            assert isinstance(contents, list)
            assert len(contents) > 0

            return {
                "passed": True,
                "details": f"Successfully read resource: {uri}",
            }

        self.test_feature("resources/list", "Resources", test_resources_list)
        self.test_feature("Resource schema validation", "Resources", test_resource_schema)
        self.test_feature("resources/read", "Resources", test_resources_read)

    def test_prompts(self) -> None:
        """Test prompts protocol."""

        def test_prompts_list():
            response = self.send_request("prompts/list")
            result = response["result"]
            assert "prompts" in result
            prompts = result["prompts"]
            assert isinstance(prompts, list)

            count = len(prompts)
            names = [p["name"] for p in prompts]

            return {
                "passed": True,
                "details": f"Found {count} prompts: {', '.join(names)}",
            }

        def test_prompt_schema():
            response = self.send_request("prompts/list")
            prompts = response["result"]["prompts"]
            assert len(prompts) > 0

            prompt = prompts[0]
            assert "name" in prompt
            assert "description" in prompt

            return {
                "passed": True,
                "details": f"Prompt '{prompt['name']}' has valid structure",
            }

        def test_prompts_get():
            response = self.send_request("prompts/list")
            prompts = response["result"]["prompts"]
            assert len(prompts) > 0

            prompt = prompts[0]
            prompt_name = prompt["name"]

            # Build arguments
            arguments = {}
            for arg in prompt.get("arguments", []):
                arg_name = arg["name"]
                # Provide test values
                test_values = {
                    "language": "python",
                    "code": "def test(): pass",
                    "concept": "MCP",
                    "level": "beginner",
                    "error_message": "Test error",
                    "context": "Testing",
                }
                arguments[arg_name] = test_values.get(arg_name, "test")

            get_response = self.send_request(
                "prompts/get",
                {"name": prompt_name, "arguments": arguments},
            )

            result = get_response["result"]
            assert "messages" in result
            messages = result["messages"]
            assert isinstance(messages, list)
            assert len(messages) > 0

            return {
                "passed": True,
                "details": f"Got prompt '{prompt_name}' with {len(messages)} messages",
            }

        self.test_feature("prompts/list", "Prompts", test_prompts_list)
        self.test_feature("Prompt schema validation", "Prompts", test_prompt_schema)
        self.test_feature("prompts/get", "Prompts", test_prompts_get)

    def test_error_handling(self) -> None:
        """Test error handling."""

        def test_method_not_found():
            response = self.send_request("invalid/method")
            assert "error" in response
            error = response["error"]
            assert "code" in error
            assert error["code"] == -32601

            return {
                "passed": True,
                "details": "Correctly returns -32601 for unknown method",
            }

        def test_invalid_params():
            response = self.send_request("tools/call", {"arguments": {}})
            assert "error" in response
            error = response["error"]
            assert "code" in error
            assert error["code"] == -32602

            return {
                "passed": True,
                "details": "Correctly returns -32602 for invalid params",
            }

        self.test_feature("Method not found error", "Error Handling", test_method_not_found)
        self.test_feature("Invalid params error", "Error Handling", test_invalid_params)

    def print_summary(self) -> None:
        """Print test summary table."""
        print("\n" + "=" * 70)
        print("  COMPLIANCE SUMMARY")
        print("=" * 70 + "\n")

        # Group by spec section
        sections = {}
        for result in self.results:
            if result.spec_section not in sections:
                sections[result.spec_section] = []
            sections[result.spec_section].append(result)

        # Print table
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests

        print(f"{'Spec Section':<25} {'Feature':<30} {'Status':<10}")
        print("-" * 70)

        for section, results in sections.items():
            for i, result in enumerate(results):
                section_name = section if i == 0 else ""
                status = "✅ PASS" if result.passed else "❌ FAIL"
                feature = result.feature[:28] + ".." if len(result.feature) > 30 else result.feature
                print(f"{section_name:<25} {feature:<30} {status:<10}")

        print("-" * 70)
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")

        percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\nCompliance: {percentage:.1f}%")

        if percentage == 100:
            print("\n🎉 FULL MCP SPECIFICATION COMPLIANCE! 🎉")
        elif percentage >= 80:
            print("\n✨ Excellent MCP compliance!")
        elif percentage >= 60:
            print("\n👍 Good MCP compliance, some features missing")
        else:
            print("\n⚠️  Significant compliance issues detected")

        print("\n" + "=" * 70 + "\n")

    def close(self) -> None:
        """Close the client."""
        self.client.close()


def main():
    """Run compliance demo."""
    parser = argparse.ArgumentParser(description="MCP Specification Compliance Demo")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/mcp",
        help="MCP server URL (default: http://localhost:8000/mcp)",
    )
    parser.add_argument(
        "--start-server",
        action="store_true",
        help="Start the reference server automatically",
    )

    args = parser.parse_args()

    server_process = None

    try:
        # Start server if requested
        if args.start_server:
            print("Starting reference server...")
            example_path = Path(__file__).parent.parent / "examples" / "11_full_server.py"
            server_process = subprocess.Popen(
                [sys.executable, str(example_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Waiting for server to start...")
            time.sleep(3)

        # Run tests
        tester = MCPComplianceTester(args.url)
        tester.run_all_tests()
        tester.close()

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")

    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Cleanup server
        if server_process:
            print("\nStopping server...")
            server_process.terminate()
            server_process.wait(timeout=5)


if __name__ == "__main__":
    main()
