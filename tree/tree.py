class TreeNode:
    def __init__(self, element=None):
        self.element = element
        self.children = []
        self.parent = None

    def __repr__(self):
        if self.element is None:
            return "None"
        else:
            result = str(self.element)
            for child in self.children:
                result += str(child)
            result += "</NODE>"
            return result

    def size(self):
        size = 1
        for child in self.children:
            size += child.size()

        return size

    def addChild(self, element):
        child = TreeNode(element)
        child.parent = self
        self.children.append(child)
        return child

if __name__ == '__main__':
# test the class
    nodeRoot = TreeNode("A")
    node1 = nodeRoot.addChild("B")
    node2 = nodeRoot.addChild("C")
    node3 = nodeRoot.addChild("D")
    node4 = node1.addChild("E")
    node5 = node4.addChild("F")
    node6 = node1.addChild("G")
    node7 = node5.addChild("H")

    print "the tree has " + str(nodeRoot.size()) + " nodes"
    print nodeRoot
