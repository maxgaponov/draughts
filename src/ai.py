from typing import Optional

from .boardstate import BoardState


class PositionEvaluation:
    def __call__(self, board: BoardState) -> float:
        score = 0
        for i in range(8):
            for j in range(8):
                score += board.board[i, j] * board.current_player
        return score


class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.search_depth: int = search_depth

    def next_move(self, board: BoardState) -> Optional[BoardState]:
        return self.get_best_move_and_score(board, self.search_depth)[0]

    def get_best_move_and_score(self, state, search_depth: int):
        moves = state.get_possible_moves()

        if len(moves) == 0 or search_depth == 0:
            return None, self.position_evaluation(state)

        best_score = None
        best_move = None
        for move in moves:
            score = self.get_best_move_and_score(move, search_depth=search_depth - 1)[1]
            score *= -1
            if best_move is None or best_score < score:
                best_score = score
                best_move = move

        return best_move, best_score
