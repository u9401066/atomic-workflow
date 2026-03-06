import { spawn } from 'child_process';
import type { GraphPayload, ValidationIssue } from '../messages';

interface McpResult<T> {
  content: Array<{ type: string; text: string }>;
}

/**
 * Lightweight MCP client that calls the Python server via CLI.
 * For MVP we shell out to `atomic-workflow-cli` instead of maintaining
 * a persistent stdio connection, keeping the extension simple.
 */
export class McpClient {
  constructor(
    private readonly workflowsDir: string,
    private readonly pythonPath: string = 'uv',
  ) {}

  async listDomains(): Promise<string[]> {
    return this.call<string[]>('list-domains');
  }

  async listVariants(domain: string): Promise<string[]> {
    return this.call<string[]>('list-variants', { domain });
  }

  async listSteps(domain: string, phase?: string, variant = 'elective'): Promise<unknown[]> {
    return this.call<unknown[]>('list-steps', { domain, phase, variant });
  }

  async getPhaseGraph(domain: string, phase: string, variant = 'elective'): Promise<GraphPayload> {
    return this.call<GraphPayload>('get-phase-graph', { domain, phase, variant });
  }

  async validateWorkflow(domain: string): Promise<{ errors: ValidationIssue[]; warnings: ValidationIssue[] }> {
    return this.call('validate-workflow', { domain });
  }

  private call<T>(command: string, args: Record<string, string | undefined> = {}): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      const cliArgs = ['run', 'python', '-m', 'atomic_workflow.cli', command, '--workflows-dir', this.workflowsDir];
      for (const [key, value] of Object.entries(args)) {
        if (value !== undefined) {
          cliArgs.push(`--${key}`, value);
        }
      }

      const proc = spawn(this.pythonPath, cliArgs, {
        stdio: ['ignore', 'pipe', 'pipe'],
        shell: false,
      });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data: Buffer) => { stdout += data.toString(); });
      proc.stderr.on('data', (data: Buffer) => { stderr += data.toString(); });

      proc.on('close', (code: number | null) => {
        if (code !== 0) {
          reject(new Error(`CLI exited with code ${code}: ${stderr}`));
          return;
        }
        try {
          resolve(JSON.parse(stdout) as T);
        } catch {
          reject(new Error(`Invalid JSON from CLI: ${stdout.slice(0, 200)}`));
        }
      });

      proc.on('error', (err: Error) => {
        reject(new Error(`Failed to spawn CLI: ${err.message}`));
      });
    });
  }
}
