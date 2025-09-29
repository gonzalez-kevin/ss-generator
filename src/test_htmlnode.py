import unittest

from htmlnode import HTMLNode

test_dict1 = {
    "href": "https://www.google.com",
    "target": "_blank",
}

test_dict2 = {
    "href": "https://www.google.com"
}

class TestHTMLNode(unittest.TestCase):
    
    def test_link1(self):
        htmlnode = HTMLNode("p", "This is the test text.", None, test_dict1)
        test_node = htmlnode.props_to_html()
        expected_text = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test_node, expected_text)
    
    def test_link2(self):
        htmlnode = HTMLNode("p", "This is the test text.", None, test_dict2)
        test_node = htmlnode.props_to_html()
        expected_text = ' href="https://www.google.com"'
        self.assertEqual(test_node, expected_text)
        
if __name__ == "__main__":
    unittest.main()