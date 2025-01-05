import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .MemoryGame import MemoryGame
import asyncio

class MemoryGameApp(toga.App):
    # Dark color palette
    DARK_BACKGROUND = '#1E1E1E'
    DARK_BUTTON_BACKGROUND = '#2C2C2C'
    DARK_TEXT = '#E0E0E0'
    DARK_BUTTON_TEXT = '#FFFFFF'
    ACCENT_COLOR = '#4A90E2'

    def __init__(self):
        super().__init__(
            formal_name='Memory Game',
            app_id='com.example.memorygame',
            app_name='memorygame'
        )
        self.game_started = False

    def startup(self):
        self.game = MemoryGame()
        
        # Main window with dark background
        self.main_window = toga.MainWindow(
            title='Memory Game', 
            size=(300, 500)  # Mobile-friendly size
        )
        
        # Main box
        main_box = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=20,
            background_color=self.DARK_BACKGROUND,
            alignment='center'
        ))
        
        # Attempts label with dark theme
        self.attempts_label = toga.Label(
            'Attempts: 0', 
            style=Pack(
                padding=10, 
                color='black',
                font_size=16,
                alignment='center'
            )
        )
        
        # Game board
        self.board_box = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=10,
            background_color=self.DARK_BACKGROUND,
            alignment='center'
        ))
        
        # Start Game button with dark theme
        start_button = toga.Button(
            'Start Game', 
            on_press=self.start_game,
            style=Pack(
                padding=10, 
                background_color=self.DARK_BUTTON_BACKGROUND,
                color=self.DARK_BUTTON_TEXT,
                font_weight='bold',
                alignment='center'
            )
        )
        
        # Reset button with dark theme
        reset_button = toga.Button(
            'Reset Game', 
            on_press=self.reset_game,
            style=Pack(
                padding=10, 
                background_color=self.DARK_BUTTON_BACKGROUND,
                color=self.DARK_BUTTON_TEXT,
                font_weight='bold',
                alignment='center'
            )
        )
        
        main_box.add(self.attempts_label)
        main_box.add(self.board_box)
        main_box.add(start_button)
        main_box.add(reset_button)
        
        self.main_window.content = main_box
        self.main_window.show()

    def start_game(self, widget):
        self.create_board_grid(preview=True)
        self.main_window.app.add_background_task(self.hide_cards_after_delay)

    async def hide_cards_after_delay(self, widget):
        await asyncio.sleep(5)
        self.game_started = True
        self.create_board_grid(preview=False)

    def create_board_grid(self, preview=False):
        self.board_box.clear()
        grid_size = self.game.size
        
        for row in range(grid_size):
            row_box = toga.Box(style=Pack(
                direction=ROW, 
                alignment='center',
                padding=5
            ))
            
            for col in range(grid_size):
                index = row * grid_size + col
                card = self.game.board[index]
                
                button_text = card['symbol'] if preview or card['flipped'] or card['matched'] else '?'
                
                card_button = toga.Button(
                    button_text,
                    on_press=lambda widget, idx=index: self.on_card_press(idx),
                    style=Pack(
                        width=50, 
                        height=50, 
                        padding=5,
                        background_color=self.DARK_BUTTON_BACKGROUND,
                        color=self.ACCENT_COLOR,
                        font_size=20,
                        font_weight='bold',
                        alignment='center'
                    )
                )
                row_box.add(card_button)
            
            self.board_box.add(row_box)
        
        self.attempts_label.text = f'Attempts: {self.game.attempts}'
        
        if self.game.is_game_over():
            self.main_window.info_dialog(
                'Congratulations!', 
                'You won the game!'
            )

    def on_card_press(self, index):
        if not self.game_started:
            return
        
        self.game.flip_card(index)
        self.create_board_grid()

    def reset_game(self, widget):
        self.game = MemoryGame()
        self.game_started = False
        self.create_board_grid(preview=False)

def main():
    return MemoryGameApp()

if __name__ == '__main__':
    main().main_loop()
