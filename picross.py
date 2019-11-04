#Ana Perdiz - nr 2
#Luis Rodrigues - nr 21
#Pedro Moura - nr 24
##################### ADT position 

def make_position(r, c):
    if(isinstance(r, int) and r >= 1 and isinstance(c, int) and c >= 1):
        return (r,c)        
    else:
        raise ValueError("make_position: invalid arguments")

def position_row(pos):
    return pos[0]

def position_column(pos):
    return pos[1]

def is_position(p): 
    return(isinstance(p, tuple) and len(p) == 2 and isinstance(position_row(p), int) and position_row(p) >= 1 and isinstance(position_column(p), int) and position_column(p) >= 1)

def equal_positions(p1, p2):
    return(position_row(p1) == position_row(p2) and position_column(p1) == position_column(p2))

def position_to_string(p):
    return "(" + str(position_row(p)) + " : " + str(position_column(p)) +")"

##################### ADT board
# example tuple: (((2; ); (3; ); (2; ); (2; 2); (2; )); ((2; ); (1; 2); (2; ); (3; ); (3; )))
# board --> {'specification': (), 'grid': []} --> dictionary containing two elements: a tuple w/ the specification and the board's grid/matrix

def isvalid_spec_param(t): #aux: validates if all nested tuple elements are integers and >= 1 
    for el in t:
        if isinstance(el, tuple):
            for nestedel in el:
                if not isinstance(nestedel, int) or nestedel < 1:
                    return False
        else:
            return False
    return True

def isvalid_spec(s):
    return isinstance(s, tuple) and len(s) == 2 and isinstance(s[0], tuple) and isvalid_spec_param(s[0]) and isinstance(s[1], tuple) and isvalid_spec_param(s[1])

def make_board(s): # s is a tuple
    if isvalid_spec(s):
        board = {}
        #creates specification part
        board['specification'] = s
        #creates the grid part
        grid = []
        nrows = len(s[0])
        ncols = len(s[1])
        i = 0
        #possible grid cells values: '?' -> empty; '.' -> white; 'x' -> black 
        while i < nrows:
            grid.append(['?'] * ncols)
            i = i + 1        
        board['grid'] = grid
        return board
    else:
        raise ValueError('make_board: invalid arguments')

def board_dimensions(b):
    spec = b['specification']
    return (len(spec[0]), len(spec[1]))

def board_specification(b): 
    return b['specification']

############# not necessary maybe
def board_grid(b):
    return b['grid']
#############

def board_cell(b, p): 
    if(is_board(b) and is_position(p)):
        cell = b['grid'][position_row(p) -1][position_column(p) -1] #-1 because positions are equal to the matrix's indexes +1
        if(cell == '?'):        #empty
            return 0
        elif(cell == '.'):      #white
            return 1
        else:                   #black
            return 2    
    else:
        raise ValueError('board_cell: invalid arguments')

def board_fill_cell(b, p, num): #test this
    if(is_board(b) and is_position(p) and (num in [0, 1, 2])):
        value = ""
        if num == 0:
            value = "?"
        elif num == 1:
            value = "."
        else:
            value = "x"
        b['grid'][position_row(p) - 1][position_column(p) - 1] = value #-1 because positions are equal to the matrix's indexes +1
        return b
    else:
        raise ValueError('board_fill_cell: invalid arguments')

def is_board(b):
    return isinstance(b, dict) and len(b) == 2 and 'specification' in b and 'grid' in b and isvalid_spec(board_specification(b)) and isinstance(board_grid(b), list) and len(board_specification(b)[0]) == len(board_grid(b)) and len(board_specification(b)[1]) == len(board_grid(b)[0])

######################## use previous abstractions from here on
def board_full(b):     
    nrows, ncols = board_dimensions(b)
    
    for row in range(nrows):
        for col in range(ncols):
            p = make_position(row + 1, col + 1)
            if board_cell(b, p) == 0:
                return False
    return True

### validate against spec ### FINISH THIS w/ ABSTRACTION

def sum_tup(t):
    sum_t = 0
    sums = []
    for el in t:
        for num in el:
            sum_t = sum_t + num
        sums.append(sum_t)
        sum_t = 0
    return tuple(sums)

