# author: Grant Bellotti
# date: March 3rd, 2023
# file: tree.py a Python program that implements a binary tree and an expression tree to organize and evaluate user inputted expressions
# input: user expressions 
# output: evaluation of expression

from stack import Stack
class BinaryTree:
    def __init__(self,rootObj):
        self.root = rootObj
        self.leftChild = None
        self.rightChild = None

    #left node
    def insertLeft(self,newNodeVal):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNodeVal)
        else:
            t = BinaryTree(newNodeVal)
            t.leftChild = self.leftChild
            self.leftChild = t

    #right node
    def insertRight(self,newNodeVal):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNodeVal)
        else:
            t = BinaryTree(newNodeVal)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getLeftChild(self):
        return self.leftChild
    
    def getRightChild(self):
        return self.rightChild
    
    def setRootVal(self, obj):
        self.root = obj

    def getRootVal(self):
        return self.root
    
    #format print
    def __str__(self):
        s = f"{self.root}"
        s += '('
        if self.leftChild != None:
            s += str(self.leftChild)
        s += ')('
        if self.rightChild != None:
            s += str(self.rightChild)
        s += ')'
        return s

class ExpTree(BinaryTree):
    def make_tree(postfix):
        stack = Stack()
        for ch in postfix:
            if ch.isdigit():
                stack.push(ch) #add numbers to stack
            else:
                newTree = ExpTree(ch)
                newTree.insertRight(stack.pop())
                newTree.insertLeft(stack.pop())
                stack.push(newTree)
        return stack.pop()

    def preorder(tree):
        s = ''
        if tree:
            operand = str(tree.getRootVal()).replace("(", "").replace(")", "")
            if len(operand) == 3:
                operand = operand[1] + operand[0] + operand[2]
            s += operand 
            s += ExpTree.preorder(tree.getLeftChild())
            s +=  ExpTree.preorder(tree.getRightChild())
        return s
    
    def inorder(tree):
        s = ''
        operator = ['^','*','/','+','-']
        if tree:
            s += ExpTree.inorder(tree.getLeftChild())
            operand = str(tree.getRootVal())
            s += operand
            s += ExpTree.inorder(tree.getRightChild())
            if operand in operator:
                s = f'({s})'
        return s
    
    def postorder(tree):
        s = ''
        if tree:
            operand = str(tree.getRootVal()).replace("(", "").replace(")", "")
            if len(operand) == 3:
                operand = operand[0] + operand[2] + operand[1]
            s += ExpTree.postorder(tree.getLeftChild())
            s += ExpTree.postorder(tree.getRightChild())
            s += operand
        return s

    def evaluate(tree):
        stack = Stack()
        numbers = ExpTree.postorder(tree).split()
        operator = ['^','*','/','+','-']

        for i in numbers:
            stack.push(i)
            if stack.peek() in operator: #check for operator
                op = stack.pop()
                num1 = stack.pop()
                num2 = stack.pop()

                #perform correct operation depending on value
                if op == "^":
                    result = float(num2) ** float(num1)
                elif op == "*":
                    result = float(num1) * float(num2)
                elif op == "/":
                    result = float(num2) / float(num1)
                elif op == "+":
                    result = float(num1) + float(num2)
                else:
                    result = float(num2) - float(num1) 
                stack.push(result)

        return stack.pop()
    
    def __str__(self):
        return ExpTree.inorder(self)

# a driver for testing BinaryTree and ExpTree
if __name__ == '__main__':
    # test a BinaryTree
    
    r = BinaryTree('a')
    assert r.getRootVal() == 'a'
    assert r.getLeftChild()== None
    assert r.getRightChild()== None
    assert str(r) == 'a()()'
    
    r.insertLeft('b')
    assert r.getLeftChild().getRootVal() == 'b'
    assert str(r) == 'a(b()())()'
    
    r.insertRight('c')
    assert r.getRightChild().getRootVal() == 'c'
    assert str(r) == 'a(b()())(c()())'
    
    r.getLeftChild().insertLeft('d')
    r.getLeftChild().insertRight('e')
    r.getRightChild().insertLeft('f')
    assert str(r) == 'a(b(d()())(e()()))(c(f()())())'
    assert str(r.getRightChild()) == 'c(f()())()'
    assert r.getRightChild().getLeftChild().getRootVal() == 'f'
    
    # test an ExpTree
    
    postfix = '5 2 3 * +'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '(5+(2*3))'
    assert ExpTree.inorder(tree) == '(5+(2*3))'
    assert ExpTree.postorder(tree) == '523*+'
    assert ExpTree.preorder(tree) == '+5*23'
    postfix = '5 2 + 3 *'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '((5+2)*3)'
    assert ExpTree.inorder(tree) == '((5+2)*3)'
    assert ExpTree.postorder(tree) == '52+3*'
    assert ExpTree.preorder(tree) == '*+523'
    