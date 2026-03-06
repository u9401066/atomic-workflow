import * as vscode from 'vscode';
import { McpClient } from '../mcp/mcpClient';

type TreeItemKind = 'domain' | 'phase' | 'step';

interface TreeNode {
  kind: TreeItemKind;
  label: string;
  domain?: string;
  phase?: string;
  stepId?: string;
  variant?: string;
  children?: TreeNode[];
}

export class PhaseTreeProvider implements vscode.TreeDataProvider<TreeNode> {
  private _onDidChangeTreeData = new vscode.EventEmitter<TreeNode | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  private _variant = 'elective';

  constructor(private readonly client: McpClient) {}

  get variant(): string {
    return this._variant;
  }

  set variant(value: string) {
    this._variant = value;
    this.refresh();
  }

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: TreeNode): vscode.TreeItem {
    const item = new vscode.TreeItem(
      element.label,
      element.kind === 'step'
        ? vscode.TreeItemCollapsibleState.None
        : vscode.TreeItemCollapsibleState.Collapsed,
    );

    item.contextValue = element.kind;

    if (element.kind === 'domain') {
      item.iconPath = new vscode.ThemeIcon('folder');
    } else if (element.kind === 'phase') {
      item.iconPath = new vscode.ThemeIcon('symbol-class');
      item.description = `Phase ${element.phase}`;
    } else if (element.kind === 'step') {
      item.iconPath = new vscode.ThemeIcon('symbol-method');
      item.description = element.stepId;
      item.tooltip = `${element.stepId}: ${element.label}`;
      item.command = {
        command: 'atomicWorkflow.goToStep',
        title: 'Go to Step',
        arguments: [element],
      };
    }

    return item;
  }

  async getChildren(element?: TreeNode): Promise<TreeNode[]> {
    if (!element) {
      return this.getDomains();
    }
    if (element.kind === 'domain') {
      return this.getPhases(element.domain!);
    }
    if (element.kind === 'phase') {
      return this.getSteps(element.domain!, element.phase!);
    }
    return [];
  }

  private async getDomains(): Promise<TreeNode[]> {
    try {
      const domains = await this.client.listDomains();
      return domains.map((d) => ({ kind: 'domain' as const, label: d, domain: d }));
    } catch {
      return [];
    }
  }

  private async getPhases(domain: string): Promise<TreeNode[]> {
    try {
      const steps = await this.client.listSteps(domain, undefined, this._variant) as Array<{ phase: string }>;
      const phases = [...new Set(steps.map((s) => s.phase))].sort();
      return phases.map((p) => ({
        kind: 'phase' as const,
        label: `Phase ${p}`,
        domain,
        phase: p,
      }));
    } catch {
      return [];
    }
  }

  private async getSteps(domain: string, phase: string): Promise<TreeNode[]> {
    try {
      const steps = await this.client.listSteps(domain, phase, this._variant) as Array<{
        step_id?: string;
        baseline_step_id?: string;
        variant_step_id?: string;
        title: string;
      }>;
      return steps.map((s) => {
        const stepId = s.step_id ?? s.baseline_step_id ?? s.variant_step_id ?? '?';
        return {
          kind: 'step' as const,
          label: s.title,
          domain,
          phase,
          stepId,
          variant: this._variant,
        };
      });
    } catch {
      return [];
    }
  }
}
