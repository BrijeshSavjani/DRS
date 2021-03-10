class Equation:
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
def subtract(orignal, subtract):
    result = orignal
    result.A -= subtract.A
    result.B -= subtract.B
    result.C -= subtract.C
    result.Y -= subtract.Y
    return result
#User Input
equations_invalid = True
while equations_invalid:
    try:
        X = input("Enter x values in the form X1,X2,X3").split(",")
        Y = input("Enter y values in the form Y1,Y2,Y3").split(",")
        eq1 = Equation(float(X[0]),float(Y[0]))
        eq2 = Equation(float(X[1]),float(Y[1]))
        eq3 = Equation(float(X[2]),float(Y[2]))
        equations_invalid = False
    except:
        print("Incorrect input")
r1 = subtract(eq1,eq2)
r2 = subtract(eq2,eq3)
r1.multiply((X[0] - X[1])**-1)
r2.multiply((X[0] - X[1])**-1)