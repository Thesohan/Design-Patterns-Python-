from enum import StrEnum


class Country(StrEnum):
    INIDA = "India"
    AUSTRALIA = "Australia"
    ENGLAND = "England"
    SOUTH_AFRICA = "South Africa"
    NEW_ZEALAND = "New Zealand"
    WEST_INDIES = "West Indies"
    PAKISTAN = "Pakistan"
    SRI_LANKA = "Sri Lanka"


class Role(StrEnum):
    BATTER = "Batter"
    BOWLER = "Bowler"
    ALL_ROUNDER = "All Rounder"
    WICKET_KEEPER = "Wicket Keeper"
    CAPTAIN = "Captain"
    VICE_CAPTAIN = "Vice Captain"

class MatchStatus(StrEnum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    TIED = "Tied"
    DRAWN = "Drawn"

class TossChoice(StrEnum):
    HEAD = "H"
    TAIL = "T"

class TeamStatus(StrEnum):
    BATTING = "Batting"
    BOWING = "Bowling"