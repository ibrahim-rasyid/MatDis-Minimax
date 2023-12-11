from abc import ABC, abstractmethod
from chess import Board, Move, engine, pgn
from math import inf
import os, sys
from time import time

MATE_SCORE = 100000

class Player(ABC):
    def __init__(self, player: bool, solver: str=None):
        self.player = player
        self.solver = solver
    
    @abstractmethod
    def move(self):
        pass

class MinimaxEngine:
    def __init__(self, player, depth=3):
        self.depth = depth
    
    def minimax(self, board: Board, player: bool, depth: int, evaluator: engine.SimpleEngine, alpha=-inf, beta=inf):
        # Basis
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            if player:
                return [evaluator.analyse(board, engine.Limit(depth=10))["score"].white().score(mate_score=MATE_SCORE), None]
            else:
                return [evaluator.analyse(board, engine.Limit(depth=10))["score"].black().score(mate_score=MATE_SCORE), None]
        
        moves = list(board.legal_moves)

        if board.turn == player:
            maxScore, bestMove = -inf, None

            for move in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self.minimax(test_board, not player, depth-1, evaluator, alpha, beta)
                
                alpha = max(alpha, score[0])
                if beta <= alpha:
                    break

                if score[0] >= maxScore:
                    maxScore = score[0]
                    bestMove = move
            
            return [maxScore, bestMove]
        else:
            minScore, bestMove = inf, None

            for move in moves:
                test_board = board.copy()
                test_board.push(move)

                score = self.minimax(test_board, not player, depth-1, alpha, beta)
                
                beta = min(beta, score[0])
                if beta <= alpha:
                    break

                if score[0] <= minScore:
                    minScore = score[0]
                    bestMove = move
            
            return [minScore, bestMove]

if __name__ == "__main__":
    test_board = Board()

    evaluator = engine.SimpleEngine.popen_uci(r"E:/stockfish/stockfish-windows-x86-64-avx2.exe")

    test_bot = MinimaxEngine(player=test_board.turn)

    start_time = time()
    print(test_bot.minimax(test_board, test_board.turn, 3, evaluator))
    end_time = time()
    print(end_time - start_time)
    evaluator.close()