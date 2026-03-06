# Atomic Workflow — VS Code Extension

Clinical workflow decomposition, variant overlay, and interactive visual redesign editor.

## Features

- **Phase Tree View**: Browse workflow phases and steps in the Activity Bar
- **Interactive Graph Editor**: Visualize workflow graphs with React Flow
- **Variant Overlay**: Compare baseline vs. variant workflows
- **Validation**: Structural validation of workflow files

## Requirements

- Python ≥ 3.12 with `atomic-workflow` package installed
- Workflow markdown files in `workflows/` directory

## Usage

1. Open a workspace containing `workflows/**/phase-*.md` files
2. The "Atomic Workflow" icon appears in the Activity Bar
3. Browse phases and steps in the tree view
4. Right-click a phase → "Open Phase Graph" for visual editor
