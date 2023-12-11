from chess import Board, Move, engine, pgn
import os, sys
import time
import threading
from minimax import MinimaxEngine

def welcome():
    print("""

          """)

def main():
    file = input("Insert .pgn file: ")
    file_path = os.path.join("test", file)
    try:
        with open(file_path) as f:
            game = pgn.read_game(f)
    except FileNotFoundError:
        print("File doesn't exists. Make sure you add the .pgn file in the directory test and input the correct file name")
    else:
        depth = int(input("Input the depth for the analysis (recommended: 3): "))

        game = game.end()
        board = game.board()

        start_time = time.time()
        print("Processing, may take a while...")
        evaluator = engine.SimpleEngine.popen_uci(r"E:/stockfish/stockfish-windows-x86-64-avx2.exe")

        test_minimax = MinimaxEngine(player=board.turn)
        test_move = test_minimax.minimax(board, board.turn, depth, evaluator)
        
        evaluator.close()
        end_time = time.time()
        print("Done evaluating.")
        time.sleep(0.8)
        
        exe_time = round(end_time-start_time, 5)

        best_move = test_move[1].uci()
        print("Found the best move: " + best_move + " in " + str(exe_time) + " seconds")

if __name__ == "__main__":
    main()