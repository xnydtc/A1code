import copy
import math  # For PI
import sys
from abc import abstractmethod


#  Class Shape the superclass of all shapes
class Shape(object):  # inherits from objects
    @abstractmethod
    def getName(self):
        return ""

    @abstractmethod
    def getArea(self):
        return ""

    @abstractmethod
    def getVolume(self):
        return ""


# Class Point, a subclass of Shape
class Point(Shape):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def getName(self):
        return "Point"

    # Point does not have area, but still a subclass will need to implement all abstract method
    def getArea(self):
        return ""

    # Point does not have volume, but still a subclass will need to implement all abstract method
    def getVolume(self):
        return ""

    def __str__(self):
        return "[" + str(self._x) + "," + str(self._y) + "]"

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y


# Class Circle, a subclass of point
class Circle(Point):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self._r = 0
        self.setRadius(r)

    def getName(self):
        return "Circle"

    def getArea(self):
        return math.pi * self._r * self._r

    def __str__(self):
        return "C=" + super().__str__() + "; R=" + str(self._r)

    def getRadius(self):  # get/set radius methods
        return self._r

    def setRadius(self, r):
        if r > 0:
            self._r = r


# Class Cylinder, a subclass of Circle
class Cylinder(Circle):
    def __init__(self, x, y, r, h):
        super().__init__(x, y, r)
        self._h = 0
        self.setHeight(h)

    def getName(self):
        return "Cylinder"

    def getArea(self):
        return 2. * super().getArea() + 2. * math.pi * self.getRadius() * self._h

    def getVolume(self):
        return super().getArea() * self._h

    def __str__(self):
        return "C=" + super().__str__() + ";H=" + str(self._h)

    def getHeight(self):
        return self._h

    def setHeight(self, h):
        if h > 0:
            self._h = h


# Class Sphere, a subclass of Circle
class Sphere(Circle):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)

    def getName(self):
        return "Sphere"

    def getArea(self):
        return 4. * super().getArea()

    def getVolume(self):
        return ""

    # Need to tale a look
    def __str__(self):
        return super().__str__() + ";R=" + str(self._r)

    def getRadius(self):
        return self._r

    def setRadius(self, r):
        if r > 0:
            self._r = r


class Rectangle(Shape):
    def __init__(self, x, y):
        if x > 0:
            self._x = x
        if y > 0:
            self._y = y

    def getName(self):
        return "Rectangle"

    def getArea(self):
        return self._x * self._y

    def getVolume(self):  # Rectangle does not have volume
        return ""

    def __str__(self):
        return "X=" + str(self._x) + ";Y=" + str(self._y)

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setX(self, x):
        if x > 0:
            self._x = x

    def setY(self, y):
        if y > 0:
            self._y = y


# We could get a square from the rectangle, but I think the number of params is not equal. So it inherits from Shape
class Square(Shape):
    def __init__(self, s):
        if s > 0:
            self._s = s

    def getName(self):
        return "Square"

    def getArea(self):
        return self._s * self._s

    def getVolume(self):  # Square does not have volume
        return ""

    def __str__(self):
        return "S=" + str(self._s)

    def getS(self):
        return self._s

    def setS(self, s):
        if s > 0:
            self._s = s


# Cube, a subclass of square
class Cube(Square):
    def __init__(self, s):
        super().__init__(s)

    def getName(self):
        return "Cube"

    def getArea(self):
        return 6. * super().getArea()

    def getVolume(self):
        return self._s * super().getArea()

    def __str__(self):
        return super().__str__()

    def getS(self):
        return super().getS()

    def setS(self, s):
        return super().setS(s)


