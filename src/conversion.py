from textnode import TextNode, TextType
from htmlnode import LeafNode
from extract import extract_markdown_images, extract_markdown_links
import re

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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            # text before the image
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            last_index = end

        # any remaining text
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            start, end = match.span()
            anchor_text, url = match.groups()

            # text before the link
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            last_index = end

        # any remaining text
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    