from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState

import unittest
from time import time


class DraughtsTest(unittest.TestCase):
    MAX_MOVE_TIME = 3

    def setUp(self):
        self.ai = AI(PositionEvaluation(), search_depth=2)
        self.board = BoardState()

    def test_ai_vs_ai(self):
        board = BoardState.initial_state()
        while not board.ended():
            start_time = time()
            board = self.ai.next_move(board)
            finish_time = time()
            self.assertIsNotNone(board)
            elp_time = finish_time - start_time
            self.assertLess(elp_time, DraughtsTest.MAX_MOVE_TIME)

    def test_simple_move_forward(self):
        self.board.board[7, 0] = 1
        result = self.ai.next_move(self.board)
        self.assertEqual(result.board[7, 0], 0)
        self.assertEqual(result.board[6, 1], 1)

    def test_simple_capt(self):
        self.board.board[7, 0] = 1
        self.board.board[6, 1] = -1
        result = self.ai.next_move(self.board)
        self.assertEqual(result.board[7, 0], 0)
        self.assertEqual(result.board[6, 1], 0)
        self.assertEqual(result.board[5, 2], 1)

    def test_king_creation(self):
        self.board.board[1, 0] = 1
        result = self.ai.next_move(self.board)
        self.assertEqual(result.board[1, 0], 0)
        self.assertEqual(result.board[0, 1], 2)

    def test_king_capt(self):
        self.board.board[7, 0] = 2
        self.board.board[1, 6] = -1
        result = self.ai.next_move(self.board)
        self.assertEqual(result.board[7, 0], 0)
        self.assertEqual(result.board[1, 6], 0)
        self.assertEqual(result.board[0, 7], 2)

    def test_multi_move(self):
        self.board.board[7, 0] = 1
        self.board.board[6, 1] = -1
        self.board.board[4, 3] = -1
        self.board.board[4, 5] = -1
        result = self.board.copy()
        for i in range(3):
            result = self.ai.next_move(result)
        self.assertEqual(result.board[7, 0], 0)
        self.assertEqual(result.board[6, 1], 0)
        self.assertEqual(result.board[4, 3], 0)
        self.assertEqual(result.board[4, 5], 0)
        self.assertEqual(result.board[5, 6], 1)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DraughtsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
