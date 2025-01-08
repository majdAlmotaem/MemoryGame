import random

class MemoryGame:
    def __init__(self, level=1):
        self.level = level
        self.size = 4  # Feste Größe für alle Level
        self.board = self._create_board()
        self.flipped_cards = []
        self.matched_pairs = 0
        self.hearts = 3

    def _create_board(self):
        total_cards = self.size * self.size
        pairs_needed = total_cards // 2
        
        # Erweiterte Symbolliste
        symbols = list('🍎🍐🍊🍋🍌🍉🍇🍓🍒🍑🍍🥝🥥🥕🌽🥨🥐🍖🍗🍔🍪🍫🍬🍭🍮🍯🍺🍻🍷🍸')[:pairs_needed]
        symbols = symbols * 2  # Verdopple die Symbole für Paare
        
        random.shuffle(symbols)
        return [{'symbol': symbol, 'matched': False, 'flipped': False} for symbol in symbols]

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
            self.hearts -= 1  # Verliere ein Herz bei Fehler
            return False

    def has_lost(self):
        return self.hearts <= 0

    def is_game_over(self):
        return self.matched_pairs == self.size**2 // 2
    
    def _calculate_size_for_level(self):
        return 4

    def level_up(self):
        if self.level < 10:  # Maximales Level ist 10
            self.level += 1
            self.size = self._calculate_size_for_level()
            self.board = self._create_board()
            self.flipped_cards = []
            self.matched_pairs = 0
            self.hearts = 3  # Setze Herzen beim Level-Up zurück
            return True
        return False

