import copy
def GetMatrix(x,y):
    Input = []  #Matrix is a list that contains child lists for rows
    for Rows in range(0,x):
        Row = []
        for Columns in range(0,y):
            Valid = False
            while Valid == False:
                try:
                    UserInput = input("Input: Row>" + str(Rows) + " Column>" + str(Columns)+ ": ")
                    Row.append(float(UserInput))
                    Valid = True
                except:Valid = False
        Input.append(Row)
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
def Transpose(Matrix): 
    Transposed = copy.deepcopy(Matrix)
    n = len(Matrix[0]) #Dimensions
    for rows in range(0,n):
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
            Cofactor[Rows][Columns] *= ((-1)**(Rows + Columns))
    return Cofactor
def DotProduct(Matrix,YMatrix):
    dotproduct = []
    temp =0
    for x in range(0,len(Matrix)):
        for y in range(0,len(Matrix)):
            temp += Matrix[x][y] * YMatrix[y]
        dotproduct.append(temp)
        temp = 0
    return dotproduct
def ScalarMultiply(Matrix,Coefficient):
        MultipliedMatrix = copy.deepcopy(Matrix)
        n = len(Matrix[0]) #Dimensions
        for Rows in range(0,n):
            for Columns in range(0,n):
                MultipliedMatrix[Rows][Columns] *= Coefficient 
        return MultipliedMatrix

try:
    Input = GetMatrix(3,3)
    YValues = GetMatrix(3,1)
    transposed = Transpose(Input)
    minors = MatrixOfMinors(Input)
    cofactors = Cofactors(minors)
    coefficients =  DotProduct(ScalarMultiply(cofactors,Coefficient(Input)),YValues)
    print("Coefficients: " + str(coefficients))
except: print("No solution")