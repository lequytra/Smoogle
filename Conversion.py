# The following code is derive from Geeks for Geeks
# Infix to Postfix article (https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/)


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

    def infix_to_postfix(self, exp):
        """
            A method to converts the given infix expression to
            postfix expression
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

        return " ".join(self.output)


c = Conversion()
s = "(flower OR boobs) AND chair AND (love OR blanket) NOT pillow"
print(c.infix_to_postfix(s))
