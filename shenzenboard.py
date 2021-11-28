import pyautogui
import pytesseract
import numpy as np
from collections import deque 
from PIL import Image, ImageGrab, ImageDraw

class Board:
    def __init__(self, screengrab) -> None:
        self._starting_coords = np.array((408, 397))
        self._shape_size = np.array((25, 20))
        self._x_offset = 152
        self._y_offset = 31

        self.card_array = self._get_card_array_from_screengrab(screengrab)

    def get_possible_moves(self, board):
        moves_possible = []
        for col_num, col in enumerate(board):
            card_index = 0
            while True:
                for i in range(1,8):
                    other_col_num = (col_num+i)%8
                    if self._can_place_over(col[card_index], board[other_col_num][0]):
                        moves_possible.append((col_num, other_col_num, card_index+1))

                card_index += 1
                if not self._can_place_over(col[card_index], col[card_index-1]):
                    break
        return moves_possible

    def perform_move(self, move, board):
        moved_card_list =  []

        col1, col2, num_cards = move

        for _ in range(num_cards):
            moved_card_list.append(board[col1].popleft())

        for card in reversed(moved_card_list):
            board[col2].appendleft(card)

    def _get_card_array_from_screengrab(self, screengrab):
        card_array = []
        for i in range(8):
            col = deque()
            coords = self._starting_coords + np.array((self._x_offset*i,0))

            while True:
                square_im = screengrab.crop(tuple(coords)+tuple(coords+self._shape_size))

                if self._is_blank_section(square_im):
                    break


                symbol = self._get_symbol_col_from_im(square_im)
                col.appendleft(symbol)
                coords = (coords[0], coords[1]+self._y_offset)

            card_array.append(col)
        return card_array

    def _get_symbol_col_from_im(self, symbol_im):
        col = self._recognize_symbol_col(symbol_im)
        symbol = self._recognize_symbol(symbol_im)

        if col is None:
            symbol = "R"

        return (symbol, col) 

    def _recognize_symbol(self, symbol_im):
        symbol = pytesseract.image_to_string(symbol_im, config="--psm 13")[0]

        symbol = symbol.replace("g","9")
        return symbol if symbol in "123456789" else "D"

    def _recognize_symbol_col(self, symbol_im):
        pixels = symbol_im.getcolors(symbol_im.width * symbol_im.height)

        symbol_colors = [
            [(174, 44, 20), (174, 43, 19)],
            [(18, 110, 75)],
            [(0, 0, 0), (14, 15, 13)]
        ]

        for _, color in pixels:
            for i in range(len(symbol_colors)):
                try:
                    symbol_col = symbol_colors[i].index(color[:3])
                    # return symbol_colors[i][0]
                    return i
                except ValueError:
                    pass
        return None

    def _can_place_over(self, symbol_top, symbol_bottom):
        if any(i in ("D", "R") for i in (symbol_top[0], symbol_bottom[0])):
            return False
        return symbol_top[1] != symbol_bottom[1] and int(symbol_top[0]) == int(symbol_bottom[0]) - 1

    def _is_blank_section(self, image):
        background_color = (202, 202, 189)
        pixels = image.getcolors(image.width * image.height)

        nearness_count = 0
        for count, color in pixels:
            nearness = np.linalg.norm(np.array(color[:3])-np.array(background_color))
            if nearness < 50:
                nearness_count += count

        return nearness_count/(image.width * image.height) > 0.9
