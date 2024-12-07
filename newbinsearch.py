class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def __contains__(self, key):
        return self.find(key) is not None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, root, key):
        if key < root.key:
            if root.left is None:
                root.left = Node(key)
            else:
                self._insert(root.left, key)
        elif key > root.key:
            if root.right is None:
                root.right = Node(key)
            else:
                self._insert(root.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete(root.right, temp.key)
        return root

    def _min_value_node(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def find(self, key):
        return self._find(self.root, key)

    def _find(self, root, key):
        if root is None:
            return None
        if key < root.key:
            return self._find(root.left, key)
        elif key > root.key:
            return self._find(root.right, key)
        else:
            return root

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.key)
            self._inorder(root.right, result)

    def display(self):
        self._display(self.root, 0)

    def _display(self, root, level):
        if root:
            self._display(root.right, level + 1)
            print(" " * 4 * level + "->", root.key)
            self._display(root.left, level + 1)

    # New functionalities

    def find_min(self):
        if self.root is None:
            return None
        return self._min_value_node(self.root)

    def find_max(self):
        current = self.root
        while current.right is not None:
            current = current.right
        return current

    def find_successor(self, key):
        node = self.find(key)
        if node is None:
            return None
        if node.right:
            return self._min_value_node(node.right)
        successor = None
        current = self.root
        while current:
            if key < current.key:
                successor = current
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                break
        return successor

    def find_predecessor(self, key):
        node = self.find(key)
        if node is None:
            return None
        if node.left:
            current = node.left
            while current.right:
                current = current.right
            return current
        predecessor = None
        current = self.root
        while current:
            if key < current.key:
                current = current.right
            elif key > current.key:
                predecessor = current
                current = current.left
            else:
                break
        return predecessor

    def tree_height(self):
        return self._tree_height(self.root)

    def _tree_height(self, root):
        if root is None:
            return 0
        left_height = self._tree_height(root.left)
        right_height = self._tree_height(root.right)
        return max(left_height, right_height) + 1

    def is_balanced(self):
        return self._is_balanced(self.root)

    def _is_balanced(self, root):
        if root is None:
            return True
        left_height = self._tree_height(root.left)
        right_height = self._tree_height(root.right)
        return abs(left_height - right_height) <= 1 and self._is_balanced(root.left) and self._is_balanced(root.right)

    def level_order(self):
        if self.root is None:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
