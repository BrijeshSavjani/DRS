class Equation:
    def __init__(self,A,B,C,equals):
        self.A = A
        self.B = B
        self.C = C
        self.equals = equals
def UserInput():
    print("Please type the co-ordinate in the form x,y")
    Cordinate = input(">")
    X = Cordinate.split(",")[0]
    Y = Cordinate.split(",")[1]
    ret = str(float(X)**2) +  "," + X + "," + Y
    return ret
def SubtractEquations(EQ1 = Equation, EQ2 = Equation):
    Subtracted_A = float(EQ1.A) - float(EQ2.A)
    Subtracted_B = float(EQ1.B) - float(EQ2.B)
    Subtracted_Equals = float(EQ1.equals) - float(EQ2.equals)
    Subtracted_Equation = Equation(Subtracted_A,Subtracted_B,0,Subtracted_Equals)
    return(Subtracted_Equation)
def MatchCoefficients(target, EQ1 = Equation, EQ2 = Equation ):
    print("A from EQ1: ",EQ1.A,"Ratio: ",ratio,"A from EQ2 :", EQ2.A)
    switch (target):
        target == "A":
            ratio = float(EQ1.A)/float(EQ2.A)
            EQ2.A * ratio
            EQ1.A * (ratio**-1)
    
#Create Equation object for co-ordinate1
returned_values = UserInput()
equation_values = returned_values.split(",")
InitialEQ1 = Equation(equation_values[0],equation_values[1],0,equation_values[2])
#Create Equation object for co-ordinate2
returned_values = UserInput()
equation_values = returned_values.split(",")
InitialEQ2 = Equation(equation_values[0],equation_values[1],0,equation_values[2])
#Create Equation object for co-ordinate3
returned_values = UserInput()
equation_values = returned_values.split(",")
InitialEQ3 = Equation(equation_values[0],equation_values[1],0,equation_values[2])

Step_1 = SubtractEquations(InitialEQ1,InitialEQ2)
print(Step_1.A)
Step_2 = SubtractEquations(InitialEQ2,InitialEQ3)
print(Step_2.A)
MatchCoefficients("A",Step_1,Step_2)
