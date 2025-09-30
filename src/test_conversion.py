import unittest

from conversion import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType

class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    
class SplitNodeDelimiter(unittest.TestCase):
    
    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_single_split_code(self):
        node = TextNode("This is `inline` code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "inline")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " code")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_bold_split(self):
        node = TextNode("Some **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_multiple_splits(self):
        node = TextNode("Mix of `code` and `more code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[3].text, "more code")
        self.assertEqual(result[3].text_type, TextType.CODE)

    def test_non_text_nodes_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Unmatched `delimiter here", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            

class TestLinkSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
class TestTextToTextNodes(unittest.TestCase):
    def test_basic_markdown(self):
        text = "This is **bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)

        # filter out any empty text nodes
        nodes = [n for n in nodes if not (n.text_type == TextType.TEXT and n.text == "")]

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(len(nodes), len(expected))
        for n, e in zip(nodes, expected):
            self.assertEqual(n.text, e.text)
            self.assertEqual(n.text_type, e.text_type)


    def test_links_and_images(self):
        text = "![alt text](https://img.com/x.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("alt text", TextType.IMAGE, "https://img.com/x.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(len(nodes), len(expected))
        for n, e in zip(nodes, expected):
            self.assertEqual(n.text, e.text)
            self.assertEqual(n.text_type, e.text_type)
            self.assertEqual(n.url, e.url)

if __name__ == "__main__":
    unittest.main()