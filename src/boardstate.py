import numpy as np
from typing import Optional, List


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        dx = to_x - from_x
        dy = to_y - from_y

        if abs(dx) != abs(dy): # not diag. movement
            return None

        if dx == 0:
            return None

        if self.board[from_y, from_x] * self.current_player <= 0: # invalid player
            return None

        if self.board[to_y, to_x] != 0: # occupied cell
            return None

        is_king = (abs(self.board[from_y, from_x]) == 2)

        (enemy_y, enemy_x) = (-1, -1)
        enemy_piece_cnt = 0
        for i in range(1, abs(dx)):
            y = from_y + i * np.sign(dy)
            x = from_x + i * np.sign(dx)
            cell_owner = np.sign(self.board[y, x])
            if cell_owner == self.current_player: # moved over itself piece
                return None
            elif cell_owner == -self.current_player:
                enemy_piece_cnt += 1
                (enemy_y, enemy_x) = (y, x)
        if enemy_piece_cnt > 1:
            return None

        if not is_king:
            if enemy_piece_cnt == 0:
                if dy != -self.current_player: # moved to incorrect direction
                    return None
            else:
                if abs(dx) != 2:
                    return None

        result = self.copy()
        result.board[to_y, to_x] = result.board[from_y, from_x]
        result.board[from_y, from_x] = 0
        if enemy_piece_cnt == 1:
            result.board[enemy_y, enemy_x] = 0
        result.current_player *= -1
        return result

    def get_possible_moves(self) -> List['BoardState']:
        return [] # todo

    @property
    def is_game_finished(self) -> bool:
        ... # todo

    @property
    def get_winner(self) -> Optional[int]:
        ... # todo

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)

        for i in range(8):
            for j in range(8):
                if (i + j) % 2: # black cell
                    if i >= 5: # first player
                        board[i, j] = 1
                    elif i < 3: # second player
                        board[i, j] = -1

        return BoardState(board, 1)
