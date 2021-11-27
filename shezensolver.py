import pyautogui
import pytesseract
import numpy as np
from collections import deque 
from PIL import Image, ImageGrab, ImageDraw


def is_blank_section(image):
    background_color = (202, 202, 189)
    pixels = image.getcolors(image.width * image.height)

    nearness_count = 0
    for count, color in pixels:
        nearness = np.linalg.norm(np.array(color[:3])-np.array(background_color))
        if nearness < 50:
            nearness_count += count

    return nearness_count/(image.width * image.height) > 0.9

def recognize_symbol_col(symbol_im):
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


def recognize_symbol(symbol_im):
    # symbol_im.show()
    symbol = pytesseract.image_to_string(symbol_im, config="--psm 13")[0]
    # print(symbol)
    symbol = symbol.replace("g","9")
    return symbol if symbol in "123456789" else "D"

def get_symbol_col_from_im(symbol_im):
    col = recognize_symbol_col(symbol_im)
    symbol = recognize_symbol(symbol_im)

    if col is None:
        symbol = "R"

    return (symbol, col) 

       

def get_screengrab():
    return Image.open('example.png')

def show_board(board):
    max_col = max([len(x) for x in board])
    board_im = Image.new("RGB", tuple(np.array((len(board), max_col))*shape_size))

    for col_index, col in enumerate(board):
        for row_index, square in enumerate(col):
            board_im.paste(square, tuple(np.array((col_index, row_index))*shape_size))

    board_im.show()

def show_board_symbol_recognition(board):
    max_col = max([len(x) for x in board])
    board_im = Image.new("RGB", tuple(np.array((len(board), max_col))*shape_size))

    for col_index, col in enumerate(board):
        for row_index, square in enumerate(col):
            d = ImageDraw.Draw(square)
            d.text((0,0), recognize_symbol(square), fill=recognize_symbol_col(square))
            board_im.paste(square, tuple(np.array((col_index, row_index))*shape_size))

    board_im.show()

def get_board_im_list(screengrab):
    board_im_list = []
    for i in range(8):
        col = []
        coords = starting_coords + np.array((x_offset*i,0))

        while True:
            square_im = screengrab.crop(tuple(coords)+tuple(coords+shape_size))

            if is_blank_section(square_im):
                break

            col.append(square_im)
            coords = (coords[0], coords[1]+y_offset)

        board_im_list.append(col)
    return board_im_list

def get_board_from_screengrab(screengrab):
    board = []
    for i in range(8):
        col = deque()
        coords = starting_coords + np.array((x_offset*i,0))

        while True:
            square_im = screengrab.crop(tuple(coords)+tuple(coords+shape_size))

            if is_blank_section(square_im):
                break


            symbol = get_symbol_col_from_im(square_im)
            col.appendleft(symbol)
            coords = (coords[0], coords[1]+y_offset)

        board.append(col)
    return board

def can_place_over(symbol_top, symbol_bottom):
    if any(i in ("D", "R") for i in (symbol_top[0], symbol_bottom[0])):
        return False
    return symbol_top[1] != symbol_bottom[1] and int(symbol_top[0]) == int(symbol_bottom[0]) - 1

def get_possible_moves(board):
    moves_possible = []
    for col_num, col in enumerate(board):
        card_index = 0
        while True:
            for i in range(1,8):
                other_col_num = (col_num+i)%8
                if can_place_over(col[card_index], board[other_col_num][0]):
                    moves_possible.append((col_num, other_col_num, card_index+1))

            card_index += 1
            if not can_place_over(col[card_index], col[card_index-1]):
                break
    return moves_possible

def perform_move(move, board):
    moved_card_list =  []

    col1, col2, num_cards = move

    for _ in range(num_cards):
        moved_card_list.append(board[col1].popleft())

    for card in reversed(moved_card_list):
        board[col2].appendleft(card)




starting_coords = np.array((408, 397))
shape_size = np.array((25, 20))
x_offset = 152
y_offset = 31

if __name__ == "__main__":
    screengrab = get_screengrab()

    board = get_board_from_screengrab(screengrab)
    # test = get_possible_moves(board)

    # perform_move((0,7,2), board)

    # board_im_list = get_board_im_list(screengrab)

    # # show_board(board_im_list)
    # show_board_symbol_recognition(board_im_list)

    # for col in board_im_list:
    #     for symbol_im in col:
    #         recognize_symbol(symbol_im)

