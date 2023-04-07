import random


class Player:
    def __init__(self):
        self.hearts = 5
        self.trophies = 0


class Game:
    def __init__(self, num_players):

        self.round = 0

        self.players = []

        self.matches = 0

        for i in range(num_players):
            player = Player()
            self.players.append(player)

        self.victors = []

        self.losers = []

    def checkForWinners(self):
        """
        Check for winners after a round (winner: Player who got to 10 trophies), move them to the winners' list and remove from active players
        """

        for index, player in enumerate(self.players):
            if player.trophies == 10:

                self.victors.append(player)

                self.players[index] = None
        
        self.players = list(filter(lambda player: player is not None, self.players))
        
    def checkForLosers(self):
        """
        Check for losers after a round (loser: Player who lost all his hearts), move them to the losers' list and remove from active players
        """

        for index, player in enumerate(self.players):
            if player.hearts == 0:

                self.losers.append(player)

                self.players[index] = None

        self.players = list(filter(lambda player: player is not None, self.players))



    def simulateRound(self):
        """
        Simulate one round of a game. Altough the real game is asynchronous, i think this model might be more or less accurate.
        And yes, i don't have draws, i think they don't really change the overall distribution this much.
        """

        # first, group all players:

        groups = []

        for hearts in range(0, 5):
            groups.append([])

            for trophies in range(0, 10):
                groups[hearts].append([])


        for player in self.players:
            groups[player.hearts - 1][player.trophies].append(player)

        # now players are grouped first by hearts and then by trophies (because i now said so that this is how i match make here (i think it matched the original))


        # next step is to make the internal groups play against each other:

        # this is a group for when the players inside group have an odd amount, so the battles must be held outside their group for those players.
        # this are a maximum of 1 per group so with 5 different heart levels and 10 different trophy levels, there are a maximum of 50 players for this
        rest = []

        for heartGroup in groups:
            for trophyGroup in heartGroup:
                returner = self.simulateGroup(trophyGroup)
                if returner != None:
                    rest.append(returner)

        if (len(rest) % 2) == 1:
            randInt = random.randint(0, 1)
            if randInt == 1:
                rest[0].trophies += 1
            else:
                rest[0].hearts -= 1

            rest.pop(0)

        while rest != []:
            player1 = rest.pop()
            player2 = rest.pop()

            match = [player1, player2]

            randInt = random.randint(0, 1)

            winner = match[randInt]
            loser = match[randInt - 1]

            winner.trophies += 1
            loser.hearts -= 1

            self.matches += 1



    def simulateGroup(self, group):
        returner = None

        # if odd players in group, return first player to play against players from other groups
        if (len(group) % 2) == 1:
            returner = group[0]
            group = group[1:]

        while group != []:
            player1 = group.pop()
            player2 = group.pop()

            match = [player1, player2]

            randInt = random.randint(0, 1)

            winner = match[randInt]
            loser = match[randInt - 1]

            winner.trophies += 1
            loser.hearts -= 1

            self.matches += 1
        
        return(returner)

    
    def play(self):
        while len(self.players) > 1:

            self.round += 1

            # simulate healing after turn 2
            if self.round == 3:
                for player in self.players:
                    if player.hearts < 5:
                        player.hearts += 1

            self.checkForLosers()
            self.checkForWinners()

            self.simulateRound()

        print("Game ended on Round " + str(self.round) + "\n\n")

        print("Victors: " + str(len(self.victors)) + "\n")
        print("\n\nLosers: " + str(len(self.losers)) + "\n")

        print("Matches played:", self.matches)

        print("Lost with 0 trophies:", len(list(filter(lambda player: player.trophies == 0, self.losers))))
        print("Lost with 1 trophies:", len(list(filter(lambda player: player.trophies == 1, self.losers))))
        print("Lost with 2 trophies:", len(list(filter(lambda player: player.trophies == 2, self.losers))))
        print("Lost with 3 trophies:", len(list(filter(lambda player: player.trophies == 3, self.losers))))
        print("Lost with 4 trophies:", len(list(filter(lambda player: player.trophies == 4, self.losers))))
        print("Lost with 5 trophies:", len(list(filter(lambda player: player.trophies == 5, self.losers))))
        print("Lost with 6 trophies:", len(list(filter(lambda player: player.trophies == 6, self.losers))))
        print("Lost with 7 trophies:", len(list(filter(lambda player: player.trophies == 7, self.losers))))
        print("Lost with 8 trophies:", len(list(filter(lambda player: player.trophies == 8, self.losers))))
        print("Lost with 9 trophies:", len(list(filter(lambda player: player.trophies == 9, self.losers))))

        print("Remaining Players (always 0 or 1): ", self.players)
        



newGame = Game(100000)

newGame.play()