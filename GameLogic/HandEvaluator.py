from typing import List, Any

from Common.VariableDefinitions import *
from itertools import combinations

# self.cardNumbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
# self.cardNumbersEvaluation = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# self.cardColors = ['♡', '♤', '♧', '♢']
# self.cardColorsEvaluation = ['heart', 'spade', 'club', 'diamond']

# ROYAL_FLUSH_RANK = 1
# STRAIGHT_FLUSH_RANK = 2
# QUADS_RANK = 3
# FULL_HOUSE_RANK = 4
# FLUSH_RANK = 5
# STRAIGHT_RANK = 6
# TRIPS_RANK = 7
# TWO_PAIRS_RANK = 8
# PAIR_RANK = 9
# HIGH_CARD_RANK = 10
#
# ROYAL_FLUSH_DESCRIPTION = "royal flush"
# STRAIGHT_FLUSH_DESCRIPTION = "straight flush"
# QUADS_DESCRIPTION = "quads"
# FULL_HOUSE_DESCRIPTION = "full house"
# FLUSH_DESCRIPTION = "flush"
# STRAIGHT_DESCRIPTION = "straight"
# TRIPS_DESCRIPTION = "trips"
# TWO_PAIRS_DESCRIPTION = "two pair"
# PAIR_DESCRIPTION = "pair"
# HIGH_CARD_DESCRIPTION = "high card"
from Common.VariableDefinitions import A_NUMBER


