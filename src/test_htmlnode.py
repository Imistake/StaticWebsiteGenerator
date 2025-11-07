import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_something_descriptive(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://boot.dev"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://boot.dev"')

    def test_props_is_none(self):
        node = HTMLNode("a", "Click me", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_constructor_values(self):
        node = HTMLNode("p", "words in a paragraph", None, {"href": "https://boot.dev"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "words in a paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://boot.dev"})

    def test_to_html(self):
        node = HTMLNode("p", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com", "target": "_blank", "title": "Click Me!"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank" title="Click Me!"')

    def test_repr(self):
        node = HTMLNode("p", "words in a paragraph", None, {"href": "https://boot.dev"})
        result = repr(node)
        self.assertEqual(result, "HTMLNode(p, words in a paragraph, children: None, {'href': 'https://boot.dev'})")

    def test_with_children(self):
        child1 = HTMLNode("p", "First")
        child2 = HTMLNode("p", "Second")
        node = HTMLNode("div", None, [child1, child2], None)
        self.assertEqual(node.children, [child1, child2])

    def test_default_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        

        if __name__ == "__main__":
            unittest.main()