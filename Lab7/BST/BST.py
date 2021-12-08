from BST.Node import Node


class DuplicateError(BaseException):
    def __init__(self, *args):
        super().__init__(args)


class BST:
    def __init__(self):
        self._root = None
        self._numberOfIndexes = 0
        self._index = 0

    def insertBST(self, value):
        try:
            self.__insertBST(self._root, value)
            self._numberOfIndexes += 1
            return self._numberOfIndexes - 1
        except DuplicateError as e:
            raise e

    def __insertBST(self, insertNode, value):
        if insertNode is None:
            self._root = Node(value, self._numberOfIndexes)
        else:
            if insertNode.value > value:
                if insertNode.left is None:
                    node = Node(value, self._numberOfIndexes)
                    insertNode.left = node
                else:
                    self.__insertBST(insertNode.left, value)
            else:
                if insertNode.value < value:
                    if insertNode.right is None:
                        node = Node(value, self._numberOfIndexes)
                        insertNode.right = node
                    else:
                        self.__insertBST(insertNode.right, value)
                else:
                    raise DuplicateError(f"Symbol {value} already present inside the Symbol table")

    def searchBst(self, value):
        self.__searchBST(self._root, value)

    def __searchBST(self, searchNode, value):
        if searchNode is None:
            return -1
        if searchNode.value > value:
            if searchNode.left is None:
                return -1
            else:
                self.__searchBST(searchNode.left, value)
        else:
            if searchNode.value < value:
                if searchNode.right is None:
                    return -1
                else:
                    self.__searchBST(searchNode.right, value)
            else:
                return searchNode.index

    def printBST(self):
        self.__printBST(self._root)

    def __printBST(self, currentNode):
        if currentNode is None:
            return
        else:
            self.__printBST(currentNode.left)
            print(currentNode.index, '--->', currentNode.value)
            self.__printBST(currentNode.right)

    def getBST(self):
        bst = self.__getBST(self._root)
        return bst

    def __getBST(self, currentNode):
        if currentNode is None:
            return None
        else:
            return (
                currentNode,
                (
                    self.__getBST(currentNode.left),
                    self.__getBST(currentNode.right)
                )
            )


    def getRoot(self):
        return self._root
