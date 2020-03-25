from .errors import UnsetDisplayIndexException


class Step:
    def __init__(self, *text_elements):
        """
        A tree node which represents an instruction.

        :param text_elements: Text, values and UnknownValues to concatenate
            together when this step is displayed
        """
        self.text_elements = text_elements
        self.children = list()

        # This is set to the step number when it is displayed
        self.display_index = None

    def __repr__(self):
        if self.display_index is None:
            raise UnsetDisplayIndexException(
                'Display index not set, cannot reference step')

        return f'step {self.display_index}'

    def text(self):
        text = str()
        for element in self.text_elements:
            text += str(element)
        return text

    def add_child(self, *args, **kwargs):
        """
        Create a new Step and add it as a child of this one.

        :returns: Created step
        """
        child = Step(*args, **kwargs)
        self.children.append(child)
        return child

    def leaf_nodes(self):
        """Yield the leaves which are descendants of this step."""
        if len(self.children) > 0:
            for child in self.children:
                # Recursively call leaf_nodes on each child
                for leaf in child.leaf_nodes():
                    yield leaf
        else:
            # We are a leaf node
            yield self
