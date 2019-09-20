

class GameStats:
    WINNING_SCORE_LIMIT = 11
    MATCH_LIMIT = 5

    PLAYER_LEFT = 'PL'
    PLAYER_RIGHT = 'PR'

    def __init__(self, player_left_score=0, player_right_score=0):
        self.pLeftScore = player_left_score
        self.pRightScore = player_right_score
        self.pLMatchScore = 0
        self.pRMatchScore = 0

    def set_player_left_score(self, score):
        self.pLeftScore = score

    def set_player_right_score(self, score):
        self.pRightScore = score

    def increment_player_score(self, player):
        if player == self.PLAYER_LEFT:
            self.pLeftScore += 1
        elif player == self.PLAYER_RIGHT:
            self.pRightScore += 1

    def increment_match_score(self, player):
        if player == self.PLAYER_LEFT:
            self.pLMatchScore += 1
        elif player == self.PLAYER_RIGHT:
            self.pRMatchScore += 1

    def has_game_winner(self):
        if abs(self.pLeftScore - self.pRightScore) >= 2:
            if self.pRightScore >= self.WINNING_SCORE_LIMIT:
                return True, 'rightWin'
            elif self.pLeftScore >= self.WINNING_SCORE_LIMIT:
                return True, 'leftWin'
        return False, ''

    def has_match_winner(self):
        if self.pLMatchScore >= 3:
            return True, 'leftWin'
        elif self.pRMatchScore >= 3:
            return True, 'rightWin'
        else:
            return False, ''

    def get_player_scores(self):
        return self.pLeftScore, self.pRightScore

    def reset_game(self):
        self.pLeftScore = 0
        self.pRightScore = 0

    def reset_match(self):
        self.reset_game()
        self.pLMatchScore = 0
        self.pRMatchScore = 0


