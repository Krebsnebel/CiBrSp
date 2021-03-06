from CivEnums.ECivilization import ECivilization
from CivEnums.EFigure import EFigure
from CivEnums.ERotation import ERotation
from CivObjects.BusinessObject import BusinessObject
from CivObjects.Position import Position


"""
class Square inherits by BusinessObject
with it all properties of each square can be defined
* trading points
* production points
* culture points
* defence points
* resource
* terrain, name and sign
* position
* bonus (for additional culture point)
* additional note (e.g. for barbarian or cottage)
* object on square
** businessObject
** marker
** city
** disaster marker
* list of armies
* list of pioneers
* and its civilization
"""


class Square(BusinessObject):

    def __init__(self, terr, res, bon, note):
        tp = terr.getTradingPoints()
        pp = terr.getProductionPoints()
        if bon:
            cp = 1
        else:
            cp = 0
        dp = 0
        s = terr.getSign()
        super().__init__(tp, pp, cp, dp, res, s)
        self.position = None
        self.terrain = terr
        self.bonus = bon
        self.note = note
        self.businessObject = None
        self.marker = None
        self.city = None
        self.disasterMarker = None
        self.figureCiv = ECivilization.NONE
        self.army = []
        self.pioneer = []

    def countTradingPoints(self, civ):
        for a in self.army:
            if a.getCivilization() is not civ:
                return 0

        for p in self.pioneer:
            if p.getCivilization() is not civ:
                return 0

        if self.businessObject is not None:
            return self.businessObject.getTradingPoints()

        if self.disasterMarker is not None:
            return self.disasterMarker.getTradingPoints()

        return self.getTradingPoints()

    def drawObjectsOfSquare(self, window, imgInfo):
        pos = imgInfo.getImgPosOfSquare(self.position)
        resize = imgInfo.getResizeSquareObj() * imgInfo.getScale()
        if self.businessObject is not None:
            self.businessObject.draw(window, ERotation.NO_ROTATION, pos, resize)
        if self.city is not None:
            self.city.draw(window, ERotation.NO_ROTATION, pos, resize)
        if self.disasterMarker is not None:
            self.disasterMarker.draw(window, ERotation.NO_ROTATION, pos, resize)
        for a in self.army:
            a.draw(window, ERotation.NO_ROTATION, pos, resize)
        for p in self.pioneer:
            p.draw(window, ERotation.NO_ROTATION, pos, resize)

    def getDisasterMarker(self):
        return self.disasterMarker

    def setDisasterMarker(self, disaster):
        self.disasterMarker = disaster

    def getCivOfFigures(self):
        return self.figureCiv

    def setFigures(self, figures):
        if figures is None or len(figures) == 0:
            print("keine gültige Figurenübergabe bei Funktion setFigures()")
            return False
        civ = figures[0].getCivilization()
        for f in figures:
            if civ is not f.getCivilization():
                print("Figuren verschiedner Civilisationen - figures")
                return False
        if (len(self.army) > 0 or len(self.pioneer) > 0) and self.figureCiv is not civ:
            print("Auf einem Feld dürfen nicht Figuren verschiedner Civilisationen")
            return False
        self.figureCiv = civ
        for f in figures:
            f.setPosition(self.position.getX(), self.position.getY())
            if f.getType() == EFigure.PIONEER:
                self.pioneer.append(f)
            elif f.getType() == EFigure.ARMY:
                self.army.append(f)
            else:
                print("Diese Figurenart gibt es nicht")
                return False
        return True

    def getArmies(self):
        return self.army

    def getPioneers(self):
        return self.pioneer

    def getMarker(self):
        return self.marker

    def getTerrain(self):
        return self.terrain

    def printLineOfSquare(self, row):
        if row == 0:
            str_tp = str(self.evalTradingPoints())
            str_a = str(0)
            str_r = str(self.evalResource())
            print(str_tp + str_a + str_r + "|", end="")
        elif row == 1:
            str_pio = str(0)
            str_o = self.getObjectType()
            str_r = str(self.evalDefencePoints())
            print(str_pio + str_o + str_r + "|", end="")
        elif row == 2:
            str_pio = str(0)
            str_o = str(0)
            str_r = str(0)
            print(str_pio + str_o + str_r + "_", end="")

    def setPosition(self, x, y):
        if self.position is None:
            self.position = Position(x, y)
        else:
            self.position.setPosition(x, y)

    def getPosition(self):
        return self.position

    def getBusinessObject(self):
        return self.businessObject

    def setBusinessObject(self, obj):
        self.businessObject = obj

    def getCity(self):
        return self.city

    def setCity(self, city):
        self.city = city
        self.city.setPosition(self.position.getX(), self.position.getY())

    def evalTradingPoints(self):
        if self.businessObject is not None:
            return self.businessObject.getTradingPoints()
        else:
            return self.getTradingPoints()

    def evalResource(self):
        if self.businessObject is not None:
            return self.businessObject.getResource().getSign()
        else:
            return self.getResource().getSign()

    def getObjectType(self):
        if self.marker is not None:
            return self.marker.getSign()
        elif self.businessObject is not None:
            return self.businessObject.getSign()
        elif self.city is not None:
            return self.city.getSign()
        else:
            return self.getSign()

    def evalDefencePoints(self):
        if self.businessObject is not None:
            return self.businessObject.getDefencePoints()
        else:
            return self.getDefencePoints()

