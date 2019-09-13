# The following code is derived from Geeks for Geeks
# Infix to Postfix article (https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/)

class Et:
    """
        Class Et for a node in the binary expression tree
    """

    # Constructor to create a node
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Conversion:

    # Constructor to initialize the class variables
    def __init__(self):
        self.top = -1
        # This array is used a stack  
        self.array = []
        self.output = []
        self.precedence = {'AND': 2, 'NOT': 1, 'OR': 0}

    def is_empty(self) -> bool:
        return True if self.top == -1 else False

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.is_empty():
            self.top -= 1
            return self.array.pop()

        else:
            return None

    def push(self, item) -> None:
        self.top += 1
        self.array.append(item)

    def is_operand(self, op):
        return not (op == 'AND' or op == 'OR' or op == 'NOT')

    def infix_to_postfix(self, exp, return_type='list'):
        """
            A method to converts the given infix expression to
            postfix expression
        :param exp: a string of infix expression
        :param return_type: a string specifying the type of the returned expression
                            (either list of words or string)
        :return: postfix expression of the input string
        """
        # Split the expression strings to a list of words
        exp = exp + ')'
        exp_ls = exp.split()

        self.push('(')
        # Iterate over the expression for conversion
        for i in exp_ls:

            # If the character is an '(', push it to stack
            if i[0] == '(':
                self.push('(')
                # Append the operand to the output
                self.output.append(i[1:])

            # If the scanned character is an ')', pop and output
            # from the stack until a '(' is found
            elif i[-1] == ')':
                a = i[:-1]
                self.output.append(a)
                while (not self.is_empty()) and self.peek() != '(':
                    a = self.pop()
                    self.output.append(a)
                if (not self.is_empty()) and self.peek() != '(':
                    return ""
                else:
                    self.pop()
            # If the current word is an operand,
            # add it to output
            elif self.is_operand(i):
                self.output.append(i)

            # An operator is encountered
            else:
                while not self.is_empty() and self.peek() != '(':
                    a = self.peek()
                    if self.precedence[a] >= self.precedence[i]:
                        self.output.append(a)
                        self.pop()
                    else:
                        break

                self.push(i)

        while not self.is_empty():
            self.output.append(self.pop())

        if return_type == 'list':
            return self.output
        else:
            return " ".join(self.output)

    # Returns root of constructed tree for
    # given postfix expression
    def constructTree(self, postfix):
        """
            Method takes a string or list of words of postfix and build
            a binary expression tree

        :param postfix: string or list of words
        :return: t: root of the binary expression tree
        """
        if type(postfix) == str:
            postfix_ls = postfix.split()
        else:
            postfix_ls = postfix

        stack = []

        # Traverse through every character of input expression
        for word in postfix_ls:

            # if operand, simply push into stack
            if self.is_operand(word):
                t = Et(word)
                stack.append(t)
            # If the current  Operator
            else:
                # Pop two top nodes
                t = Et(word)
                t1 = stack.pop()
                t2 = stack.pop()

                # make them children
                t.right = t1
                t.left = t2

                # Add this subexpression to stack
                stack.append(t)

                # Only element  will be the root of expression tree
        t = stack.pop()

        return t

    # A utility function to do inorder traversal
    def inorder(self, t):
        """
            This method is to print out the inorder traversal of the
            current binary expression tree.
        :param t: a pointer to the root of the tree
        :return: nothing
        """
        if t is not None:
            self.inorder(t.left)
            print(t.value)
            self.inorder(t.right)


c = Conversion()
s = "(flower OR boobs) AND chair AND (love OR blanket) NOT pillow"
postfix = c.infix_to_postfix(s)
print(postfix)
tree = c.constructTree(postfix)
print("My tree looking good!!!")
c.inorder(tree)