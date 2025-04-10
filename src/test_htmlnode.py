from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

class TestHTMLNode(unittest.TestCase):
        #html node tests

    def test_rep(self):
        node = HTMLNode( tag= "<h1>", value= "A big heading")
        self.assertEqual(node.__repr__(), "HTMLNode (tag: <h1>, value: A big heading, children: None, props: None)")

    def test_props_to_html(self):
        node = HTMLNode(tag ="<a>", value= "link to boot.dev", props={"href":"https://www.boot.dev"})
        self.assertEqual(node.props_to_html(),' href="https://www.boot.dev"' )

        #leaf node tests
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) 
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>') 

        #parent node tests

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

    def test_complex_html_structure_with_links_and_images(self):
        # Create an image node (self-closing tag)
        img_props = {"src": "example.jpg", "alt": "Example Image"}
        img_node = LeafNode("img", "", img_props)  # Empty string as value instead of None
        
        # Create a link node with text
        link_text = LeafNode(None, "Click here")
        link_props = {"href": "https://example.com", "target": "_blank"}
        link_node = ParentNode("a", [link_text], link_props)
        
        # Create a paragraph containing both the image and link
        paragraph = ParentNode("p", [
            LeafNode(None, "Check out this image: "),
            img_node,
            LeafNode(None, " and "),
            link_node
        ])
        
        # Create a section containing the paragraph
        section = ParentNode("section", [
            LeafNode("h2", "Image and Link Example"),
            paragraph
        ])
        
        # Note: The img tag is now properly closed
        expected_html = "<section><h2>Image and Link Example</h2><p>Check out this image: <img src=\"example.jpg\" alt=\"Example Image\"></img> and <a href=\"https://example.com\" target=\"_blank\">Click here</a></p></section>"
        
        self.assertEqual(section.to_html(), expected_html)

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
