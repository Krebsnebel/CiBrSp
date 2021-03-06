from random import shuffle, randrange

from CivEnums.EBuilding import EBuilding
from CivEnums.EGreatPerson import EGreatPerson
from CivEnums.ERotation import ERotation
from CivEnums.EWonder import EWonder
from CivObjects.Building import Building
from CivObjects.DisasterMarker import DisasterMarker
from CivObjects.GreatPerson import GreatPerson
from CivObjects.Position import Position
from CivObjects.Wonder import Wonder
from Drawing.EImageObject import EImageObject


"""
this class is a collection of business objects on market map
stacks of marina, tradingPost, blacksmith, library, granary, market, temple, barrack, greatPerson, city, 
disaster, wonderVisible, wonderCovered_L2, wonderCovered_L3 are collected and - if necessary - shuffled here
depending of move of each player business objects can be lifted off the stacks
there is a function to draw the stacks on market place
"""


def drawStack(window, resize, stack, imgInfo, imgObj, s):
    i = 0
    stackPos = imgInfo.getImgPosOf(imgObj)
    for obj in stack:
        pos = Position(stackPos.getX() + i, stackPos.getY() - i)
        obj.draw(window, ERotation.NO_ROTATION, pos, resize)
        i = i + s


class BusinessObjectCollection:

    def __init__(self, imgInfoMarketMap):
        self.imgInfo = imgInfoMarketMap
        self.marina = []
        self.tradingPost = []
        self.blacksmith = []
        self.library = []
        self.granary = []
        self.market = []
        self.temple = []
        self.barrack = []
        self.greatPerson = []
        self.city = []
        self.disaster = []
        self.wonderVisible = []
        self.wonderCovered_L2 = []
        self.wonderCovered_L3 = []

        for i in range(3):
            self.greatPerson.append(GreatPerson(EGreatPerson.ARTIST))
            self.greatPerson.append(GreatPerson(EGreatPerson.BUILDER))
            self.greatPerson.append(GreatPerson(EGreatPerson.GENERAL))
            self.greatPerson.append(GreatPerson(EGreatPerson.HUMANITARIAN))
            self.greatPerson.append(GreatPerson(EGreatPerson.INDUSTRIALIST))
            self.greatPerson.append(GreatPerson(EGreatPerson.SCIENTIST))

        for i in range(5):
            self.market.append(Building(EBuilding.MARKET))
            self.temple.append(Building(EBuilding.TEMPLE))
            self.barrack.append(Building(EBuilding.BARRACK))

        for i in range(6):
            self.tradingPost.append(Building(EBuilding.TRADING_POST))
            self.blacksmith.append(Building(EBuilding.BLACKSMITH))
            self.library.append(Building(EBuilding.LIBRARY))
            self.granary.append(Building(EBuilding.GRANARY))

        for i in range(10):
            self.marina.append(Building(EBuilding.MARINA))

        for i in range(12):
            self.disaster.append(DisasterMarker())

        # level 1
        self.wonderVisible.append(Wonder(EWonder.STONEHENGE))
        self.wonderVisible.append(Wonder(EWonder.THE_HANGING_GARDENS))
        self.wonderVisible.append(Wonder(EWonder.THE_COLOSSUS))
        self.wonderVisible.append(Wonder(EWonder.THE_ORACLE))
        for w in self.wonderVisible:
            w.isVisible()

        shuffle(self.wonderVisible)

        # level 2
        self.wonderCovered_L2.append(Wonder(EWonder.THE_LOUVRE))
        self.wonderCovered_L2.append(Wonder(EWonder.CASTLE_HIMEJI))
        self.wonderCovered_L2.append(Wonder(EWonder.ANGKOR_WAT))
        self.wonderCovered_L2.append(Wonder(EWonder.PORCELAIN_TOWER))
        shuffle(self.wonderCovered_L2)

        # level 2
        self.wonderCovered_L3.append(Wonder(EWonder.PANAMA_CANAL))
        self.wonderCovered_L3.append(Wonder(EWonder.OPERA_HOUSE_OF_SIDNEY))
        self.wonderCovered_L3.append(Wonder(EWonder.STATUE_OF_LIBERTY))
        self.wonderCovered_L3.append(Wonder(EWonder.UNITED_NATIONS))
        shuffle(self.wonderCovered_L3)

    def popWonder(self, idx):
        if 0 <= idx < len(self.wonderVisible):
            w = self.wonderVisible.pop(idx)
            if len(self.wonderCovered_L2) > 0:
                n = self.wonderCovered_L2.pop(0)
                n.isVisible()
                self.wonderVisible.insert(idx, n)
            elif len(self.wonderCovered_L3) > 0:
                n = self.wonderCovered_L3.pop(0)
                n.isVisible()
                self.wonderVisible.insert(idx, n)
            return w
        return None

    def popGreatPerson(self):
        idx = randrange(len(self.greatPerson))
        if 0 <= idx < len(self.greatPerson):
            return self.greatPerson.pop(idx)
        return None

    def draw(self, window):
        resizeCard = self.imgInfo.getResize(EImageObject.WONDER_CARD)
        resizeMarker = self.imgInfo.getResize(EImageObject.SQUARE_OBJECT)

        delta = 2
        drawStack(window, resizeMarker, self.market, self.imgInfo, EImageObject.BUILDING_STACK_1L, delta)
        drawStack(window, resizeMarker, self.temple, self.imgInfo, EImageObject.BUILDING_STACK_1R, delta)
        drawStack(window, resizeMarker, self.granary, self.imgInfo, EImageObject.BUILDING_STACK_2L, delta)
        drawStack(window, resizeMarker, self.library, self.imgInfo, EImageObject.BUILDING_STACK_2R, delta)
        drawStack(window, resizeMarker, self.barrack, self.imgInfo, EImageObject.BUILDING_STACK_3L, delta)
        drawStack(window, resizeMarker, self.blacksmith, self.imgInfo, EImageObject.BUILDING_STACK_3R, delta)
        drawStack(window, resizeMarker, self.tradingPost, self.imgInfo, EImageObject.BUILDING_STACK_4L, delta)
        drawStack(window, resizeMarker, self.marina, self.imgInfo, EImageObject.BUILDING_STACK_4R, delta)

        i = 0
        for w in self.wonderVisible:
            if i == 0:
                cardObj = EImageObject.WONDER_CARD_POS_1
                markerObj = EImageObject.WONDER_MARKER_POS_1
            elif i == 1:
                cardObj = EImageObject.WONDER_CARD_POS_2
                markerObj = EImageObject.WONDER_MARKER_POS_2
            elif i == 2:
                cardObj = EImageObject.WONDER_CARD_POS_3
                markerObj = EImageObject.WONDER_MARKER_POS_3
            else:   # i == 3
                cardObj = EImageObject.WONDER_CARD_POS_4
                markerObj = EImageObject.WONDER_MARKER_POS_4
            pos = self.imgInfo.getImgPosOf(markerObj)
            w.draw(window, ERotation.CLOCKWISE_90, pos, resizeMarker)
            pos = self.imgInfo.getImgPosOf(cardObj)
            w.drawCard(window, ERotation.NO_ROTATION, pos, resizeCard)
            i = i + 1

        d = 0
        stackPos = self.imgInfo.getImgPosOf(EImageObject.WONDER_STACK)
        for w in self.wonderCovered_L3:
            pos = Position(stackPos.getX() + d, stackPos.getY() - d)
            w.drawCard(window, ERotation.NO_ROTATION, pos, resizeCard)
            d = d + 2

        for w in self.wonderCovered_L2:
            pos = Position(stackPos.getX() + d, stackPos.getY() - d)
            w.drawCard(window, ERotation.NO_ROTATION, pos, resizeCard)
            d = d + 2
