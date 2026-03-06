from __future__ import annotations

from dataclasses import asdict

from atomic_workflow.domain.models import ResolvedStep, WorkflowGraphEdge, WorkflowGraphNode


class WorkflowGraphGenerator:
    def generate(
        self,
        steps: list[ResolvedStep],
        *,
        phase: str,
        variant: str,
        format: str = "reactflow",
    ) -> dict[str, object]:
        nodes = [self._to_graph_node(step) for step in steps]
        node_ids = {node.node_id for node in nodes}
        edges = self._build_edges(steps, node_ids)

        if format == "reactflow":
            return {
                "nodes": [self._to_reactflow_node(node, index) for index, node in enumerate(nodes)],
                "edges": [self._to_reactflow_edge(edge, index) for index, edge in enumerate(edges)],
                "meta": {"phase": phase, "variant": variant, "nodeCount": len(nodes), "edgeCount": len(edges)},
            }

        return {
            "nodes": [asdict(node) for node in nodes],
            "edges": [asdict(edge) for edge in edges],
            "meta": {"phase": phase, "variant": variant, "nodeCount": len(nodes), "edgeCount": len(edges)},
        }

    def _to_graph_node(self, step: ResolvedStep) -> WorkflowGraphNode:
        return WorkflowGraphNode(
            node_id=step.step_id,
            label=step.title,
            phase=step.phase,
            variant=step.variant,
            kind=step.origin,
            node_type=step.node_type,
            refs=step.refs,
        )

    def _build_edges(
        self,
        steps: list[ResolvedStep],
        node_ids: set[str],
    ) -> list[WorkflowGraphEdge]:
        edges: list[WorkflowGraphEdge] = []

        for index in range(len(steps) - 1):
            edges.append(
                WorkflowGraphEdge(
                    source=steps[index].step_id,
                    target=steps[index + 1].step_id,
                    edge_type="sequential",
                )
            )

        for step in steps:
            for ref in step.refs:
                if ref.target in node_ids:
                    edges.append(
                        WorkflowGraphEdge(
                            source=step.step_id,
                            target=ref.target,
                            edge_type=ref.type,
                            condition=ref.condition,
                            description=ref.description,
                        )
                    )

        return edges

    def _to_reactflow_node(self, node: WorkflowGraphNode, index: int) -> dict[str, object]:
        return {
            "id": node.node_id,
            "type": self._reactflow_node_type(node.node_type),
            "position": {"x": 120, "y": 80 + (index * 120)},
            "data": {
                "label": node.label,
                "stepId": node.node_id,
                "phase": node.phase,
                "variant": node.variant,
                "kind": node.kind,
                "nodeType": node.node_type,
                "refs": [asdict(ref) for ref in node.refs],
            },
        }

    def _to_reactflow_edge(self, edge: WorkflowGraphEdge, index: int) -> dict[str, object]:
        return {
            "id": f"edge-{index}-{edge.source}-{edge.target}",
            "source": edge.source,
            "target": edge.target,
            "type": edge.edge_type,
            "label": edge.condition,
            "animated": edge.edge_type != "sequential",
            "data": {"description": edge.description},
        }

    def _reactflow_node_type(self, node_type: str) -> str:
        mapping = {
            "task": "step",
            "decision": "decision",
            "parallel_start": "parallel",
            "parallel_end": "parallel",
            "subprocess": "subprocess",
            "event": "event",
            "milestone": "milestone",
        }
        return mapping.get(node_type, "step")