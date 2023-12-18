import random
import sys
import pygame
import time

# initialize pygame and create the screen
pygame.init()
main_font = pygame.font.SysFont("cambria", 50)
SCREEN = pygame.display.set_mode((800, 600))
SCREEN.fill((200, 200, 200, 0.5))
class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


# Converts indices from matrix [9][5] to size of the screen [800][600]
def convert_coordinates(pyramid_row, pyramid_col):
    return [100 + pyramid_row * 64, 100 + pyramid_col * 64]


# Determines whether the indices are in the pyramid range or not
def pyramid_indices(row_value, col_value, width, height):
    y = int(width/2)
    z = int(width/2)
    for x in range(height):
        if (row_value == x) and (col_value > y or col_value < z):
            return False
        y = y + 1
        z = z - 1
    return True


def print_matrix(matrix, row_value, col_value):
    print("the current indices are: " + "[" + str(row_value) + "]" + "[" + str(col_value) + "]")
    for r_ind in matrix:
        print(r_ind)
    print(" ")


# ************************************ INITIALIZING BOARD ************************************

# If the indices are in the pyramid range so the optional values are one of the values {1,2,3},and else the value is 0
def create_first_matrix(matrix, width, height):
    for p_r in range(height):
        for p_c in range(width):
            if pyramid_indices(p_r, p_c, width, height):
                matrix[p_r][p_c] = random.randint(1, 3)
            else:
                matrix[p_r][p_c] = 0


# Count the number of yellow cells in each row; the list will be updated in each randomize action
def init_yellows(matrix, width, height):
    yellows_array = [0 for x in range(h)]
    for row_index in range(height):
        number_of_yellow_cells = 0
        for column_index in range(width):
            if pyramid_indices(row_index, column_index, width, height):
                if matrix[row_index][column_index] == 2:  # if the cell is yellow so increase the counter
                    number_of_yellow_cells += 1
        yellows_array[row_index] = number_of_yellow_cells
    return yellows_array


# Convert number to color: blue - 1; yellow - 2; pink - 3; empty cell - 0
def create_board_game(matrix, width, height):
    white_cube_obj = pygame.image.load('square.png')
    yellow_cube_obj = pygame.image.load('yellow_square.png')
    blue_cube_obj = pygame.image.load('blue_square.png')
    pink_cube_obj = pygame.image.load('pink_square.png')
    SCREEN.fill("black")
    SCREEN.fill((200, 200, 200, 0.5))
    for p_r in range(height):
        for p_c in range(width):
            temp_array = convert_coordinates(p_r, p_c)
            if matrix[p_r][p_c] == 1:
                SCREEN.blit(blue_cube_obj, (temp_array[1], temp_array[0]))
            if matrix[p_r][p_c] == 2:
                SCREEN.blit(yellow_cube_obj, (temp_array[1], temp_array[0]))
            if matrix[p_r][p_c] == 3:
                SCREEN.blit(pink_cube_obj, (temp_array[1], temp_array[0]))
            if matrix[p_r][p_c] == 0:
                SCREEN.blit(white_cube_obj, (temp_array[1], temp_array[0]))

# ************************************ INITIALIZING BOARD ************************************


# ************************************ RULES OF THE GAME ************************************

# Blue is not on the frame of the pyramid
def blue_rule(row_value, col_value, width, height):
    if row_value == height - 1:
        return False
    y = int(width / 2)
    z = int(width / 2)
    for x in range(height - 1):
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
    if row_value == height - 1:  # In a case of a last row, check only the right, left, and up neighbors
        if col_value == 0:
            if matrix[row_value][col_value + 1] == 1:
                return False
            return True
        if col_value == width - 1:
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

# ************************************ RULES OF THE GAME ************************************


# page of the progress of the game
def start(matrix, width, height):
    pygame.display.set_caption("The pyramid game")
    icon = pygame.image.load('pyramid.png')
    pygame.display.set_icon(icon)
    while True:
        create_board_game(matrix, width, height)
        pygame.display.update()
        run_the_game(matrix, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


# Home page
def main_menu(matrix, width, height):
    pygame.display.set_caption("Menu")
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=pygame.image.load("play_blue.png"), x_pos=400, y_pos=300, text_input="")
        PLAY_BUTTON.update()  # Create the play button on the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start(matrix, width, height)
        pygame.display.update()


# Final page; possible to quit by pressing exit in the up right corner or play another game by press to REPLAY button
def end_of_game(matrix, width, height):
    create_board_game(matrix, width, height)
    # define the RGB value for white,
    # green, blue colour .
    background = (200, 200, 200)
    red = (200, 0, 0)
    blue = (0, 0, 128)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('congratulation, a solution is found', True, red, background)
    SCREEN.blit(text, (120, 450))
    pygame.display.set_caption("The pyramid game")
    icon = pygame.image.load('pyramid.png')
    pygame.display.set_icon(icon)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        REPLAY = Button(image=pygame.image.load("replay.png"), x_pos=390, y_pos=532, text_input="")
        REPLAY.update()  # Create the play button on the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY.checkForInput(MENU_MOUSE_POS):
                    start(matrix, width, height)
        pygame.display.update()


def run_the_game(matrix, width, height):
    create_first_matrix(matrix, width, height)
    print("starting board")
    print_matrix(matrix, 0, 0)
    yellows = init_yellows(matrix, width, height)
    counter = 1
    while counter != 0:
        counter = 0
        for r in range(height):
            for c in range(width):
                if pyramid_indices(r, c, width, height):
                    # For each pyramid's cell, check it's color and then determined if it necessary to randomize a new color
                    if matrix[r][c] == 1:  # If the cell is blue
                        blue_condition = blue_rule(r, c, width, height)
                        if not blue_condition:
                            matrix[r][c] = random.randint(2, 3)  # Random different value than 1
                            create_board_game(matrix, width, height)
                            pygame.display.update()
                            if matrix[r][c] == 2:  # If the new color is yellow so increase yellow[r] by 1
                                yellows[r] += 1
                            counter += 1
                        time.sleep(0.2)
                        print_matrix(matrix, r, c)
                    else:
                        if matrix[r][c] == 2:  # If the cell is yellow
                            yellow_condition = yellow_rule(r, yellows)
                            if not yellow_condition:
                                yellows[r] = 0
                                for j in range(width):  # Replace the colors in the whole row in the pyramid
                                    if pyramid_indices(r, j, width, height):
                                        matrix[r][j] = random.randint(1, 3)
                                        create_board_game(matrix, width, height)
                                        pygame.display.update()
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
                                    create_board_game(matrix, width, height)
                                    pygame.display.update()
                                    if matrix[r][c] == 2:  # If the new color is yellow so increase yellows[r] by 1
                                        yellows[r] += 1
                                    counter += 1
                                print_matrix(matrix, r, c)

    if counter == 0:
        end_of_game(matrix, width, height)


# It's possible to change w,h for harder or easier pyramid
# w is odd number
# def main():
w, h = 9, 5
new_matrix = [[0 for x in range(w)] for y in range(h)]
main_menu(new_matrix, w, h)

# if __name__ == "TomerReiss_ThePyramidGame":
#     main()




