from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        return ValueError("Not a valid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # If it's not a TextNode (no text_type attribute) -> keep unchanged
        if not hasattr(node, "text_type"):
            new_nodes.append(node)
            continue

        # Only split nodes that are TextType.TEXT
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text  # expected attribute name in your TextNode
        # If delimiter not present, keep the original node object
        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        # Balanced delimiters => parts length is odd (e.g. [pre, inside, post])
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text!r}")

        # Create nodes for each part (including empty strings)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # even -> plain text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # odd -> formatted text
                new_nodes.append(TextNode(part, text_type))

    return new_nodes