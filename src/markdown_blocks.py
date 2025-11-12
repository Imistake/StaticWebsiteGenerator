from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    stripped = []
    for block in new_blocks:
        clean = block.strip()
        if clean != "":
            stripped.append(clean)
    return stripped

def block_to_block_type(markdown):
    i = 0
    while i < len(markdown) and markdown[i] == "#":
        i += 1
    if 1 <= i <= 6 and i < len(markdown) and markdown[i] == " " and i+1 < len(markdown) and markdown[i+1] != " ":
        return BlockType.HEADING
    
    lines = markdown.split("\n")

    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        s = line.strip()
        if len(s) == 0 or not s.startswith("> "):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered = True
    for line in lines:
        s = line.strip()
        if len(s) == 0 or not s.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    expected = 1
    matched_any = False
    for line in lines:
        s = line.strip()
        if len(s) == 0 or not s.startswith(f"{expected}. "):
            is_ordered = False
            break
        elif s.startswith(f"{expected}. "):
            expected += 1
            matched_any = True
        else:
            is_ordered = False
            break
    if is_ordered and matched_any:  
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

