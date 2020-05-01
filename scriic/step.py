from .errors import UnsetDisplayIndexException
from .value import Value


class Step:
    """
    A tree node which represents an instruction.

    :param text: Either a Value instance, or a single object which will be
        converted to Value.

    :var children: List of child steps.
    :var display_index:
        When the step is displayed or rendered, this should be set to a number
        or string which can be used by future steps to tell the user to refer
        back to this step.
    """

    def __init__(self, text):
        if type(text) != Value:
            text = Value(text)

        self.text_value = text
        self.children = list()

        # This is set to the step number when it is displayed
        self.display_index = None

    def get_display_index(self):
        """
        Get the display index for this step.

        If this step does not have a display index itself, attempt to return
        the display index of its first child. This can recurse and have the
        effect of selecting the display index of the first leaf node.

        :raises UnsetDisplayIndexException: No display index could be found.
        """
        if self.display_index is not None:
            return self.display_index
        elif len(self.children) > 0:
            return self.children[0].get_display_index()
        else:
            raise UnsetDisplayIndexException("Display index not set")

    def __repr__(self):
        return f"step {self.get_display_index()}"

    def text(self):
        """Return the static text of this step."""
        return str(self.text_value)

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
