import numpy as np
from typing import Optional


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player
        self.last_move = (-1, -1)
        self.last_move_cont = False
        self.is_last_capt = False

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        move = (from_x, from_y, to_x, to_y)
        moves = self.get_possible_moves()
        return moves.get(move)

    def get_possible_moves(self):
        cells = [self.last_move] if self.last_move_cont else self.get_current_player_cells()
        moves = {}
        for (from_x, from_y) in cells:
            self.add_possible_moves_from_pos(moves, from_x, from_y)

        capt_moves = dict([(move, state) for (move, state) in moves.items() if state.is_last_capt])
        if len(capt_moves) > 0:
            moves = capt_moves

        return moves

    def add_possible_moves_from_pos(self, moves, from_x, from_y):
        is_king = (abs(self.board[from_y, from_x]) == 2)
        move_lens = list(range(1, 8) if is_king else range(1, 3))

        for dir_x in [1, -1]:
            for dir_y in [1, -1]:
                for move_len in move_lens:
                    if not is_king and move_len == 1 and dir_y == self.current_player:
                        continue
                    dx = dir_x * move_len
                    dy = dir_y * move_len
                    to_x = from_x + dx
                    to_y = from_y + dy
                    if not self.is_empty_cell(to_x, to_y):
                        continue
                    move = (from_x, from_y, to_x, to_y)
                    enemy_cnt = 0
                    enemy_x = -1
                    enemy_y = -1
                    for i in range(1, move_len):
                        cur_x = from_x + i * dir_x
                        cur_y = from_y + i * dir_y
                        if self.is_enemy_cell(cur_x, cur_y):
                            enemy_cnt += 1
                            enemy_x = cur_x
                            enemy_y = cur_y
                    if enemy_cnt > 1:
                        continue
                    if not is_king and enemy_cnt == 0 and move_len == 2:
                        continue
                    if self.last_move_cont and enemy_cnt == 0:
                        continue
                    result = self.copy()
                    result.board[to_y, to_x] = result.board[from_y, from_x]
                    king_line = 0 if self.current_player == 1 else 7
                    if to_y == king_line:
                        result.board[to_y, to_x] = self.current_player * 2
                    result.board[from_y, from_x] = 0
                    if enemy_cnt == 1:
                        result.board[enemy_y, enemy_x] = 0
                        result.is_last_capt = True
                        result.last_move = (to_x, to_y)
                        result.last_move_cont = True
                        if len(result.get_possible_moves()) == 0:
                            result.last_move_cont = False
                            result.current_player *= -1
                    else:
                        result.last_move_cont = False
                        result.is_last_capt = False
                        result.current_player *= -1
                    moves[move] = result

    def is_empty_cell(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8 and self.board[y, x] == 0

    def get_current_player_cells(self):
        cells = []
        for x in range(8):
            for y in range(8):
                if np.sign(self.board[y, x]) == self.current_player:
                    cells += [(x, y)]
        return cells

    def is_enemy_cell(self, x, y):
        return self.board[y, x] * self.current_player < 0

    def ended(self):
        return len(self.get_possible_moves()) == 0

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)

        for i in range(8):
            for j in range(8):
                if (i + j) % 2:  # black cell
                    if i >= 5:  # first player
                        board[i, j] = 1
                    elif i < 3:  # second player
                        board[i, j] = -1

        return BoardState(board, 1)
