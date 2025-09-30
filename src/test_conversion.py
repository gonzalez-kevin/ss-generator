import unittest

from conversion import text_node_to_html_node, split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()