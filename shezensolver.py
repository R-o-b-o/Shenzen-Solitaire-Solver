# import pyautogui
# import pytesseract
# import numpy as np
# from collections import deque 
from PIL import Image, ImageGrab, ImageDraw

from shenzenboard import Board
   

def get_screengrab():
    return Image.open('example.png')

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

