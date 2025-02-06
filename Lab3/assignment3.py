#define the class
class Shape:
    def __init__():
        pass

#create the rectangle subclass
class Rectangle(Shape):
    def __init__(self,l,w): #will read the text file and the variables will be assigned in the init order
        self.length=l
        self.width=w #take the string text and make it an attribute of the rectangle
    def calcArea(self):
        return self.length * self.width 
    
#create the circle subclass
class Circle(Shape):
    def __init__(self,r): 
        self.radius=r
    def calcArea(self):
        return 3.14 * self.radius ** 2
    
#create triangle subclass
class Triangle(Shape):
    def __init__(self,b,h):
        self.base=b
        self.height=h
    def calcArea(self):
        return 0.5 * self.base * self.height
    
#read the text file
shapes_file = open(r'C:\Users\leahmrdz22\MataRodriguez-online-GEOG676-spring2025\Lab3\shape.txt','r')
lines = shapes_file.readlines() 
shapes_file.close()

for line in lines:
    splits = line.split(',') #breaking up the test at commas
    shape = splits[0] #telling python the shape name is in the first position

    if shape == 'Rectangle':
        rect = Rectangle(int(splits[1]),int(splits[2])) #identifying the second and third positions for calculations; turn them into integers
        print('The rectangle area is ', rect.calcArea())

    elif shape == 'Circle':
        circ = Circle(int(splits[1]))
        print('The circle area is ', circ.calcArea())

    elif shape == 'Triangle':
        tri = Triangle(int(splits[1]),int(splits[2]))
        print('The triangle area is ', tri.calcArea())

    else:
        pass