
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):

        if not self.props:
            return ""

        if self.props:
            result = ""
            for prop in self.props:
               result += f' {prop}="{self.props[prop]}"' 
            return result

    def __repr__(self) -> str:
        return f"HTMLNode (tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
 
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag= tag, value= value, props = props)

    def to_html(self) -> str:
        if  self.value is None:
            raise ValueError('leafnode must have value')

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children,props = None):
        super().__init__(tag = tag, children= children, props = props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode require a tag")
        if not self.children:
            raise ValueError("ParentNode require children")

        result =""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>" 
   
    

