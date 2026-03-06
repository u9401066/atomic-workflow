import * as vscode from 'vscode';
import { McpClient } from './mcp/mcpClient';
import { PhaseTreeProvider } from './treeView/phaseTreeProvider';
import { WorkflowEditorPanel } from './editorPanel';

export function activate(context: vscode.ExtensionContext): void {
  const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!workspaceRoot) {
    return;
  }

  const workflowsDir = vscode.Uri.joinPath(
    vscode.Uri.file(workspaceRoot),
    'workflows',
  ).fsPath;

  const client = new McpClient(workflowsDir);
  const treeProvider = new PhaseTreeProvider(client);

  // Tree View
  const treeView = vscode.window.createTreeView('atomicWorkflow.phaseTree', {
    treeDataProvider: treeProvider,
    showCollapseAll: true,
  });
  context.subscriptions.push(treeView);

  // Commands
  context.subscriptions.push(
    vscode.commands.registerCommand('atomicWorkflow.refreshTree', () => {
      treeProvider.refresh();
    }),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      'atomicWorkflow.openEditor',
      async (domain?: string, phase?: string) => {
        domain = domain ?? await pickDomain(client);
        if (!domain) { return; }
        phase = phase ?? await pickPhase(client, domain);
        if (!phase) { return; }

        const panel = WorkflowEditorPanel.createOrShow(
          context.extensionUri,
          client,
          domain,
          phase,
          treeProvider.variant,
        );
        await panel.loadGraph();
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      'atomicWorkflow.openPhaseGraph',
      async (node?: { domain?: string; phase?: string }) => {
        const domain = node?.domain ?? await pickDomain(client);
        if (!domain) { return; }
        const phase = node?.phase ?? await pickPhase(client, domain);
        if (!phase) { return; }

        const panel = WorkflowEditorPanel.createOrShow(
          context.extensionUri,
          client,
          domain,
          phase,
          treeProvider.variant,
        );
        await panel.loadGraph();
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      'atomicWorkflow.validateDomain',
      async (domain?: string) => {
        domain = domain ?? await pickDomain(client);
        if (!domain) { return; }

        try {
          const report = await client.validateWorkflow(domain);
          if (report.errors.length === 0 && report.warnings.length === 0) {
            void vscode.window.showInformationMessage(`✅ Domain "${domain}" is valid.`);
          } else {
            void vscode.window.showWarningMessage(
              `⚠ Domain "${domain}": ${report.errors.length} errors, ${report.warnings.length} warnings`,
            );
          }
        } catch (err) {
          void vscode.window.showErrorMessage(
            `Validation failed: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      },
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('atomicWorkflow.goToStep', (node?: { stepId?: string }) => {
      if (!node?.stepId) { return; }
      // Search workspace for step heading
      void vscode.commands.executeCommand('workbench.action.findInFiles', {
        query: `### \\[${node.stepId}\\]`,
        isRegex: true,
        filesToInclude: '**/workflows/**/*.md',
        triggerSearch: true,
      });
    }),
  );

  // File watcher for auto-refresh
  const watcher = vscode.workspace.createFileSystemWatcher('**/workflows/**/*.md');
  watcher.onDidChange(() => treeProvider.refresh());
  watcher.onDidCreate(() => treeProvider.refresh());
  watcher.onDidDelete(() => treeProvider.refresh());
  context.subscriptions.push(watcher);
}

export function deactivate(): void {
  // no-op
}

async function pickDomain(client: McpClient): Promise<string | undefined> {
  try {
    const domains = await client.listDomains();
    if (domains.length === 1) { return domains[0]; }
    return vscode.window.showQuickPick(domains, { placeHolder: 'Select domain' });
  } catch {
    void vscode.window.showErrorMessage('Failed to list domains. Is the Python engine available?');
    return undefined;
  }
}

async function pickPhase(client: McpClient, domain: string): Promise<string | undefined> {
  try {
    const steps = await client.listSteps(domain) as Array<{ phase: string }>;
    const phases = [...new Set(steps.map((s) => s.phase))].sort();
    return vscode.window.showQuickPick(phases, { placeHolder: 'Select phase' });
  } catch {
    void vscode.window.showErrorMessage('Failed to list phases.');
    return undefined;
  }
}
