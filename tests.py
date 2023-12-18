import random
import sys
import time

# Determines whether the indices are in the pyramid range or not
def pyramid_indices(row_value, col_value):
    y = 4
    z = 4
    for x in range(5):
        if (row_value == x) and (col_value > y or col_value < z):
            return False
        y = y + 1
        z = z - 1
    return True


# Blue is not on the frame of the pyramid
def blue_rule(row_value, col_value, width, height):
    if row_value == height-1:
        return False
    y = int(width/2)
    z = int(width/2)
    for x in range(height-1):
        if (row_value == x) and (col_value == y or col_value == z):
            return False
        y = y + 1
        z = z - 1
    return True


# Pink don't have blue neighbors
def pink_rule(row_value, col_value, matrix, width, height):
    if row_value == 0:  # In a case of a first row, check only the lower neighbor
        if matrix[row_value + 1][col_value] == 1:
            return False
    if row_value == height-1:  # In a case of a last row, check only the right, left, and up neighbors
        if col_value == 0:
            if matrix[row_value][col_value + 1] == 1:
                return False
            return True
        if col_value == width-1:
            if matrix[row_value][col_value - 1] == 1:
                return False
            return True
        else:
            if matrix[row_value][col_value + 1] == 1 or matrix[row_value][col_value - 1] == 1 or \
                    matrix[row_value - 1][col_value] == 1:
                return False
    else:
        if matrix[row_value][col_value + 1] == 1 or matrix[row_value][col_value - 1] == 1 or \
                matrix[row_value - 1][col_value] == 1 or matrix[row_value + 1][col_value] == 1:
            return False
    return True


# In each row, less than 4 yellow cells
def yellow_rule(row_value, yellows_array):
    if yellows_array[row_value] > 4:
        return False
    return True


# If the indices are in the pyramid range so the optional values are one of the values {1,2,3},and else the value is 0
def create_first_matrix(matrix, width, height):
    for p_r in range(height):
        for p_c in range(width):
            if pyramid_indices(p_r, p_c):
                matrix[p_r][p_c] = random.randint(1, 3)
            else:
                matrix[p_r][p_c] = 0


def print_matrix(matrix, row_value, col_value):
    print("the current indices are: " + "[" + str(row_value) + "]" + "[" + str(col_value) + "]")
    for r_ind in matrix:
        print(r_ind)
    print(" ")


# Count the number of yellow cells in each row; the list will be updated in each randomize action
def init_yellows(matrix,width, height):
    yellows_array = [0, 0, 0, 0, 0]
    for row_index in range(height):
        number_of_yellow_cells = 0
        for column_index in range(width):
            if pyramid_indices(row_index, column_index):
                if matrix[row_index][column_index] == 2:  # if the cell is yellow so increase the counter
                    number_of_yellow_cells += 1
        yellows_array[row_index] = number_of_yellow_cells
    return yellows_array


def run_the_game(matrix, width, height):
    create_first_matrix(matrix,width, height)
    print("starting board")
    print_matrix(matrix, 0, 0)
    yellows = init_yellows(matrix, width, height)
    counter = 1
    while counter != 0:
        counter = 0
        for r in range(height):
            for c in range(width):
                if pyramid_indices(r, c):
                    # For each pyramid's cell, check it's color and then determined if it necessary to randomize a new color
                    if matrix[r][c] == 1:  # If the cell is blue
                        blue_condition = blue_rule(r, c, width, height)
                        if not blue_condition:
                            matrix[r][c] = random.randint(2, 3)  # Random different value than 1
                            if matrix[r][c] == 2:  # If the new color is yellow so increase yellow[r] by 1
                                yellows[r] += 1
                            counter += 1
                        print_matrix(matrix, r, c)
                    else:
                        if matrix[r][c] == 2:  # If the cell is yellow
                            yellow_condition = yellow_rule(r, yellows)
                            if not yellow_condition:
                                yellows[r] = 0
                                for j in range(width):  # Replace the colors in the whole row in the pyramid
                                    if pyramid_indices(r, j):
                                        matrix[r][j] = random.randint(1, 3)
                                        if matrix[r][
                                            j] == 2:  # If the new color is yellow so increase yellows[r] by 1
                                            yellows[r] += 1
                                counter += 1
                            print_matrix(matrix, r, c)
                        else:
                            if matrix[r][c] == 3:  # If the cell is pink
                                pink_condition = pink_rule(r, c, matrix, width, height)
                                if not pink_condition:
                                    matrix[r][c] = random.randint(1, 2)  # Random different value than 3
                                    if matrix[r][c] == 2:  # If the new color is yellow so increase yellows[r] by 1
                                        yellows[r] += 1
                                    counter += 1
                                print_matrix(matrix, r, c)

    print("the board game satisfied all the rules ")


w, h = 9, 5
new_matrix = [[0 for x in range(w)] for y in range(h)]
run_the_game(new_matrix, w, h)