class HandEvaluator:

    def __init__(self, cardsToEvaluate, playerID):
        self.cardsToEvaluate = cardsToEvaluate
        self.playerID = playerID
        self.handResult = []  # ["description", rank, tuple_with_combination_of_cards, playerID]

    def evaluteHand(self):
        self.checkFor5CardsCombination()
        return self.handResult

    @staticmethod
    def higherFullHouse(fullNew, fullOld):  # check if fullNew is bigger than fullOld - 0 false, 1 true, 2 equal
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in fullNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in fullOld]
        numbersNew.sort()
        numbersOld.sort()
        if numbersNew == numbersOld:
            return 2

        tripsNew = 0
        pairNew = 0
        tripsOld = 0
        pairOld = 0

        for index in range(2):  # a full house has only 2 values
            if numbersNew.count(list(set(numbersNew))[index]) == 3:  # the big part from a full house
                tripsNew = list(set(numbersNew))[index]
            else:
                pairNew = list(set(numbersNew))[index]

            if numbersOld.count(list(set(numbersOld))[index]) == 3:  # the big part from a full house
                tripsOld = list(set(numbersOld))[index]
            else:
                pairOld = list(set(numbersOld))[index]

        if tripsNew > tripsOld:
            return 1
        elif tripsNew < tripsOld:
            return 0
        else:
            if pairNew > pairOld:
                return 1
            elif pairNew < pairOld:
                return 0

    @staticmethod
    def higherStraight(stNew, stOld):  # check if stNew is bigger than stOld
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in stNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in stOld]
        numbersNew.sort()
        numbersOld.sort()
        if numbersNew == numbersOld:
            return 2

        if max(numbersNew) != A_NUMBER and max(numbersOld) != A_NUMBER:
            if max(numbersNew) > max(numbersOld):
                return 1
            elif max(numbersNew) < max(numbersOld):
                return 0
        elif max(numbersNew) == A_NUMBER and max(numbersOld) == A_NUMBER:
            if min(numbersNew) > min(numbersOld):
                return 1
            elif min(numbersNew) < min(numbersOld):
                return 0
        elif max(numbersNew) == A_NUMBER and max(numbersOld) != A_NUMBER:
            if min(numbersNew) <= min(numbersOld):
                return 0
            else:
                return 1
        elif max(numbersNew) != A_NUMBER and max(numbersOld) == A_NUMBER:
            if min(numbersNew) >= min(numbersOld):
                return 1
            else:
                return 0

    @staticmethod
    def higherTwoPairs(twoPairNew, twoPairOld):  # if new is higher than old. 1 true, 0 false, 2 equal
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in twoPairNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in twoPairOld]
        numbersNew.sort()
        numbersOld.sort()
        if numbersNew == numbersOld:
            return 2

        pair1New = 0
        pair2New = 0
        highCardNew = 0

        pair1Old = 0
        pair2Old = 0
        highCardOld = 0

        for index in range(3):
            if numbersNew.count(list(set(numbersNew))[index]) == 2:  # pair
                if pair1New == 0:
                    pair1New = list(set(numbersNew))[index]
                else:
                    pair2New = list(set(numbersNew))[index]
            else:
                highCardNew = list(set(numbersNew))[index]

            if numbersOld.count(list(set(numbersOld))[index]) == 2:  # pair
                if pair1Old == 0:
                    pair1Old = list(set(numbersOld))[index]
                else:
                    pair2Old = list(set(numbersOld))[index]
            else:
                highCardOld = list(set(numbersOld))[index]

        if max([pair1New, pair2New]) > max([pair1Old, pair2Old]):
            return 1
        elif max([pair1New, pair2New]) < max([pair1Old, pair2Old]):
            return 0
        else:
            if min([pair1New, pair2New]) > min([pair1Old, pair2Old]):
                return 1
            elif min([pair1New, pair2New]) > min([pair1Old, pair2Old]):
                return 0
            else:
                if highCardNew > highCardOld:
                    return 1
                elif highCardNew < highCardOld:
                    return 0

    @staticmethod
    def higherTrips(trNew, trOld):
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in trNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in trOld]
        numbersNew.sort()
        numbersOld.sort()
        if numbersNew == numbersOld:
            return 2

        tripsNew = 0
        highCard1New = 0
        highCard2New = 0

        tripsOld = 0
        highCard1Old = 0
        highCard2Old = 0

        for index in range(3):
            if numbersNew.count(list(set(numbersNew))[index]) == 3:
                tripsNew = list(set(numbersNew))[index]
            else:
                if highCard1New == 0:
                    highCard1New = list(set(numbersNew))[index]
                else:
                    highCard2New = list(set(numbersNew))[index]

            if numbersNew.count(list(set(numbersNew))[index]) == 3:
                tripsNew = list(set(numbersNew))[index]
            else:
                if highCard1Old == 0:
                    highCard1Old = list(set(numbersOld))[index]
                else:
                    highCard2Old = list(set(numbersOld))[index]

        if tripsNew > tripsOld:
            return 1
        elif tripsNew < tripsOld:
            return 0
        else:
            if max([highCard1New, highCard2New]) > max([highCard1Old, highCard2Old]):
                return 1
            elif max([highCard1New, highCard2New]) < max([highCard1Old, highCard2Old]):
                return 0
            else:
                if min([highCard1New, highCard2New]) > min([highCard1Old, highCard2Old]):
                    return 1
                elif min([highCard1New, highCard2New]) < min([highCard1Old, highCard2Old]):
                    return 0

    @staticmethod
    def higherPair(pairNew, PairOld):
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in pairNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in PairOld]
        numbersNew.sort()
        numbersOld.sort()
        if numbersNew == numbersOld:
            return 2

        pairNew = 0
        highCardNew = []

        pairOld = 0
        highCardOld = []

        for index in range(4):  # 4 = one pair + 3 high cards
            if numbersNew.count(list(set(numbersNew))[index]) == 2:
                pairNew = list(set(numbersNew))[index]
            else:
                highCardNew.append(list(set(numbersNew))[index])

            if numbersOld.count(list(set(numbersOld))[index]) == 2:
                pairOld = list(set(numbersOld))[index]
            else:
                highCardOld.append(list(set(numbersOld))[index])

        highCardNew.sort()
        highCardOld.sort()

        if pairNew > pairOld:
            return 1
        elif pairNew < pairOld:
            return 0
        else:
            if highCardNew > highCardOld:
                return 1
            else:
                return 0

    @staticmethod
    def higherCard(highCardNew, highCardOld):
        numbersNew = [x[NUMBER_INDEX_TUPLE] for x in highCardNew]
        numbersOld = [x[NUMBER_INDEX_TUPLE] for x in highCardOld]
        numbersNew.sort()
        numbersOld.sort()

        if numbersNew > numbersOld:
            return 1
        if numbersNew < numbersOld:
            return 0
        else:
            return 2

    def checkFor5CardsCombination(self):  # royal flush, straight flush, straight, flush, full house?
        listOfStraight = 0
        listOfStraightFlush = 0
        listOfFullHouse = 0
        listOfFlush = 0
        listOfRoyalFlush = 0
        listOfQuads = 0
        listOfTrips = 0
        listOfTwoPair = 0
        listOfPair = 0
        listOfHighCard = 0
        comb5 = list(combinations(self.cardsToEvaluate, 5))
        for comb in comb5:
            listOfNumbers: List[Any] = [x[NUMBER_INDEX_TUPLE] for x in comb]
            listOfColors = [x[COLOR_INDEX_TUPLE] for x in comb]
            if (sorted(listOfNumbers) == list(range(min(listOfNumbers), max(listOfNumbers) + 1))) or (
                    sorted(listOfNumbers) == SMALL_STRAIGHT):  # if straight
                if len(set(listOfColors)) == 1:  # if all colors are the same
                    if max(listOfNumbers) == A_NUMBER:  # if A is max
                        listOfRoyalFlush = comb
                    elif listOfStraightFlush == 0 or self.higherStraight(comb, listOfStraightFlush) == 1:
                        listOfStraightFlush = comb
                elif listOfStraight == 0 or self.higherStraight(comb, listOfStraight) == 1:
                    listOfStraight = comb
            elif len(set(listOfNumbers)) == 2:  # if are only 2 numbers means that is full house or quads
                if (listOfNumbers.count(list(set(listOfNumbers))[0]) != NUMBER_OF_CARDS_FOR_QUADS) and (
                        listOfNumbers.count(list(set(listOfNumbers))[1]) != NUMBER_OF_CARDS_FOR_QUADS):
                    if listOfFullHouse == 0 or self.higherFullHouse(comb, listOfFullHouse):
                        listOfFullHouse = comb
                else:
                    listOfQuads = comb
            elif len(set(listOfColors)) == 1:
                if listOfFlush == 0 or (max(listOfNumbers) > max([x[NUMBER_INDEX_TUPLE] for x in listOfFlush])):
                    listOfFlush = comb
            elif len(set(listOfNumbers)) == 3:  # if are only 3 numbers means that is trips or two pairs
                if (listOfNumbers.count(list(set(listOfNumbers))[0]) != NUMBER_OF_CARDS_FOR_TRIPS) and (
                        listOfNumbers.count(list(set(listOfNumbers))[1]) != NUMBER_OF_CARDS_FOR_TRIPS) and (
                        listOfNumbers.count(list(set(listOfNumbers))[2]) != NUMBER_OF_CARDS_FOR_TRIPS):
                    if listOfTwoPair == 0 or self.higherTwoPairs(comb, listOfTwoPair) == 1:
                        listOfTwoPair = comb
                elif listOfTrips == 0 or self.higherTrips(comb, listOfTrips) == 1:
                    listOfTrips = comb
            elif len(set(listOfNumbers)) == 4:  # if are 4 numbers means that there is a pair with three high cards
                if listOfPair == 0 or self.higherPair(comb, listOfPair) == 1:
                    listOfPair = comb
            elif len(set(listOfNumbers)) == 5:  # if are 5 numbers means that the hand is high card
                if listOfHighCard == 0 or self.higherCard(comb, listOfHighCard) == 1:
                    listOfHighCard = comb

        if listOfRoyalFlush != 0:
            self.handResult = [ROYAL_FLUSH_DESCRIPTION, ROYAL_FLUSH_RANK, listOfRoyalFlush, self.playerID]
        elif listOfStraightFlush != 0:
            self.handResult = [STRAIGHT_FLUSH_DESCRIPTION, STRAIGHT_FLUSH_RANK, listOfStraightFlush, self.playerID]
        elif listOfQuads != 0:
            self.handResult = [QUADS_DESCRIPTION, QUADS_RANK, listOfQuads, self.playerID]
        elif listOfFullHouse != 0:
            self.handResult = [FULL_HOUSE_DESCRIPTION, FULL_HOUSE_RANK, listOfFullHouse, self.playerID]
        elif listOfStraight != 0:
            self.handResult = [STRAIGHT_DESCRIPTION, STRAIGHT_RANK, listOfStraight, self.playerID]
        elif listOfFlush != 0:
            self.handResult = [FLUSH_DESCRIPTION, FLUSH_RANK, listOfFlush, self.playerID]
        elif listOfTrips != 0:
            self.handResult = [TRIPS_DESCRIPTION, TRIPS_RANK, listOfTrips, self.playerID]
        elif listOfTwoPair != 0:
            self.handResult = [TWO_PAIRS_DESCRIPTION, TWO_PAIRS_RANK, listOfTwoPair, self.playerID]
        elif listOfPair != 0:
            self.handResult = [PAIR_DESCRIPTION, PAIR_RANK, listOfPair, self.playerID]
        elif listOfHighCard != 0:
            self.handResult = [HIGH_CARD_DESCRIPTION, HIGH_CARD_RANK, listOfHighCard, self.playerID]
