from typing import Optional

from .boardstate import BoardState


class PositionEvaluation:
    def __call__(self, board: BoardState) -> float:
        score = 0
        for i in range(8):
            for j in range(8):
                score += (board.board[i, j] * board.current_player) ** 2
        return score


class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.search_depth: int = search_depth

    def next_move(self, board: BoardState) -> Optional[BoardState]:
        return self.get_best_state_and_score(board, self.search_depth)[0]

    def get_best_state_and_score(self, state, search_depth: int):
        cur_score = self.position_evaluation(state)
        if search_depth == 0:
            return None, cur_score

        moves = state.get_possible_moves()
        if len(moves) == 0:
            return None, cur_score

        best_score = None
        best_state = None
        for (move, state) in moves.items():
            score_approx = -self.get_best_state_and_score(state, search_depth=0)[1]
            if best_score is not None and score_approx < best_score:
                continue
            score = -self.get_best_state_and_score(state, search_depth=search_depth - 1)[1]
            if best_state is None or best_score < score:
                best_score = score
                best_state = state

        return best_state, best_score
