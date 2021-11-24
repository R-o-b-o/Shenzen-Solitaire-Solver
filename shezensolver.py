import pyautogui
import pytesseract
import numpy as np
from PIL import Image, ImageGrab


def is_blank(image):
    
    background_color = (202, 202, 189)
    pixels = image.getcolors(image.width * image.height)

    nearness_count = 0
    for count, color in pixels:
        nearness = np.linalg.norm(np.array(color[:3])-np.array(background_color))
        if nearness < 50:
            nearness_count += count

    return nearness_count/(image.width * image.height) > 0.9


def get_screen_grab():
    return Image.open('example.png')

def show_board(board):
    max_col = max([len(x) for x in board])
    board_im = Image.new("RGB", tuple(np.array((len(board), max_col))*shape_size))

    for col_index, col in enumerate(board):
        for row_index, square in enumerate(col):
            board_im.paste(square, tuple(np.array((col_index, row_index))*shape_size))

    board_im.show()

def get_board_im_list(screen_grab):
    board_im_list = []
    for i in range(8):
        col = []
        coords = starting_coords + np.array((x_offset*i,0))

        while True:
            square_im = screen_grab.crop(tuple(coords)+tuple(coords+shape_size))

            if is_blank(square_im):
                break

            col.append(square_im)
            coords = (coords[0], coords[1]+y_offset)

        board_im_list.append(col)
    return board_im_list


starting_coords = np.array((408, 397))
shape_size = np.array((25, 25))
x_offset = 152
y_offset = 31

if __name__ == "__main__":
    screen_grab = get_screen_grab()
    board_im_list = get_board_im_list(screen_grab)

    show_board(board_im_list)

