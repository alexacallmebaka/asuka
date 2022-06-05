#This script serves as a basic numerical integrator.
#The script works by first converting the given mathematical function into reverse-polish notation (RPN), and then computing the integral
#We do this as RPN is much easier to evaluate when the function gets very complex.

import re
import math

#This is a custom error that wil be raised if the function input has unbalanced parentheses.
#We inherit from Exception, the base class for user defined exceptions in Python.
class UnbalancedParanthesesError(Exception):
    pass

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

#Some elementry trig functions are not defined in the math module, so we define them here.
cot = lambda x: math.cos(x)/math.sin(x)

sec = lambda x: 1/math.cos(x)

csc = lambda x: 1/math.sin(x)

#This is a table of supported operators for our functions. The tuple each one is mapped to holds important info about said operator.

#The first element states the priority of the operator. This is where it stands in the order of operations heirarchy.
#The higher the number, the higher the priority.lambda

#The second element is the associativity of the operator. This means, when multiple of the them are stack, in what order do you evaluate them.
#Ex. 2-3-5 is evalaued left-to-right, hence left associtivty.lambda

#The third element is what operator Python uses to preform the given operation.
optable = {
    '+':(0,"L","+"),
    '-':(0,"L","-"),
    '*':(1,"L","*"),
    '/':(1,"L","/"),
    '^':(2,"R","**"),
}

#This dictionary contains a list of special functions that we will support, mapped to what functions can be used to evauate them in python.
functable = {
'ln': math.log,
'sin': math.sin,
'cos': math.cos,
'tan': math.tan,
'sec': sec,
'csc': csc,
'cot': cot,
'arcsin': math.asin,
'arccos': math.acos,
'arctan': math.atan
}

#This dictionary maps special numbers to their values in python. 
spectoks = {
    'e': math.e,
    'π': math.pi
}

#The rosetta function is used to convert a function in infix (standard) notation to postfix (reverse-polish) notation.
#We accomplish this with an implementation of Dijkstra's Shunting-Yard algorithim.
#Read more about the Shunting-Yard algorithim here: https://en.wikipedia.org/wiki/Shunting-yard_algorithm

#This function takes in a mathematical function as well as what the variable in the function is. Both inputs are strings.
#Ex. rosetta("3+x","x").
def rosetta(func,var):

    #opstack will hold tokens not ready for output yet.
    opstack = []
    
    #oqueue is where the postfix function will but output to, one token at a time.
    oqueue = []

    for tok in func:

        #If the token is a digit, a variable, or a special number, then add to output.
        if is_float(tok) or tok == var or tok in spectoks:
            oqueue.append(tok)

        #If the function is a token, push the token's correponding python function to opstack.
        elif tok in functable:
            opstack.append(functable[tok])

        #If the token is an operator...
        elif tok in optable:

            #If opstack is not empty, and there is an operator on the top of opstack...
            while len(opstack) != 0 and opstack[-1] in optable:

                #If the operator on top of the stack has greater precedence than "tok" or they have the same precedence and are left associative...

                #The if else inside the while loop here just makes the code more readable.
                if optable[opstack[-1]][0] > optable[tok][0] or optable[opstack[-1]][0] == optable[tok][0] and  optable[tok][1] == "L":
                    
                    #Pop the operator from opstack and add to output.
                    oqueue.append(opstack.pop())
                
                else:
                    break

            #Regardless, push the token to opstack.
            opstack.append(tok)

        #If token is a left parethesis, than push it to opstack.
        elif tok == "(":
            opstack.append(tok)

        #If the token is a right parenthesis, and the stack is not empty....
        elif tok == ")" and len(opstack) != 0:
            
            #While a left parenthesis does not lie on top of opstack, pop from opsatck and add to output.
            try:
                while opstack[-1] != "(":
                    oqueue.append(opstack.pop())
                
                #Pop the left parenthesis from opstack
                opstack.pop()

                #If a function token is on top of opstack, pop it and add to output.
                #We must also check to make sure opstack is not empty, you cannot pop from an empty stack!
                if len(opstack) != 0 and callable(opstack[-1]):
                    oqueue.append(opstack.pop())

            except IndexError:
                raise UnbalancedParanthesesError()

    #If opstack is not empty, pop the rest of opstack to output.
    if len(opstack) != 0: 

        #If a parenthesis in opstack, there are unbalanced parentheses.
        if "(" in opstack or ")" in opstack:

            #Raise the relavent error.
            raise UnbalancedParanthesesError()

        else:
            #We reverse here as we want to pop the values off of opstack, so the top values get added first.
            
            #.reverse() edits the list in-place.
            opstack.reverse()

            #Add the reversed list to output. Effectively "popping" the rest of opstack to output.
            oqueue += opstack

    #Return the output.
    return oqueue
    
