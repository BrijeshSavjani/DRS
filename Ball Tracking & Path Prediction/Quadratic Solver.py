class Equation: #In form ax^2 + bx + c = y
    def __init__(self,x,y):
        #Coefficients of the letter. 
        self.A = x**2
        self.B = x
        self.C = 1
        self.Y = y
    def multiply(self,factor): #Multiply out by factor
        self.A *= factor
        self.B *= factor
        self.C *= factor
        self.Y *= factor
def subtract(orignal, subtract): #Subtract one equation from another
    orignal.A -= subtract.A
    orignal.B -= subtract.B
    orignal.C -= subtract.C
    orignal.Y -= subtract.Y
    return orignal
#User Input
equations_invalid = True
while equations_invalid:
    try: #Incase user doesn't input a number
        X = input("Enter x values in the form X1,X2,X3").split(",")
        Y = input("Enter y values in the form Y1,Y2,Y3").split(",")
        eq1 = Equation(float(X[0]),float(Y[0]))
        eq2 = Equation(float(X[1]),float(Y[1]))
        eq3 = Equation(float(X[2]),float(Y[2]))#Define 3 equations(3 needed since there are 3 unknowns)
        equations_invalid = False #Exit loop as inputs were valid
    except:
        print("Incorrect input") #Invalid input
r1 = subtract(eq1,eq2) #Remove +c by subtracting second equation from first
r2 = subtract(eq2,eq3)#Remove +c by subtracting third equation from second
r1.multiply((float(X[0]) - float(X[1]))**-1) #Divide out by (x[0] - x[1]) to get eq in form na + b = k
r2.multiply((float(X[1]) - float(X[2]))**-1) #Same but for second equation
r3 = subtract(r1,r2) # Remove +b by subrtacting both equations to be left whith na = k
r3.multiply((r3.A ** -1)) #Divide by coefficent of A
eq1 = Equation(float(X[0]),float(Y[0])) #Reset eq1 as python passes by reference
A = r3.Y #Set value of A 
B =r2.Y - (A * r2.A) #Substitue value of A into r2 and calculate C
C = eq1.Y - ((eq1.A * A) + (eq1.B * B)) #Sub a & b into eq1 to calculate C
print(A, B, C)
