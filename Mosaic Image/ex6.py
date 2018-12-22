###############################################################
# FILE : ex6.py
# WRITER : Harel Yacovian, harelyac, 311319990
# EXERCISE : intro2d cs ex4 2016-2017
# DESCRIPTION : This functions file used for making the photoMosaic
# image which is an image made out a lot of others images that resemble
# with their color to the original pixels.
###############################################################

import math
from copy import deepcopy
from PIL import Image
import sys
import mosaic

ZERO_VALUE = 0
RED_VALUE = 0
GREEN_VALUE = 1
BLUE_VALUE = 2
ROW = 0
COL = 1


def compare_pixel(pixel1, pixel2):
    """
    Calculate the difference of each r,g,b value of 1 pixel to the other 1.
    :param pixel1: First tuple that indicates the r,g,b distribute of a pixel.
    :param pixel2: Second tuple that indicates the r,g,b distribute of a pixel.
    :return: The sum of all differences between each r,g,b of a single pixel
    and on a second pixel. which is called the "two pixels difference"
    """

    pixel_dif_sum = 0

    # Calculate the diff sum
    pixel_dif_sum = math.fabs(pixel1[RED_VALUE] - pixel2[RED_VALUE]) + \
                    math.fabs(pixel1[GREEN_VALUE] - pixel2[GREEN_VALUE]) + \
                    math.fabs(pixel1[BLUE_VALUE] - pixel2[BLUE_VALUE])

    return pixel_dif_sum


def compare(image1, image2):
    """
    Calculate the sum of all differences between two pixels.
    :param image1: First image
    :param image2: Second image
    :return: Return the sum of all the "two pixels difference" between
    each pixel on first image to the matched pixel on the second image which
    is called the "two images difference"
    """

    image_dif_sum = 0

    # Check images sizes
    length1 = len(image1)
    length2 = len(image2)
    width1 = len(image1[ZERO_VALUE])
    width2 = len(image2[ZERO_VALUE])

    # Calculate the "two images difference".
    for row in range(min(length1,length2)):
        for col in range(min(width1,width2)):
            # Call the compare pixel func
            image_dif_sum += compare_pixel(image1[row][col], image2[row][col])
    return image_dif_sum


def get_piece(image, upper_left, size):
    """
    Cut a piece from the image with given sizes requirements.
    :param image: The origin image
    :param upper_left: a starting point where we start
    to cut the piece of the image
    :param size:
    :return: the piece which was cut out of the image
    """

    piece = list()
    temp_list = list()

    length = size[ROW] + upper_left[ROW]
    width = size[COL] + upper_left[COL]

    # Checking if the size of the cut piece dont cross the borders of origin
    # image - calling check functions
    if length > len(image):
        length = len(image)
    if width > len(image[ROW]):
        width = len(image[ROW])

    # Cutting process
    for row in range(upper_left[ROW], length):
        piece.append(image[row][upper_left[COL]:width])
    return piece


def set_piece(image, upper_left, piece):
    """
    Set the piece inside the origin image
    :param image: The origin image
    :param upper_left: the upper left coordinate of the piece
    to be set into the image
    :param piece: the piece that is now being set into the image
    :return:
    """

    length = len(piece) + upper_left[ROW]
    width = len(piece[ROW]) + upper_left[COL]

    # Checking if the size of the cut piece dont cross the borders of origin
    # image - calling check functions
    if length > len(image):
        length = len(image)
    if width > len(image[ROW]):
        width = len(image[ROW])

    # Make starting points to indexes to run in the current piece image
    row_piece = 0
    col_piece = 0

    # Setting process
    for row in range(upper_left[ROW], length):
        col_piece = 0
        for col in range(upper_left[COL], width):
            image[row][col] = piece[row_piece][col_piece]
            col_piece += 1
        row_piece += 1


def average(image):
    """
    Calculate the average r,g,b count of all pixels in the image
    :param image: the origin image
    :return: the average r,g,b count
    """

    avg_red = 0
    avg_blue = 0
    avg_green = 0

    # Calculate the pixels number in the image
    pixels_num = len(image)*len(image[ROW])

    # Move on each pixel in the image and sum the r,g,b counts
    for row in range(len(image)):
        for col in range(len(image[ROW])):
            avg_red += image[row][col][RED_VALUE]
            avg_blue += image[row][col][BLUE_VALUE]
            avg_green += image[row][col][GREEN_VALUE]

    # Calculate the average r,g,b of all pixels of the image
    avg_blue /= pixels_num
    avg_green /= pixels_num
    avg_red /= pixels_num

    return avg_red, avg_green, avg_blue


