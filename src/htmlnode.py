class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        
        attributes = []

        for prop_name, prop_value in self.props.items():
            attributes.append(f'{prop_name}="{prop_value}"')
        
        return " " + " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("self.value is not valid")
        if self.tag is None:
            return self.value
        else:
            attrs = self.props_to_html()
            return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if isinstance(children, list):
            for child in children:
                if not isinstance(child, HTMLNode):
                    raise ValueError("ParentNode children must be HTMLNode instances")
                
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode missing children")
        if not isinstance(self.children, list):
            raise ValueError("ParentNode children must be a list")
        
        props = self.props_to_html()
        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props}>{inner}</{self.tag}>"

        
            
        
