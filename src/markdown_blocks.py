from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4: -3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)