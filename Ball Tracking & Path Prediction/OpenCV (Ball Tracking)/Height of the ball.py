def Find1DVelocity(coordinates):
    displacement = coordinates[len(coordinates)] - coordinates[0]
    time = len(coordinates) / 30
    return (displacement/time)
def SecondRoot(inititial_vertical_velocity,horrizontal_velocity,e,root1_x):
    vertex_x = ((e * inititial_vertical_velocity) / -9.91) * horrizontal_velocity
    root2_x = (vertex_x - root1_x) + vertex_x
    return root2_x
def Coefficients(max_height,root1,root2):
    max_height_x = (root1 + root2)/2
    y = (max_height_x)^2 - ((root1 + root2) * max_height_x) + (root1 * root2)
    a = max_height / y
    b = a * -(root1 + root2)
    c = a * -(root1 * root2)
    return([a,b,c])
def GetHeight(coeffcients):
    return (Coefficients[0] * 500^2) + (coeffcients[1] * 500) + coeffcients[2]