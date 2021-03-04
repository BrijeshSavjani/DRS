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

#User Input
equations_invalid = True
while equations_invalid:
    try:
        values = input("Enter x and y in the form x,y").split(",")
        values2 = input("Enter x and y in the form x,y").split(",")
        eq1 = Equation(float(values[0]),float(values[1]))
        eq2 = Equation(float(values2[0]),float(values2[1]))
        equations_invalid = False
    except:
        print("Incorrect input")
