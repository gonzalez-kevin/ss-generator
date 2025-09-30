import unittest

from blocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type

class TestBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
            
class TestBlockType(unittest.TestCase):
        def test_heading(self):
            for i in range(1, 7):
                self.assertEqual(
                    block_to_block_type(f"{'#'*i} Heading text"),
                    BlockType.HEADING
                )

        def test_code_block(self):
            code = "```\nprint('hello')\n```"
            self.assertEqual(block_to_block_type(code), BlockType.CODE)

        def test_quote(self):
            quote = "> This is a quote\n> continued quote"
            self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

        def test_unordered_list(self):
            ul = "- Item 1\n- Item 2\n- Item 3"
            self.assertEqual(block_to_block_type(ul), BlockType.ULIST)

        def test_ordered_list(self):
            ol = "1. First\n2. Second\n3. Third"
            self.assertEqual(block_to_block_type(ol), BlockType.OLIST)

        def test_ordered_list_non_sequential(self):
            # Should fallback to paragraph because numbers do not increment properly
            ol = "1. First\n3. Second"
            self.assertEqual(block_to_block_type(ol), BlockType.PARAGRAPH)

        def test_paragraph(self):
            paragraph = "This is a normal paragraph.\nIt has multiple lines."
            self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)