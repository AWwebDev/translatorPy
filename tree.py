class Node:
    def __init__(self, val, per_elem):
        self.val = val
        self.parent_element = per_elem
        self.leaves = []


class Tree:
    def __init__(self):
        self.root = Node("signal-program", None)
        self.current_element = self.root

    def add(self, val):
        tmp_cur_elem = Node(val, self.current_element)
        self.current_element.leaves.append(tmp_cur_elem)
        self.current_element = tmp_cur_elem

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root, 0)

    def _print_tree(self, root, depth):
        for i in range(0, depth):
            print('', end='     ')
        if root.leaves:
            print('<', root.val, '>')
        else:
            print(root.val)
        for leave in root.leaves:
            self._print_tree(leave, depth+1)

    def listing(self):
        if self.root is not None:
            self._listing(self.root)

    def _listing(self, root):
        if not root.leaves:
            if root.val == "empty":
                return
            if root.val == ';':
                print(root.val)
            else:
                print(root.val, end=" ")
        for leave in root.leaves:
            self._listing(leave)