#This function evaluates RPN.
def evalRPN(func, var, value):

    #We take the function string, and replace the variable with the value we are plugging into the function.
    func = [value if x == var else x for x in func]

    #We will use this list to evaluate the RPN in a stack fashion.
    calc_stack = []

    #Go through each token in the function.
    for tok in func:

        #If it is a function pop from calc_stack, evaluate the function at that value, and then push back onto the stack.  
        if callable(tok):
             calc_stack.append(tok(float(calc_stack.pop())))
        
        #If the function is a number, push to the stack. 
        elif is_float(tok):
            calc_stack.append(tok)

        #If token is an operator, pop two values from the tack and perform said operation with them.
        elif tok in optable:
            top, sec_top = calc_stack.pop(), calc_stack.pop()
            #top, sec_top = calc_stack.pop(), calc_stack.pop()
            
            #This handles a weird edge case where we have negative leading coefficents or negative numbers in parenthesis.
            #if len(calc_stack) == 0 or is_float(calc_stack[-1]) == False:
            #    sec_top = 0
            #else:
            #    sec_top = calc_stack.pop()

            calc_stack.append(eval("{}{}{}".format(sec_top,optable[tok][2],top)))
        #If the token is a special token, push its value from the spectoks dictionary to the stack.
        elif tok in spectoks:
            calc_stack.append(spectoks[tok])   
    
    #Return the top of the stack, the result, as a float.
    return float(calc_stack[0])

#The function evaluates an infix-notation function at a given point.
def evaluate(func,var,value):

    #First, make sure the value is a string. We need it to be a string in order to pass it to evalRPN.
    value = str(value)

    rpn = rosetta(func, var)
    #Evaluate the RPN at a value.
    return evalRPN(rpn, var, value)

#This prepares our function for integration.
def prep(func,var):

    #This regex inserts the proper multiplication operators in places where the might be absent.
    #For example 4x --> 4*x, (x+4)x --> (x+4)*x
    mult_regex = r'(?<=[0-9πe)' + var + r'])(?=[' + var + r'a-z(])|(?<=[πe)' + var + r'])(?=[' + var + r'a-z0-9(])'
    
    #Use our regex.
    func = re.sub(mult_regex,"*",func)
    
    #To help defeat edge cases, we prefix leading negatives with a zero.
    #Ex. -7x --> 0-7x, (-9)(x+7) --> (0-9)(x+7)
    func = re.sub(r'((?<=^)|(?<=\())(?=-)','0',func)
    
    #This regex will turn our function string into a list of tokens.
    #It begins with adding whitespace between tokens, stripping leading and trailing whitespace, and then splitting on said whitespace.
    #The regex itself defines borders between tokens.
    func = re.sub(r'(?<=[^\da-zA-Z.])|(?=[^\da-zA-Z.])',' ',func).strip().split(' ')
    #Convert the function to reverse-polish notation.

    return func


#Finally, we have reached the main event, the integrator.
#The integrator just adds up a lot of Reimann Sums to approximate an integral using the midpoint rule.
def integrate(func, var, start, end, partitions=1000):
    
    #Prepare the function for integration.
    func = prep(func,var)
    
    #Since ranges in Python are non-inclusive, we add one to our partition count.
    partitions = partitions + 1

    #Delta is how much we increment between partitions.
    delta = (end - start)/(partitions)

    #Avoid excessive division.
    halfdelta = delta/2
    
    point_sum = 0
    
    for i in range(partitions):
        
        #This how we find each point to evaluate at, comes from simplification of the Reimann Sum formula.
        point = start + halfdelta*(2*i + 1)

        #Evaluate the function at that point and add to our running sum.
        point_sum = point_sum + evaluate(func, var, point)
    
    #Multiply by our constant, delta.
    sum = point_sum*delta
    return sum
