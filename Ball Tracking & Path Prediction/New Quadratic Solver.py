import copy
def GetMatrix():
    Input =  [[],[],[]]
    for Rows in range(0,3):
        Row = []
        for Columns in range(0,3):
            Valid = False
            while Valid == False:
                try:
                    UserInput = input("Input: Row>" + str(Rows) + " Column>" + str(Columns)+ ": ")
                    Row.append(int(UserInput))
                    Valid = True
                except:Valid = False
        Input[Rows] = Row
    return Input

def Determinant(Matrix): #Only works w/ 2x2 Matrixes, copy not needed as Matrix not modified
    ad = Matrix[0][0] * Matrix[1][1]
    bc = Matrix[0][1] * Matrix[1][0]
    return(ad-bc)
def Minor(Row,Column,Matrix): 
    Matrix = copy.deepcopy(Matrix)
    for row in Matrix:
        row.pop(Column)
    Matrix.pop(Row)
    return(Determinant(Matrix))
def Coefficient(Matrix):#Only works for 3x3 matrices
    det = Matrix[0][0]*Minor(0,0,Matrix) - Matrix[0][1]*Minor(0,1,Matrix) + Matrix[0][2]*Minor(0,2,Matrix)
    return (1/det) 
def Transpose(Matrix): #For  n*n matrices only
    Transposed = copy.deepcopy(Matrix)
    n = len(Matrix[0]) #Dimensions
    for r in range(0,n):
        for c in range(0,n):
            Transposed[r][c] = copy.deepcopy(Matrix)[c][r]
        return Transposed
def MatrixOfMinors(Matrix):
        MinorMatrix = copy.deepcopy(Matrix)
        n = len(Matrix[0]) #Dimensions
        for Rows in range(0,n):
            for Columns in range(0,n):
                MinorMatrix[Rows][Columns] = Minor(Rows,Columns,Matrix)
        return MinorMatrix
def Cofactors(Matrix):
    Cofactor = copy.deepcopy(Matrix)
    n = len(Matrix[0]) #Dimensions
    for Rows in range(0,n):
        for Columns in range(0,n):
            if ((3* Rows) + Columns + 1) % 2 == 0:
                 Cofactor[Rows][Columns] *= -1
    return Cofactor
try:
    Input = GetMatrix()
    transposed = Transpose(Input)
    minors = MatrixOfMinors(transposed)
    cofactors = Cofactors(minors)
    print("Coefficient: " + str(Coefficient(Input)) + " Result: " + str(cofactors))
except: print("No solution")