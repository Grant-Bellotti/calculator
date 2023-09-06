# author: Grant Bellotti
# date: March 3rd, 2023
# file: calculator.py a Python program that allows users to calculate basic equations 
# input: user expressions
# output: evaluation of expression

from stack import Stack
from tree import ExpTree

def infix_to_postfix(infix):
    stack = Stack()
    infix.strip()
    infix += ' ' #add extra space so no out of bound error
    prec = { "^" : 4, "/" : 3, "*" : 3, "+" : 2, "-" : 2, "(" : 1}
    postfixList = []
    numbers = []

    characterIndex = 0
    while characterIndex < len(infix):
        if infix[characterIndex].isdigit() or infix[characterIndex] == ".":
            nextCharacterIndex = characterIndex + 1
            while infix[nextCharacterIndex].isdigit() or infix[nextCharacterIndex] == ".":
                nextCharacterIndex += 1

            numbers.append(infix[characterIndex:nextCharacterIndex]) #number
            characterIndex = nextCharacterIndex

        else:
            numbers.append(infix[characterIndex])
            characterIndex += 1
            
    numbers.pop()
    for num in numbers:
        if num[0].isdigit():
            postfixList.append(num)
        elif num == '(':
            stack.push(num)
        elif num == ')': 
            operator = stack.pop()

            while not(operator == '('): #checks to find whole parenthesis
                postfixList.append(operator)
                operator = stack.pop()

        #PEMDAS
        else:
            while (not(stack.isEmpty())) and (prec[stack.peek()] >= prec[num]):
                postfixList.append(stack.pop())
            stack.push(num) 

    while not(stack.isEmpty()):
        postfixList.append(stack.pop())

    return " ".join(postfixList)  #return the expression in postfix form

def calculate(infix):
    postFix = infix_to_postfix(infix)
    value = ExpTree.evaluate(ExpTree(postFix)) #calculates expresion
    return value

# a driver to test calculate module
if __name__ == '__main__':
    print('Welcome to Calculator Program!')
    while True:
        userInput = input("Please enter your expression here. To quit enter 'quit' or 'q': \n")
        if userInput.upper() == 'Q' or userInput.upper() == 'QUIT':
            print("Goodbye!")
            break
        answer = calculate(userInput)
        print(answer)

    # test infix_to_postfix function
    assert infix_to_postfix('(5+2)*3') == '5 2 + 3 *'
    assert infix_to_postfix('5+2*3') == '5 2 3 * +'
    # test calculate function
    assert calculate('(5+2)*3') == 21.0
    assert calculate('5+2*3') == 11.0