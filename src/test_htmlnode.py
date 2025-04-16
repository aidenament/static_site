import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with empty props dictionary
        node = HTMLNode("div", "Hello", [], {})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(node.props_to_html(), " class=\"container\"")
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode("a", "Click me", [], {"href": "https://example.com", "class": "link", "id": "main-link"})
        # Order of props may vary, so we check for each part separately
        result = node.props_to_html()
        self.assertIn("href=\"https://example.com\"", result)
        self.assertIn("class=\"link\"", result)
        self.assertIn("id=\"main-link\"", result)
        self.assertEqual(len(result.split()), 3) # 3 props
    
    def test_repr_method(self):
        # Test the __repr__ method
        node = HTMLNode("p", "Paragraph text", [], {"class": "text"})
        repr_result = node.__repr__()
        self.assertIn("tag: p", repr_result)
        self.assertIn("value: Paragraph text", repr_result)
        self.assertIn("property: class= text", repr_result)
    
    def test_repr_with_children(self):
        # Test __repr__ with children
        child = HTMLNode("span", "child text", [], {})
        parent = HTMLNode("div", None, [child], {"id": "parent"})
        repr_result = parent.__repr__()
        self.assertIn("tag: div", repr_result)
        self.assertIn("tag: span", repr_result)
        self.assertIn("value: child text", repr_result)
        self.assertIn("property: id= parent", repr_result)
        
    def test_initialization(self):
        # Test initialization of HTMLNode
        node = HTMLNode("h1", "Title", [], {"class": "heading"})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "heading"})
    
    def test_initialization_with_none_values(self):
        # Test initialization with None values
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("div", "Content", {"class": "container", "id": "main", "data-test": "value"})
        html = node.to_html()
        self.assertIn("<div", html)
        self.assertIn(">Content</div>", html)
        self.assertIn("class=\"container\"", html)
        self.assertIn("id=\"main\"", html)
        self.assertIn("data-test=\"value\"", html)
    
    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Text", {})
        self.assertEqual(node.to_html(), "<span>Text</span>")
        
    def test_leaf_to_html_none_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_initialization(self):
        node = LeafNode("h1", "Title", {"class": "heading"})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "heading"})
    
    def test_leaf_default_props(self):
        node = LeafNode("p", "Text")
        self.assertIsNone(node.props)

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        # Test basic ParentNode functionality
        child = LeafNode("p", "Hello, world!")
        parent = ParentNode("div", [child], {})
        self.assertEqual(parent.to_html(), "<div><p>Hello, world!</p></div>")
    
    def test_parent_node_with_props(self):
        # Test ParentNode with properties
        child = LeafNode("span", "Content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        html = parent.to_html()
        self.assertTrue(html.startswith("<div"))
        self.assertTrue(html.endswith("</div>"))
        self.assertIn("<span>Content</span>", html)
    
    def test_multiple_children(self):
        # Test ParentNode with multiple children
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        child3 = LeafNode("p", "Paragraph 3")
        parent = ParentNode("div", [child1, child2, child3], {})
        html = parent.to_html()
        self.assertEqual(html, "<div><p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p></div>")
    
    def test_nested_parent_nodes(self):
        # Test nested ParentNodes
        inner_child = LeafNode("span", "Inner content")
        inner_parent = ParentNode("div", [inner_child], {"class": "inner"})
        outer_parent = ParentNode("section", [inner_parent], {"class": "outer"})
        html = outer_parent.to_html()
        self.assertEqual(html, "<section><div><span>Inner content</span></div></section>")
    
    def test_deep_nesting(self):
        # Test deep nesting of ParentNodes
        text = LeafNode("span", "Deep content")
        level3 = ParentNode("div", [text], {"class": "level3"})
        level2 = ParentNode("div", [level3], {"class": "level2"})
        level1 = ParentNode("div", [level2], {"class": "level1"})
        html = level1.to_html()
        self.assertEqual(html, "<div><div><div><span>Deep content</span></div></div></div>")
    
    def test_mixed_leaf_and_parent_children(self):
        # Test a mix of LeafNodes and ParentNodes as children
        leaf1 = LeafNode("p", "Paragraph")
        inner_parent = ParentNode("div", [LeafNode("span", "Inner content")], {})
        leaf2 = LeafNode("p", "Another paragraph")
        parent = ParentNode("section", [leaf1, inner_parent, leaf2], {})
        html = parent.to_html()
        self.assertEqual(html, "<section><p>Paragraph</p><div><span>Inner content</span></div><p>Another paragraph</p></section>")
    
    def test_empty_children_list(self):
        # Test ParentNode with empty children list
        parent = ParentNode("div", [], {})
        self.assertEqual(parent.to_html(), "<div></div>")
    
    def test_none_tag(self):
        # Test error when tag is None
        child = LeafNode("p", "Text")
        parent = ParentNode(None, [child], {})
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_none_children(self):
        # Test error when children is None
        with self.assertRaises(ValueError):
            ParentNode("div", None, {}).to_html()
    
    def test_non_htmlnode_children(self):
        # Test behavior with non-HTMLNode children
        # This test should fail because children should be HTMLNode instances
        with self.assertRaises(AttributeError):
            parent = ParentNode("div", ["not a node", 123], {})
            parent.to_html()
    
    def test_initialization(self):
        # Test initialization
        children = [LeafNode("p", "Text")]
        parent = ParentNode("div", children, {"id": "test"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, children)
        self.assertEqual(parent.props, {"id": "test"})
        self.assertIsNone(parent.value)
    
    def test_repr(self):
        # Test __repr__ method for ParentNode
        child = LeafNode("p", "Text")
        parent = ParentNode("div", [child], {"class": "container"})
        repr_result = parent.__repr__()
        self.assertIn("tag: div", repr_result)
        self.assertIn("tag: p", repr_result) 
        self.assertIn("value: Text", repr_result)
        self.assertIn("property: class= container", repr_result)


if __name__ == "__main__":
    unittest.main()
