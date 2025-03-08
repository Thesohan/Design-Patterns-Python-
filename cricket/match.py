from enums import MatchStatus, TossChoice, TeamStatus
from team import Team
import random
from threading import Lock
class Match:

    _instance = None

    def __init__(self,batting_team:Team,bowling_team:Team,max_overs:int=20):

        if Match._instance is not None:
            raise Exception("This class is singleton, Please call get_instance instead.")
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.winner = None
        self.status = MatchStatus.NOT_STARTED
        self.max_overs = max_overs
        self.lock = Lock()


    def get_instance(self,batting_team:Team,bowling_team:Team):
        with self.lock:
            if not hasattr(Match, "_instance"):
                Match._instance = Match(batting_team=batting_team,bowling_team=bowling_team)
        return Match._instance

    def toss(self,choice:TossChoice):
        return random.choice(list(TossChoice.__members__)) == choice

    def handle_bowl_action(self,bowl_action:str):
        if bowl_action == 'W':
            self.batting_team.wickets += 1
            return True
        if bowl_action == 'R':
            run = int(input("Enter the run scored\n"))
            if run == 4:
                self.batting_team.fours += 1
            if run == 6:
                self.batting_team.sixes += 1
            self.batting_team.score += run
            return True
        if bowl_action == 'WD':
            self.batting_team.score += 1
            return False
        if bowl_action == 'NB':
            self.batting_team.score += 1
            self.handle_bowl_action('R')
            return False
        

    def play(self,):
        self.status = MatchStatus.IN_PROGRESS
        while self.bowling_team.overs < self.max_overs:
            # play match bowl by bowl
            valid_bowls = 0
            while valid_bowls < 6:
                bowl_action = input(f"Over: {self.bowling_team.overs} Enter the bowl action: W for wicket, R for run, WD for wide, NB for no ball\n")
                valid_bowl = self.handle_bowl_action(bowl_action)
                if valid_bowl:
                    valid_bowls += 1
                    self.bowling_team.overs += valid_bowls/10
                if self.batting_team.wickets == 10:
                    self.status = MatchStatus.COMPLETED
                    self.winner = self.bowling_team.country
                    break





        self.status = MatchStatus.COMPLETED
