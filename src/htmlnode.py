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