def validate_board_against_spec(b): #returns True or False
    nrows, ncols = board_dimensions(b)
    spec_rows, spec_cols = board_specification(b)
    # validate rows
    sum_x_rows = 0
    sums_rows = []
    for row in range(nrows):
        sum_x_rows = 0    
        for col in range(ncols):
            p = make_position(row + 1, col + 1)
            cell = board_cell(b, p)
            if cell == 2:
                sum_x_rows = sum_x_rows + 1
        sums_rows.append(sum_x_rows)
    #validate columns
    sum_x_cols = 0
    sums_cols = []
    for row in range(nrows):
        sum_x_cols = 0    
        for col in range(ncols):
            p = make_position(col + 1, row + 1)
            cell = board_cell(b, p)
            if cell == 2:
                sum_x_cols = sum_x_cols + 1
        sums_cols.append(sum_x_cols)

    
    if sum_tup(spec_rows) == tuple(sums_rows) and sum_tup(spec_cols) == tuple(sums_cols):
        return True
    else:
        return False
    
def board_finished(b): #board full + board is valid == winning condition
    return board_full(b) and validate_board_against_spec(b)

##############################

def max_len(t): #aux
    maxlen = 0
    for i in t:
        len_i = len(i)
        if len_i > maxlen:
            len_i, maxlen = maxlen, len_i
    return maxlen

def print_top_board(s): #aux
    sub_s = s[1]
    top_str = ""
    i = max_len(sub_s)

    while i > 0:
        for el in sub_s:
            if(len(el) - i) < 0:
                top_str = top_str + "     "
            else:
                top_str = top_str + "  " + str(el[len(el) - i]) + "  "
        top_str = top_str + "\n"
        i = i - 1  
    return top_str

def print_grid_board(b): #aux
    matrix = ""
    sub_r = board_specification(b)[0]
    nrows, ncols = board_dimensions(b)
    max_sub_r = max_len(sub_r)

    for row in range(nrows):
        matrix = matrix + "\n"
        for col in range(ncols):
            p = make_position(row + 1, col + 1)
            cell = board_cell(b, p)
            value = ""
            if cell == 0:
                value = "?"
            elif cell == 1:
                value = "."
            else:
                value = "x"
            matrix = matrix + "[ " + value + " ]"
        for el in sub_r[row]:                                                                  
            matrix = matrix + " " + str(el) 
        matrix = matrix + "  " * (max_sub_r - len(sub_r[row])) + " |"
    return matrix[1:]

def board_to_string(b): 
    if is_board(b):
        spec = board_specification(b)
        return print_top_board(spec) + print_grid_board(b)
    else:
        raise ValueError("board_to_string: invalid arguments")

def print_board(b): # takes up string form board_to_string and simply prints it
    print(board_to_string(b))


##################### ADT board 

import os 

def read_board(filename): #works
    if os.path.isfile(filename): #check if file exists
        with open(filename, 'r') as f:
            spec = eval(f.readline()) #read first line of file and turn it into python code: str -> tuple 
            if isvalid_spec(spec):
                return spec
            else:
                raise ValueError("read_board: string in file is an invalid specification")
    else:
        raise ValueError("read_board: file not found")

def is_valid_coords(list_coords):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for el in list_coords:
        if el == '':
            return False
        else:
            for digit in el:
                if digit not in digits:
                    return False
    return True

def validate_play_pos(b):
    nrows, ncols = board_dimensions(b)
    max_pos = make_position(nrows, ncols)
    enter_cell_str = "- enter the cell position (between (1 : 1) and " + position_to_string(max_pos) + ") >> "

    enter_cell_input = input(enter_cell_str).strip("()").replace(" ", "")

    if ":" in enter_cell_input:    
        enter_cell_coords = enter_cell_input.split(":")
    else:
        print("Invalid position")
        return validate_play_pos(b)

    if is_valid_coords(enter_cell_coords):
        cell_play_pos = make_position(int(enter_cell_coords[0]), int(enter_cell_coords[1]))
        if is_position(cell_play_pos) and position_row(cell_play_pos) <= nrows and position_column(cell_play_pos) <= ncols:  
            return cell_play_pos
        else:
            print("Invalid position")
            return validate_play_pos(b)
    else:
        print("Invalid position")
        return validate_play_pos(b)

def validate_play_value():
    value = input("- enter the value >> ")
    if value not in ["1", "2"]:
        print("Invalid value")
        return validate_play_value()
    else:
        value = int(value)
        return value

def ask_for_play(b): #works
    print("\nEnter the next play")
    cell_play_pos = validate_play_pos(b)
    value = validate_play_value()
    return (cell_play_pos, value)

#### main function
def picross_game(filename): 
    board = make_board(read_board(filename))
    print("\nPicross Game\n")
    while not board_full(board):
        print_board(board)
        play = ask_for_play(board)
        play_pos = play[0]
        play_value = play[1]
        
        board = board_fill_cell(board, play_pos, play_value)

    if board_finished(board):
        print("Picross Game: You won! Congratulations :)")
    else:
        print("Picross Game: You lost ... :(")
    
    return board_finished(board)


########################### tests
#picross_game("jogo_fig1.txt")






