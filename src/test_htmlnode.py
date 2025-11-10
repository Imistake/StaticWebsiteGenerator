import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_multiple_attrs(self):
        node = LeafNode("a", "Click",
                        {"href": "https://example.com", "target": "_blank", "title": "Go"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank" title="Go">Click</a>'
        )
    def test_leaf_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span></div>")
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    
    def test_to_html_with_props(self):
        parent_node = ParentNode("div", [], {"class": "box"})
        self.assertEqual(parent_node.to_html(), '<div class="box"></div>')

    def test_to_html_nested(self):
        inner = ParentNode("span", [])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span></span></div>")

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()
    
    def test_children_type_validation(self):
        with self.assertRaises(ValueError):
            ParentNode("div", ["not-a-node"])
    
    def test_multiple_props(self):
        node = ParentNode("div", [], {"class": "a", "id": "x"})
        html = node.to_html()
        self.assertIn("<div", html)
        self.assertIn('class="a"', html)
        self.assertIn('id="x"', html)
        self.assertTrue(html.endswith("</div>"))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code_text(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_links(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props.get("href"), "https://boot.dev")
    
    def test_images(self):
        node = TextNode("A cat", TextType.IMAGE, "https://ex.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props.get("src"), "https://ex.com/cat.png")
        self.assertEqual(html_node.props.get("alt"), "A cat")

    def test_unsupported_type_raises(self):
        node = TextNode("x", TextType.TEXT)
        node.text_type = None
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_plain_has_no_props(self):
        node = TextNode("test node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.props)


if __name__ == "__main__":
    unittest.main()