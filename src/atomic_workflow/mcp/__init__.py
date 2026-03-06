from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from atomic_workflow.serialization import to_jsonable
from atomic_workflow.services import WorkflowService


def create_server(workflows_path: Path | None = None) -> FastMCP:
    service = WorkflowService.from_root(
        workflows_path or Path(os.environ.get("VAULT_PATH", "workflows")).resolve()
    )
    server = FastMCP(
        name="atomic-workflow",
        instructions="Read-only MCP server for Atomic Workflow baseline and variant workflow exploration.",
    )

    @server.tool(description="List all workflow domains available in the workspace")
    def list_domains() -> list[str]:
        return service.list_domains()

    @server.tool(description="List available variants for a workflow domain")
    def list_variants(domain: str) -> list[str]:
        return service.list_variants(domain)

    @server.tool(description="List resolved workflow steps for a domain/phase/variant")
    def list_steps(domain: str, phase: str | None = None, variant: str = "elective") -> list[dict[str, object]]:
        return to_jsonable(service.list_steps(domain, phase=phase, variant=variant))

    @server.tool(description="Query a single resolved workflow step by ID")
    def query_step(domain: str, step_id: str, variant: str = "elective") -> dict[str, object]:
        return to_jsonable(service.get_resolved_step(domain, step_id, variant=variant))

    @server.tool(description="Validate a workflow domain and return structured issues")
    def validate_workflow(domain: str) -> dict[str, object]:
        return to_jsonable(service.validate_domain(domain))

    @server.tool(description="Return a phase graph in reactflow or raw graph format")
    def get_phase_graph(domain: str, phase: str, variant: str = "elective", format: str = "reactflow") -> dict[str, object]:
        return to_jsonable(service.get_phase_graph(domain, phase, variant=variant, format=format))

    return server


def main() -> int:
    server = create_server()
    server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())