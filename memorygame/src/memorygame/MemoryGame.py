import random

class MemoryGame:
    def __init__(self, size=4):
        self.size = size
        self.board = self._create_board()
        self.flipped_cards = []
        self.matched_pairs = 0

    def _create_board(self):
        symbols = list('🍎🍐🍊🍋🍌🍉🍇🍓') * 2
        random.shuffle(symbols)
        return [{'symbol': symbol, 'matched': False, 'flipped': False} for symbol in symbols[:self.size**2]]

    def flip_card(self, index):
        card = self.board[index]
        if not card['matched'] and not card['flipped']:
            card['flipped'] = True
            self.flipped_cards.append(index)

            if len(self.flipped_cards) == 2:
                return self._check_match()
        return False

    def _check_match(self):
        card1 = self.board[self.flipped_cards[0]]
        card2 = self.board[self.flipped_cards[1]]

        if card1['symbol'] == card2['symbol']:
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs += 1
            self.flipped_cards.clear()
            return True
        else:
            card1['flipped'] = False
            card2['flipped'] = False
            self.flipped_cards.clear()
            return False

    def is_game_over(self):
        return self.matched_pairs == self.size**2 // 2