def preprocess_tiles(tiles):
    """
    This function calculate the average r,g,b count of all pixels inside
    each tile in the tiles list
    :param tiles: the tiles list
    :return: the average r,g,b count of each tile in the list
    """
    avg_tiles_list = []

    for tile in range(len(tiles)):
        avg_tiles_list.append(average(tiles[tile]))
    return avg_tiles_list


def get_best_tiles(objective, tiles, averages , num_candidates):
    """
    Calculate the best tiles to start work with and more deeply to start
    choose from.
    :param objective: the chosen image to be changed by the chosen tile
    :param tiles: list of tiles
    :param averages: avg r,g,b count of each tiles
    :param num_candidates: number of candidates that one of them will be the
    chosen one
    :return: all the candidate
    """

    best_tiles_list = list()
    pixel_diff_list = list()
    temp_pixel_list = list()

    # Check the avg count of objective image
    obj_avg_rgb = average(objective)

    # Check all differences of tiles from objective image
    for tile in range(len(averages)):
        pixel_diff_list.append(compare_pixel(obj_avg_rgb, averages[tile]))

    # Makes a copy of the diff list to keep the indexes intact
    temp_pixel_list = pixel_diff_list[:]

    # Check for the lowest pixel_diff for "num_candidates" times
    for candidate in range(num_candidates):
        # Find min diff
        option = min(pixel_diff_list)
        # Find the index of the min tile
        min_index = temp_pixel_list.index(option)
        # Remove the diff from diff list
        pixel_diff_list.remove(option)
        # Append the tile to the best tiles list!
        best_tiles_list.append(tiles[min_index])
    return best_tiles_list


def choose_tile(piece, tiles):
    """
    This function compare more deeply between images. by using the compare
    functions.
    :param piece: the piece of the image that we want to change
    :param tiles: the list of chosen tiles that only one of them will
    be the chosen one
    :return: This function return the chosen tile to be
    implemented in the image
    """

    diff_sum_list = list()
    for tile in tiles:
        diff_sum = compare(piece, tile)
        diff_sum_list.append(diff_sum)

    # Get the chosen one which is minimal
    minimal_diff_sum = min(diff_sum_list)
    min_index = diff_sum_list.index(minimal_diff_sum)
    chosen_tile = tiles[min_index]

    return chosen_tile


def make_mosaic(image, tiles, num_candidates):
    """
    This is the main functions which make eventually the transformed image,
    the Photomosaic
    :param image: the original image
    :param tiles: the tiles list
    :param num_candidates: num of candidate to choose the chosen one from
    :return: the transformed image!
    """

    avg_tiles_list = ()
    best_tiles = ()
    tile_length = len(tiles[ZERO_VALUE])
    tile_width = len(tiles[ZERO_VALUE][ZERO_VALUE])
    image_length = len(image)
    image_width = len(image[ZERO_VALUE])
    size = (tile_length,tile_width)
    temp_image = deepcopy(image)

    # Preprocess tiles
    avg_tiles_list = preprocess_tiles(tiles)

    # Make the full algoritem process of making the moasic image!
    for piece_len in range(0,image_length,tile_length):
        for piece_width in range(0,image_width, tile_width):
            upper_left = (piece_len, piece_width)
            obj_piece = get_piece(temp_image,upper_left,size)
            best_tiles = get_best_tiles\
                (obj_piece, tiles,avg_tiles_list,num_candidates)
            chosen_tile = choose_tile(obj_piece,best_tiles)
            set_piece(temp_image,upper_left,chosen_tile)
    return temp_image

def main():
    # initializing variables
    image_name = sys.argv[1]
    tiles_directory = sys.argv[2]
    tile_height = int(sys.argv[4])
    image = list()
    tiles = list()
    mosaic_image = list()
    num_of_candidates = int(sys.argv[5])
    # Make the list of list image
    image = mosaic.load_image(image_name)
    # Make the list tiles that are pure list of list made
    tiles = mosaic.build_tile_base(tiles_directory,tile_height)
    # Start the mosaic process!
    mosaic_image = make_mosaic(image, tiles, num_of_candidates)
    # The name of the mosaic image
    mosaic_name = sys.argv[3]
    # Saving the image
    mosaic.save(mosaic_image,mosaic_name)

if __name__ == "__main__":
    NUMBER_OF_PARAMETERS = 6
    # Check number of arguments:
    if len(sys.argv) != 6:
        print("Wrong number of parameters. The correct usage is:" + "\n" +
              "ex6.py <image_source> <images_dir> <output_name>" +
              " <tile_height> <num_candidates>")
    else:
        main()
