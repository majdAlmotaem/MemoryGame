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
            icon= "resources/icon.png"
        )
        self.game_started = False
        self.current_level = 1

    def startup(self):
        self.game = MemoryGame()
    
        self.main_window = toga.MainWindow(
            title='Memory Game', 
            size=(300, 500)
        )
    
        outer_container = toga.Box(style=Pack(
            direction=COLUMN,
            background_color=self.DARK_BACKGROUND,
            flex=1,
            padding=0
        ))

        # Header Box mit dunklem Hintergrund
        header_box = toga.Box(style=Pack(
            direction=ROW, 
            alignment='center',
            background_color=self.DARK_BACKGROUND
        ))

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

        self.game = MemoryGame(level=self.current_level)
    
        self.level_label = toga.Label(
            f'Level: {self.current_level}',
            style=Pack(
                padding=(10, 10, 10, 10),
                color=self.DARK_BUTTON_TEXT,
                font_size=16,
                font_weight='bold',
                background_color=self.DARK_BACKGROUND
            )
        )

        self.hearts_label = toga.Label(
            '❤️' * self.game.hearts,
            style=Pack(
                padding=(10, 10, 10, 10),
                color='#FF0000',
                font_size=20,
                font_weight='bold',
                background_color=self.DARK_BACKGROUND,
                alignment='right'
            )
        )
    
        header_box.add(self.level_label)
        header_box.add(self.hearts_label)
        main_box.insert(0, header_box)

        main_box.add(self.board_box)
        main_box.add(start_button)
        main_box.add(reset_button)

        outer_container.add(main_box)
    
        self.main_window.content = outer_container
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
                if index < len(self.game.board):  # Prüfe ob der Index gültig ist
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
            self.on_level_complete()


    def on_card_press(self, index):
        if not self.game_started:
            return
        
        self.game.flip_card(index)
        self.hearts_label.text = '❤️' * self.game.hearts
        
        # Prüfe auf Game Over
        if self.game.has_lost():
            self.main_window.info_dialog(
                'Game Over!',
                'Du hast alle Leben verloren! Versuche es noch einmal!'
            )
            self.reset_game(None)
            return
            
        self.create_board_grid()
    
    def reset_game(self, widget):
        self.current_level = 1
        self.game = MemoryGame(level=self.current_level)
        self.level_label.text = f'Level: {self.current_level}'
        self.hearts_label.text = '❤️' * self.game.hearts
        self.game_started = False
        self.create_board_grid(preview=False)

    def on_level_complete(self):
        if self.game.level_up():
            self.current_level += 1
            self.level_label.text = f'Level: {self.current_level}'
            self.hearts_label.text = '❤️' * self.game.hearts  # Aktualisiere Herzen-Anzeige
            self.main_window.info_dialog(
                f'Level Up!{self.current_level}',
                f'Du bist wahnsinnig!'
            )
            self.game_started = False
            self.create_board_grid(preview=False)
        else:
            self.main_window.info_dialog(
                'Spiel gewonnen!',
                'wow du bist ein Genie!'
            )


def main():
    return MemoryGameApp()

if __name__ == '__main__':
    main().main_loop()
