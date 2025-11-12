

def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    stripped = []
    for block in new_blocks:
        clean = block.strip()
        if clean != "":
            stripped.append(clean)
    return stripped