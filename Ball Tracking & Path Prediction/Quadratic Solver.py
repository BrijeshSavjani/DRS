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
    orignal.A -= subtract.A
    orignal.B -= subtract.B
    orignal.C -= subtract.C
    orignal.Y -= subtract.Y
    return orignal
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
r1.multiply((float(X[0]) - float(X[1]))**-1)
r2.multiply((float(X[1]) - float(X[2]))**-1)
r3 = subtract(r1,r2)
r3.multiply((r3.A ** -1))
A = r3.Y
B =r2.Y - (A * r2.A)
eq1 = Equation(float(X[0]),float(Y[0]))
C = eq1.Y - ((eq1.A * A) + (eq1.B * B))
print(A, B, C)
