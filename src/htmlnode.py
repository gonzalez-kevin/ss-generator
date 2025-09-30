class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
            
        return " " + " ".join(str(attribute) for attribute in attributes)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a non-None value")
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if tag is None or not children:
            raise ValueError("ParentNode requires a non-None tag and children")
        super().__init__(tag = tag, children = children, props = props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Please include a tag")
        if not self.children:
            raise ValueError("Please include at least one child")
        children_html = "".join(
            child.to_html() if isinstance(child, HTMLNode) else str(child)
            for child in self.children
        )
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"