from enums import Country, TeamStatus
from player import Player

class Team:
    def __init__(self, country:Country,players:list[Player]):
        self.country = country
        self.players = players
        self.score = 0
        self.wickets = 0
        self.overs = 0 # Overs bowled
        self.status = None
        self.batter = players[0]
        self.runner = players[0]
        self.bowler = players[-1]
    
    def __str__(self):
        return f'{self.country} has the following players: {", ".join(self.players)}'
    
    def set_status(self,status:TeamStatus):
        self.status = status

    def switch_batter(self):
        self.batter, self.runner = self.runner, self.batter
    
    def switch_bowler(self):
        self.bowler = self.players[]