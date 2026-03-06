/** Typed wrapper for the VS Code webview API (acquireVsCodeApi). */

interface VsCodeApi {
  postMessage(message: unknown): void;
  getState(): unknown;
  setState(state: unknown): void;
}

// VS Code injects this global
declare function acquireVsCodeApi(): VsCodeApi;

let api: VsCodeApi | undefined;

export function getVsCodeApi(): VsCodeApi | undefined {
  if (api) { return api; }
  if (typeof acquireVsCodeApi === 'function') {
    api = acquireVsCodeApi();
    return api;
  }
  return undefined;
}

export function postMessage(message: unknown): void {
  getVsCodeApi()?.postMessage(message);
}
