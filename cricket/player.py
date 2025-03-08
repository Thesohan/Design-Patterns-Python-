from enums import Role
class Player:
    def __init__(self,name:str,roles:list[Role]):
        self.name = name
        self.roles = roles
        self.score = 0
        self.wickets = 0
        self.ball_faced = 0
        self.ball_bowled = 0
        self.fours = 0
        self.sixes = 0
        self.double = 0
        self.triple = 0
        self.strike_rate = 0
        self.economy = 0
        self.out = False

    def __str__(self):
        return f'{self.name} - {" & ".join(self.roles)}'
    
