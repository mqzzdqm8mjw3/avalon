r"""
    avalon.py - for Python 3, to be run on repl.it
"""

import random

__author__ = 'mqzzdqm8mjw3'

NEVIL = { 5 : 2, 6 : 2, 7 : 3, 8 : 3, 9 : 3, 10 : 3 }


class Character(object):
    def __init__(self, name, player, side, description):
        self._name        = name
        self._player      = player
        self._side        = side
        self._description = description

class Game(object):

    def __init__(self, players, seed=42):
        self._seed    = random.seed(seed)

        self._n       = len(players)
        self._players = random.sample(players, self._n)
        self._nEvil   = NEVIL[self._n]
        self._knownToMerlin = self._players[:self._nEvil]
        self._knownToEvil   = self._players[:self._nEvil]
        self._nOptEvil      = 0

        self._assignments = {self._players[-1] : "Merlin", 
                             self._players[0] : "the Assassin"}
        self._characters  = {'Merlin' : Character("Merlin",
            self._players[-1], "Good",
            "You know the agents of Evil, but you must speak of this only in riddle. If your true identity is discovered, all will be lost."),
                            'the Assassin': Character("the Assassin",
            self._players[0], "Evil",
            "You have an additional evil objective: identify and assassinate Merlin at the end of the game.")}

        self._knownToPercival = [self._players[-1]]


    def addCharacter(self, character):
        if character == 'Percival':
            self._addPercival()
            return
        elif (character in ['Mordred', 'Oberon', 'Morgana']) and \
             (character not in self._characters) and \
             (self._nOptEvil < self._nEvil-1):
            if character == 'Mordred':
                self._addMordred()
            elif character == 'Oberon':
                self._addOberon()
            elif character == 'Morgana':
                self._addMorgana()
            return
        else:
            print("Error adding character. %s not added." % character)
            return

    def _addPercival(self):
        p = self._players[self._nEvil]
        self._assignments[p] = 'Percival'
        self._characters['Percival'] = Character("Percival", p, "Good",
            "Your special power is knowledge of Merlin at the start of the game. You must use your knowledge wisely to protect Merlin's identity.")
        return

    def _addMordred(self):
        p = self._players[self._nOptEvil+1]
        self._assignments[p] = 'Mordred'
        self._characters['Mordred'] = Character("Mordred", p, "Evil",
            "Your special power is that your identity is not revealed to Merlin at the start of the game.")
        self._knownToMerlin.remove(p)
        self._knownToMerlin.append('Mordred (identity unknown)')
        self._nOptEvil += 1
        return

    def _addOberon(self):
        p = self._players[self._nOptEvil+1]
        self._assignments[p] = 'Oberon'
        self._characters['Oberon'] = Character("Oberon", p, "Evil",
            "You are not revealed to other Evil players, nor do you know which players are Evil at the start of the game.")
        #self._knownToMerlin.remove(p)
        self._knownToEvil.remove(p)
        #self._knownToMerlin.append('Oberon (identity unknown)')
        self._knownToEvil.append('Oberon (identity unknown)')
        self._nOptEvil += 1
        return

    def _addMorgana(self):
        p = self._players[self._nOptEvil+1]
        self._assignments[p] = 'Morgana'
        self._characters['Morgana'] = Character("Morgana", p, "Evil",
            "You appear to Percival as Merlin.")
        self._knownToPercival.append(p)
        self._nOptEvil += 1

    def _addLoyalServant(self, p):
        self._assignments[p] = 'a Loyal Servant of Arthur'
        if 'a Loyal Servant of Arthur' in self._characters:
            self._characters['a Loyal Servant of Arthur']._player.append(p)
        else:
            self._characters['a Loyal Servant of Arthur'] = Character(
                "a Loyal Servant of Arthur", [p], "Good", "")
        return

    def _addMinion(self, p):
        self._assignments[p] = 'a Minion of Mordred'
        if 'a Minion of Mordred' in self._characters:
            self._characters['a Minion of Mordred']._player.append(p)
        else:
            self._characters['a Minion of Mordred'] = Character(
                "a Minion of Mordred", [p], "Evil", "")
        return

    def assignRemainingCharacters(self):
        for p in self._players[self._nOptEvil+1:self._nEvil]:
            self._addMinion(p)
        for p in self._players[len(self._assignments)-1:-1]:
            self._addLoyalServant(p)

    def getAssignment(self, player):
        return self._assignments[player]

    def printInfo(self, assignment):
        side       = self._characters[assignment]._side
        print("\tYou are %s, on the side of %s." % (assignment, side))
        print('\t'+self._characters[assignment]._description)
        return

    def printKnowledge(self, character):
        if character == 'Merlin':
            print("\tYou know the following players are Evil: " + \
                  ', '.join(self._knownToMerlin))
        elif character in ['the Assassin', 'a Minion of Mordred', \
                         'Mordred', 'Morgana']:
            print("\tYou know the following players are Evil: " + \
                  ', '.join(self._knownToEvil))
        elif character == 'Percival':
            print("\tMerlin is (one of) the following player(s): " + \
                  ', '.join(self._knownToPercival))
        return


    def printLeaders(self):
        leaders = random.sample(self._players, self._n)
        print("\nTeam Leaders: " + ", ".join(leaders))
        return


def main():

    ###
    #
    # CHANGE ONLY THE FOLLOWING LINES TO INITIALIZE A NEW GAME
    #     - List all players in the list PLAYERS, like the example.
    #     - Select a random number for SEED. (e.g., random.org)
    #     - List all additional characters you wish to use (e.g.,
    #       'Percival', 'Mordred', 'Oberon', 'Morgana')
    #
    ####

    PLAYERS = ['Ai', 'Lisa', 'mQ', 'Natalie', 'Seiran']
    SEED    = 1
    ADDCHAR = []

    ###
    #
    # DO NOT CHANGE ANYTHING BELOW THIS LINE
    #
    ###
    
    print("Players: " + ', '.join(PLAYERS))
    
    query = input("Enter your name:").strip().lower()

    # set-up game    
    g = Game([p.lower() for p in PLAYERS], seed=SEED)
    for ch in ADDCHAR:
        g.addCharacter(ch)
    g.assignRemainingCharacters()

    # print player info
    assignment = g.getAssignment(query)
    g.printInfo(assignment)
    g.printKnowledge(assignment)
    g.printLeaders()


if __name__ == '__main__':
    main()
    
# for repl.it
main()
