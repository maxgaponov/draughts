from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState

import unittest
from time import time


class DraughtsTest(unittest.TestCase):
    MAX_MOVE_TIME = 2

    def test_ai_vs_ai(self):
        ai = AI()
        board = BoardState.initial_state()
        while not board.ended():
            start_time = time()
            board = ai.next_move(board)
            finish_time = time()
            self.assertIsNotNone(board)
            elp_time = finish_time - start_time
            self.assertLess(elp_time, DraughtsTest.MAX_MOVE_TIME)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DraughtsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
