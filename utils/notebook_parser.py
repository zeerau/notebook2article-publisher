import nbformat


def extract_notebook_code_and_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    code_cells = []
    markdown_cells = []
    ordered_cells = []

    for cell in nb.cells:
        if cell.cell_type == "code":
            code_cells.append(cell.source)
            ordered_cells.append({"type": "code", "content": cell.source})
        elif cell.cell_type == "markdown":
            markdown_cells.append(cell.source)
            ordered_cells.append({"type": "markdown", "content": cell.source})

    # Default return for backward compatibility
    return code_cells, markdown_cells, ordered_cells
