from enums import Country, Role,TeamStatus
from team import Team
from player import Player
from match import Match

if __name__ == '__main__':
    players = [Player('Sachin', [Role.BATTER]), Player('Kohli', [Role.BATTER]),Player('Dhoni', [Role.WICKET_KEEPER,Role.CAPTAIN])]
    team_india = Team(Country.INIDA,players=players)

    players =[Player('Babar', [Role.BATTER]), Player('Harish', [Role.BATTER]),Player('Rizwan', [Role.WICKET_KEEPER,Role.CAPTAIN])]
    team_pak = Team(Country.PAKISTAN,players=players)
    
    match = Match(team_a=team_india,team_b=team_pak,max_overs=1)
    choice = input("Welcome to India vs Pakistan match. It's toss time, let's see who wins the toss, Enter H for Head and T for Tail, You are supporting India!\n")
    if match.toss(choice=choice):
        print("India won the toss")
        team_india.set_status(TeamStatus.Battiing)
        team_pak.set_status(TeamStatus.Bowling)
        
    else:
        team_pak.set_status(TeamStatus.Battiing)
        team_india.set_status(TeamStatus.Bowling)
        print("Pakistan won the toss")
    print(f"Players in {team_india.country} are {[str(player) for player in team_india.players]}")
    print(f"Players in {team_pak.country} are {[str(player) for player in team_pak.players]}")
    print(f"Match status: {match.status}")

    match.play()
    print(f"Match winner: {match.winner}")


