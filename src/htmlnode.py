class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None or (len(self.props.keys()) == 0):
            return ""
        out = " "
        for key, value in self.props.items():
            out += f"{key}=\"{value}\" "
        return out[:-1]
    
    def __repr__(self):
        out = ""
        out += f"tag: {self.tag} \n value: {self.value}\n"
        if self.children is not None:
            for child in self.children:
                out += child.__repr__() 
        if self.props is not None:
            for key, value in self.props.items():
                out += f"property: {key}= {value}\n"
        return out
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value cannot be None")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag cannot be None")
        if self.children is None:
            raise ValueError("children cannot be None")
        html = [child.to_html() for child in self.children]
        html = "".join(html)
        return f"<{self.tag}>{html}</{self.tag}>"