class menu():
    def __init__(self):  # the class constructor
        self._data = []  # initialises the _data “private” instance variable to an empty list

    def getData(self):
        return self._data  # returns the contained data list to users of the class

    def setData(self, data):  # initialises the list with “externally-created” data
        self._data = data

    def start(self):
        print("Menu:")
        print("1: Create An Object")
        print("2: Delete An Object")
        print("3: Print Function")
        print("4: Modify An Object")
        print("4: Exit")
        while(True):
            try:
                print("Please Enter the command:")
                command = int(input())
                if command == 1:
                    self.create()
                elif command == 2:
                    print('Please Enter the Object Index')
                    index = int(input())
                    self.remove(index)
                elif command == 3:
                    print('Please Enter an Object Index or All to print all objects')
                    print_index = input()
                    self.print(print_index)
                elif command == 4:
                    print('Please Enter the Object Index')
                    modify_index = input()
                    self.modify(modify_index)
                elif command == 5:
                    sys.exit()
                else:

                    print("Please Input A Valid Option (1-4)")
            except ValueError:
                print("input should be an int!")


    @staticmethod
    def _getNDataFromKeyboard():
        print("Enter Type of Shape you want to Create")
        data = ""
        nshapes = 0
        gotDataCorrectly = gotNShapesCorrectly = False
        while not gotDataCorrectly:
            try:
                data = str(input())
                print(data)
                if data in ["Shape", "Point", "Circle", "Cylinder", "Sphere", "Rectangle", "Square", "Cube"]:
                    gotNDataCorrectly = True
                    break
                else:
                    print("_getNDataFromKeyboard: Your will need to input an valid shape")
            except(ValueError, SyntaxError):
                print("_getNDataFromKeyboard: data should be an string!")

        print("Enter the Number of Shape you want to Create")

        while not gotNShapesCorrectly:
            try:
                nshapes = int(input())  # read from the keyboard, accept also strings & convert
                if nshapes >= 0:  # check for integer input >= 2
                    gotNShapesCorrectly = True
                else:
                    print("_getNDataFromKeyboard: nshapes should be >=2")
            except(ValueError, SyntaxError):
                print("_getNDataFromKeyboard: nshapes should be an integer!")
        # end while loop
        return [str(data), int(nshapes)]  # return nshapes as int



    def create(self):
        shapeInfo = self._getNDataFromKeyboard()
        shapeType = shapeInfo[0]
        nShapes = shapeInfo[1]
        # Case only available after Python 3.10, just use if here
        if shapeType == "Shape":
            pass
        elif shapeType == "Point":
            try:
                x = float(input('Enter the value of X:'))
                y = float(input('Enter the value of Y:'))
                instance = Point(x, y)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Circle":
            try:
                x = float(input('Enter the value of X:'))
                y = float(input('Enter the value of Y:'))
                r = float(input('Enter the value of R:'))
                instance = Circle(x, y, r)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Cylinder":
            try:
                x = float(input('Enter the value of X:'))
                y = float(input('Enter the value of Y:'))
                r = float(input('Enter the value of R:'))
                h = float(input('Enter the value of H:'))
                instance = Cylinder(x, y, r, h)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Sphere":
            try:
                x = float(input('Enter the value of X:'))
                y = float(input('Enter the value of Y:'))
                r = float(input('Enter the value of R:'))
                instance = Sphere(x, y, r)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Rectangle":
            try:
                x = float(input('Enter the value of X:'))
                y = float(input('Enter the value of Y:'))
                instance = Rectangle(x, y)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Square":
            try:
                userInput = float(input('Enter the value of S:'))
                instance = Square(userInput)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")
        elif shapeType == "Cube":
            try:
                userInput = float(input('Enter the value of S:'))
                instance = Cube(userInput)
            except (ValueError, UnboundLocalError):
                print("Not Valid Input")

        while nShapes != 0:
            try:
                temp = copy.deepcopy(instance)
                self._data.append(temp)
                nShapes -= 1

            except ValueError:
                print("Not Valid Input")
                continue

    # Print Menu, If index = "All", Print All, Else, just print the shape at the input index
    def print(self, index="All"):
        if index == "All":
            for each in range(0, len(self._data)):
                print("Index:" + str(each)+
                    "  Shape Name:" + self._data[each].getName() + "Shape Details" + self._data[each].__str__() + "Shape Area:" + str(self._data[each].getArea()) + "Shape Volume:" + str(self._data[each].getVolume()))
        else:
            try:
                index = int(index)
                target = self._data[index]
                print(
                    "Shape Name:" + target.getName() + "Shape Details" + target.__str__() + "Shape Area:" + str(target.getArea()) + "Shape Volume:" + str(target.getVolume()))

            except ValueError:
                print("Not a Valid Input")

    # Remove a shape by index
    def remove(self, index):
        try:
            if int(index) < len(self._data):
                del self._data[index]
        except ValueError:
            print("Please provide a value index")

    # Modify particular shape by Index
    def modify(self, index):
        try:
            index = int(index)
            if int(index) < len(self._data):
                shapeType = self._data[index].getName()
                if shapeType == "Shape":
                    pass
                elif shapeType == "Point":
                    try:
                        x = float(input('Enter the value of X:'))
                        y = float(input('Enter the value of Y:'))
                        self._data[index].setX(x)
                        self._data[index].setY(y)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Circle":
                    try:
                        x = float(input('Enter the value of X:'))
                        y = float(input('Enter the value of Y:'))
                        r = float(input('Enter the value of R:'))
                        self._data[index].setX(x)
                        self._data[index].setY(y)
                        self._data[index].setR(r)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Cylinder":
                    try:
                        x = float(input('Enter the value of X:'))
                        y = float(input('Enter the value of Y:'))
                        r = float(input('Enter the value of R:'))
                        h = float(input('Enter the value of H:'))
                        self._data[index].setX(x)
                        self._data[index].setY(y)
                        self._data[index].setR(r)
                        self._data[index].setH(h)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Sphere":
                    try:
                        x = float(input('Enter the value of X:'))
                        y = float(input('Enter the value of Y:'))
                        r = float(input('Enter the value of R:'))
                        self._data[index].setX(x)
                        self._data[index].setY(y)
                        self._data[index].setR(r)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Rectangle":
                    try:
                        x = float(input('Enter the value of X:'))
                        y = float(input('Enter the value of Y:'))
                        self._data[index].setX(x)
                        self._data[index].setY(y)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Square":
                    try:
                        s = float(input('Enter the value of S:'))
                        self._data[index].setS(s)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
                elif shapeType == "Cube":
                    try:
                        s = float(input('Enter the value of S:'))
                        self._data[index].setS(s)
                    except (ValueError, UnboundLocalError):
                        print("Not Valid Input")
        except ValueError:
            print("Please provide a value index")


def main():
    nmenu = menu()
    nmenu.start()


if __name__ == "__main__":
    main()
