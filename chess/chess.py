from abc import ABC,abstractmethod
from enum import StrEnum

class Position:

    def __init__(self,row:int,col:int):
        self.row = row
        self.col = col

class PieceType(StrEnum):
    BLACK = "black"
    WHITE = "white"
    
class Piece(ABC):

    def __init__(self,color:PieceType):
        self.position = None
        self.alive = True 
        self.color = color

    @abstractmethod
    def get_possible_moves(self)->list[Position]:
        pass

    def move(self,new_position:Position):
        self.position = new_position



class Player:
    def __init__(self,name:str,piece_type:PieceType):
        self.name = name
        self.piece_type = piece_type

class Board:
    def __init__(self):
        self.board = [[0]*8 for _ in range(8)]
        self.rows = 8
        self.cols = 8
        self.position_piece_map = {(x,y):Piece,.....}


class Game:
    def __init__(self,board:Board,player1:Player,player2:Player):
        self.board = board 
        self.player1 = player1
        self.player2 = player2
        self.player1_pieces = self.get_player1_pieces()
        self.player2_pieces = self.get_player2_pieces()
        self.active_player = None


    def get_player1_pieces(self):
        return 

    def get_player2_pieces(self):
        return 

    def get_piece(self,piece:str):
        return Piece()
    
    def play(self,player:Player):
        # {""}
        while True:

            piece:Piece = self.get_piece(input(f"{self.active_player}'s turn"))
            moves = piece.get_possible_moves()
            print(moves)
            move = self.get_piece(input(f"{self.active_player}'s move"))
            if move in moves:

            piece = input(f"{self.active_player}'s turn")

        

