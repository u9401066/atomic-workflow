import * as vscode from 'vscode';
import type { ExtToWebview, GraphPayload, WebviewToExt } from './messages';
import { McpClient } from './mcp/mcpClient';

export class WorkflowEditorPanel {
  public static readonly viewType = 'atomicWorkflow.editor';
  private static panels = new Map<string, WorkflowEditorPanel>();

  private constructor(
    private readonly panel: vscode.WebviewPanel,
    private readonly client: McpClient,
    private readonly extensionUri: vscode.Uri,
    private domain: string,
    private phase: string,
    private variant: string,
  ) {
    this.panel.onDidDispose(() => this.dispose());
    this.panel.webview.html = this.getHtmlForWebview();
    this.panel.webview.onDidReceiveMessage((msg: WebviewToExt) => this.onMessage(msg));
  }

  static createOrShow(
    extensionUri: vscode.Uri,
    client: McpClient,
    domain: string,
    phase: string,
    variant = 'elective',
  ): WorkflowEditorPanel {
    const key = `${domain}:${phase}:${variant}`;
    const existing = WorkflowEditorPanel.panels.get(key);
    if (existing) {
      existing.panel.reveal(vscode.ViewColumn.One);
      return existing;
    }

    const panel = vscode.window.createWebviewPanel(
      WorkflowEditorPanel.viewType,
      `Workflow: Phase ${phase} (${variant})`,
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'dist', 'webview')],
      },
    );

    const instance = new WorkflowEditorPanel(panel, client, extensionUri, domain, phase, variant);
    WorkflowEditorPanel.panels.set(key, instance);
    return instance;
  }

  async loadGraph(): Promise<void> {
    try {
      const graph = await this.client.getPhaseGraph(this.domain, this.phase, this.variant);
      this.postMessage({ type: 'graph:update', payload: graph });
    } catch (err) {
      void vscode.window.showErrorMessage(`Failed to load graph: ${err instanceof Error ? err.message : String(err)}`);
    }
  }

  private postMessage(message: ExtToWebview): void {
    void this.panel.webview.postMessage(message);
  }

  private async onMessage(msg: WebviewToExt): Promise<void> {
    switch (msg.type) {
      case 'ready':
        await this.loadGraph();
        break;
      case 'node:clicked':
        void vscode.commands.executeCommand('atomicWorkflow.goToStep', {
          domain: this.domain,
          stepId: msg.payload.stepId,
        });
        break;
      case 'variant:select':
        this.variant = msg.payload.variant;
        this.panel.title = `Workflow: Phase ${this.phase} (${this.variant})`;
        await this.loadGraph();
        break;
    }
  }

  private getHtmlForWebview(): string {
    const webview = this.panel.webview;
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this.extensionUri, 'dist', 'webview', 'index.js'),
    );
    const styleUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this.extensionUri, 'dist', 'webview', 'index.css'),
    );
    const nonce = getNonce();

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'none';
                 style-src ${webview.cspSource} 'unsafe-inline';
                 script-src 'nonce-${nonce}';
                 font-src ${webview.cspSource};">
  <link rel="stylesheet" href="${styleUri}">
  <title>Workflow Editor</title>
</head>
<body>
  <div id="root"></div>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
  }

  private dispose(): void {
    const key = `${this.domain}:${this.phase}:${this.variant}`;
    WorkflowEditorPanel.panels.delete(key);
    this.panel.dispose();
  }
}

function getNonce(): string {
  let text = '';
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return text;
}
