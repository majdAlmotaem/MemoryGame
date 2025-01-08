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
            app_name='memorygame',
            icon='resources/256.png'
        )
        self.game_started = False

    def startup(self):
        self.game = MemoryGame()
        
        self.main_window = toga.MainWindow(
            title='Memory Game', 
            size=(300, 500)
        )
        
        # Äußerster Container ohne Padding
        outer_container = toga.Box(style=Pack(
            direction=COLUMN,
            background_color=self.DARK_BACKGROUND,
            flex=1,
            padding=0
        ))

        # Innerer Container für den Content
        main_box = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=20,
            background_color=self.DARK_BACKGROUND,
            alignment='center',
            flex=1
        ))
        
        self.board_box = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=10,
            background_color=self.DARK_BACKGROUND,
            alignment='center'
        ))
        
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

        # Füge alle Elemente zum inneren Container hinzu
        main_box.add(self.board_box)
        main_box.add(start_button)
        main_box.add(reset_button)

        # Füge den inneren Container zum äußeren hinzu
        outer_container.add(main_box)
        
        # Setze den äußeren Container als Hauptinhalt
        self.main_window.content = outer_container
        self.main_window.show()

    def start_game(self, widget):
        self.create_board_grid(preview=True)
        self.main_window.app.add_background_task(self.hide_cards_after_delay)

    async def hide_cards_after_delay(self, widget):
        await asyncio.sleep(3)
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
                        width=70, 
                        height=70, 
                        padding=5,
                        background_color=self.DARK_BUTTON_BACKGROUND,
                        color=self.ACCENT_COLOR,
                        font_size=32,
                        font_weight='bold',
                        alignment='center'
                    )
                )
                row_box.add(card_button)
            
            self.board_box.add(row_box)
        
        if self.game.is_game_over():
            self.beep()
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
