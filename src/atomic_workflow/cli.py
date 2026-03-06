from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from atomic_workflow.serialization import to_jsonable
from atomic_workflow.services import WorkflowService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atomic-workflow-cli")
    parser.add_argument("command", choices=["list-domains", "list-variants", "list-steps", "query-step", "get-phase-graph", "validate-workflow"])
    parser.add_argument("--domain")
    parser.add_argument("--phase")
    parser.add_argument("--variant", default="elective")
    parser.add_argument("--step-id")
    parser.add_argument("--format", default="reactflow")
    parser.add_argument("--workflows-dir", default=os.environ.get("VAULT_PATH", "workflows"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    service = WorkflowService.from_root(Path(args.workflows_dir))

    if args.command == "list-domains":
        payload = service.list_domains()
    elif args.command == "list-variants":
        payload = service.list_variants(_required(args.domain, "--domain"))
    elif args.command == "list-steps":
        payload = service.list_steps(_required(args.domain, "--domain"), phase=args.phase, variant=args.variant)
    elif args.command == "query-step":
        payload = service.get_resolved_step(_required(args.domain, "--domain"), _required(args.step_id, "--step-id"), variant=args.variant)
    elif args.command == "get-phase-graph":
        payload = service.get_phase_graph(_required(args.domain, "--domain"), _required(args.phase, "--phase"), variant=args.variant, format=args.format)
    else:
        payload = service.validate_domain(_required(args.domain, "--domain"))

    print(json.dumps(to_jsonable(payload), ensure_ascii=False))
    return 0


def _required(value: str | None, flag: str) -> str:
    if value is None:
        raise SystemExit(f"Missing required argument: {flag}")
    return value


if __name__ == "__main__":
    raise SystemExit(main())