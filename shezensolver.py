import pyautogui
import pytesseract
import numpy as np
from collections import deque 
from PIL import Image, ImageGrab, ImageDraw

from shenzenboard import Board
   

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



starting_coords = np.array((408, 397))
shape_size = np.array((25, 20))
x_offset = 152
y_offset = 31

if __name__ == "__main__":
    screengrab = get_screengrab()

    board = Board(screengrab)
    # test = get_possible_moves(board)

    # perform_move((0,7,2), board)

    # board_im_list = get_board_im_list(screengrab)

    # # show_board(board_im_list)
    # show_board_symbol_recognition(board_im_list)

    # for col in board_im_list:
    #     for symbol_im in col:
    #         recognize_symbol(symbol_im)

