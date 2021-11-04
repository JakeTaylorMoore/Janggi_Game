# Author:      Jacob Moore
# Date:        3/11/21
# Description: This program is a complete game of Janggi, or Korean Chess. It defines
#              classes for Board, Team, two team classes that inherit from team, Piece,
#              seven Piece classes that inherit from Team, and the JanggiGame class which
#              each of the other classes run through. This project is the final project for
#              CS 162 at Oregon State University.

########


class JanggiGame:
    """
    Definition for objects of the JanggiGame class. This class initializes the entire game and interacts
    with each other class defined in this file.
    """

    def __init__(self):
        self._board = Board()
        self._blue_turn = True
        self._red_team = Red()
        self._blue_team = Blue()
        self._red_pieces, self._blue_pieces = self._board.get_list_of_pieces()
        self._red_team.set_pieces(self._red_pieces)
        self._blue_team.set_pieces(self._blue_pieces)
        self._possible_moves_red = self._red_team.get_possible_moves(
            self._board)
        self._possible_moves_blue = self._blue_team.get_possible_moves(
            self._board)
        self._possible_moves_red_test = self._red_team.get_possible_moves_test(
            self._board)
        self._possible_moves_blue_test = self._blue_team.get_possible_moves_test(
            self._board)
        self._legal_moves_red = []
        self._legal_moves_blue = []

    def set_board(self, start_pos, end_pos):
        """
        Takes in positions and sends to board method set_board
        :param start_pos:
        :param end_pos:
        :return:
        """
        self._board.set_board(start_pos, end_pos)
        return True

    def get_legal_moves(self, team):
        """
        Takes in team color and returns legal moves for that team
        :param team:
        :return:
        """
        if team == 'blue':
            return self._legal_moves_blue
        else:
            return self._legal_moves_red

    def set_legal_moves(self, team):
        """
        Takes in team color and creates list of only legal moves out of possible moves dictionary
        :param team:
        :return:
        """
        if team == 'red':
            moves = self._possible_moves_red
            self._legal_moves_red = []
        else:
            moves = self._possible_moves_blue
            self._legal_moves_blue = []
        for key in moves:
            for position in moves[key]:
                if self.test_move_legality(key, position):
                    if team == 'red':
                        self._legal_moves_red.append([key, position])
                    else:
                        self._legal_moves_blue.append([key, position])
        return True

    @staticmethod
    def get_numbers_from_position(position):
        """
        Takes in a position and returns numbers that correspond to row and columns.
        :return:
        :param position:
        :return column_number, row_number:
        """
        # Letters list
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        # Dictionary with letters and their corresponding numbers
        letters_to_numbers = {'a': 1, 'b': 2, 'c': 3,
                              'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}
        # Create variable column_letter that is the 0 index of position variable
        column_letter = position[0]
        if column_letter in letters:
            # Create variable column_number that is the number corresponding to the letter
            column_number = letters_to_numbers[column_letter]
        else:
            return False
        # Create variable row_number that is the remainder of position passed in
        row_number = int(position[1:])
        if row_number not in range(1, 11):
            return False
        else:
            # Return both variables
            return column_number, row_number

    @staticmethod
    def get_position_from_numbers(column, row):
        """
        Takes in row and column integers and returns single string with board position
        :param row:
        :param column:
        :return:
        """
        # Create dictionary with numbers and corresponding letters
        numbers_to_letters = {1: 'a', 2: 'b', 3: 'c',
                              4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}
        # Check that numbers in range
        if column not in range(1, 10) or row not in range(1, 11):
            return False
        else:
            # Create variable position set to dictionary at column
            position = numbers_to_letters[column]
            # Concatenate position with string of row
            position += str(row)
            # Return position
            return position

    def update_possible_moves(self):
        """
        Updates each teams' possible moves after a turn is made.
        :return:
        """
        self._possible_moves_red = self._red_team.get_possible_moves(
            self._board)
        self._possible_moves_blue = self._blue_team.get_possible_moves(
            self._board)
        return True

    def update_possible_moves_test(self):
        """
        Updates each teams' possible moves after a turn is made.
        :return:
        """
        self._possible_moves_red_test = self._red_team.get_possible_moves_test(
            self._board)
        self._possible_moves_blue_test = self._blue_team.get_possible_moves_test(
            self._board)
        return True

    def get_board(self):
        """
        Returns board that has been initialized
        :return:
        """
        return self._board

    def get_game_state(self):
        """
        Returns whether someone has won the game or if it is unfinished
        :return:
        """
        if self.is_in_checkmate('blue'):
            return 'RED_WON'
        elif self.is_in_checkmate('red'):
            return 'BLUE_WON'
        else:
            return 'UNFINISHED'

    def is_in_check(self, team):
        """
        Returns True if the current player is in check or False if not
        :param team:
        :return:
        """
        in_check = False
        if team == 'blue':
            for piece in self._blue_pieces:
                if piece.get_initials() == 'bGN':
                    general = piece
            blue_general_position = general.get_position()
            for key, values in self._possible_moves_red_test.items():
                for value in values:
                    if blue_general_position == value:
                        in_check = True
        elif team == 'red':
            for piece in self._red_pieces:
                if piece.get_initials() == 'rGN':
                    general = piece
            red_general_position = general.get_position()
            for key, values in self._possible_moves_blue_test.items():
                for value in values:
                    if red_general_position == value:
                        in_check = True
        return in_check

    def test_move_legality(self, start_pos, end_pos):
        """
        Tests if a certain move would put team in check
        :return:
        """
        # Send in algebraic notation starting and ending positions.
        # Set start_column to letter and start_row to number sent in
        start_column = start_pos[0]
        start_row = int(start_pos[1:])
        # Set end_column to letter and end_row to number sent in.
        end_column = end_pos[0]
        end_row = int(end_pos[1:])

        # Decide which team is being tested for
        if self._board.get_board()[start_row][start_column].get_team_color() == 'r':
            team = 'red'
        else:
            team = 'blue'

        # Set Piece object at end's position to None since it has now been captured
        # This will not effect EmptySpace object since its position is already None
        self._board.get_board()[end_row][end_column].set_position(None)
        # Set Piece object at start's position to end position since it will now be there
        self._board.get_board()[start_row][start_column].set_position(end_pos)
        # Set board at end_row, end_column to board at start_row, start_column
        hold_end_object = self._board.get_board()[end_row][end_column]
        self._board.get_board()[end_row][end_column] = self._board.get_board()[
            start_row][start_column]
        # Set board at start_row, start_column to empty_space
        empty_space = EmptySpace()
        self._board.get_board()[start_row][start_column] = empty_space
        # Make sure to call update after set board
        self.update_possible_moves_test()

        if self.is_in_check(team):
            legal = False
        else:
            legal = True

        # Reversal of setting board
        self._board.get_board()[start_row][start_column] = self._board.get_board()[
            end_row][end_column]
        self._board.get_board()[end_row][end_column] = hold_end_object
        self._board.get_board()[end_row][end_column].set_position(end_pos)
        self._board.get_board()[
            start_row][start_column].set_position(start_pos)
        self.update_possible_moves_test()
        return legal

    def is_in_checkmate(self, team):
        """
        Returns True if the current player is in checkmate or False if not
        :param team:
        :return:
        """
        if self.is_in_check(team) and self.get_legal_moves(team) == []:
            return True
        else:
            return False

    def print_board(self):
        """
        Calls the print_board function for ongoing game
        :return:
        """
        self._board.print_board()
        return True

    def make_move(self, start_position, end_position):
        """
        Takes in start and end position of move. Verifies if each move is legal and then sends them to be set.
        :param start_position:
        :param end_position:
        :return:
        """
        # Create list variable to check if positions are in legal moves list
        moves_test = [start_position, end_position]
        # Every time function is called, it should update moves
        self.update_possible_moves()
        self.set_legal_moves('red')
        self.set_legal_moves('blue')
        # Check that game is unfinished
        if self.get_game_state() != 'UNFINISHED':
            print(self.get_game_state())
            return False
        # Check that the correct turn team is going
        blue_turn = self.get_blue_turn()
        start_piece = self._board.get_piece_in_position(start_position)
        start_team = start_piece.get_team_color()
        if start_team == 'r' and blue_turn is True:
            return False
        elif start_team == 'b' and blue_turn is False:
            return False
        # Check that moves are in the legal moves list
        if start_team == 'r' and moves_test in self._legal_moves_red:
            self.set_board(start_position, end_position)
            self.set_blue_turn()
            return True
        elif start_team == 'b' and moves_test in self._legal_moves_blue:
            self.set_board(start_position, end_position)
            self.set_blue_turn()
            return True
        else:
            return False

    def set_blue_turn(self):
        """
        If current team is blue, change to False, else change to True
        :return:
        """
        if self._blue_turn:
            self._blue_turn = False
        else:
            self._blue_turn = True

    def get_blue_turn(self):
        """
        Returns True if blue turn, false if red turn
        :return:
        """
        return self._blue_turn


class Board:
    """ Defines a class that creates a Janggi board to be interacted with by JanggiGame.
    Board is a nested dictionary with A-I Columns and 0-10 Rows,
    Initialized with instances of Piece objects in correct positions"""

    def __init__(self):
        # All letters of columns on board
        self._letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        # Define each piece in the game
        self._red_chariot_1 = Chariot('r', 'a1')
        self._red_chariot_2 = Chariot('r', 'i1')
        self._red_elephant_1 = Elephant('r', 'b1')
        self._red_elephant_2 = Elephant('r', 'g1')
        self._red_horse_1 = Horse('r', 'c1')
        self._red_horse_2 = Horse('r', 'h1')
        self._red_guard_1 = Guard('r', 'd1')
        self._red_guard_2 = Guard('r', 'f1')
        self._red_general = General('r', 'e2')
        self._red_cannon_1 = Cannon('r', 'b3')
        self._red_cannon_2 = Cannon('r', 'h3')
        self._red_soldier_1 = Soldier('r', 'a4')
        self._red_soldier_2 = Soldier('r', 'c4')
        self._red_soldier_3 = Soldier('r', 'e4')
        self._red_soldier_4 = Soldier('r', 'g4')
        self._red_soldier_5 = Soldier('r', 'i4')
        self._blue_chariot_1 = Chariot('b', 'a10')
        self._blue_chariot_2 = Chariot('b', 'i10')
        self._blue_elephant_1 = Elephant('b', 'b10')
        self._blue_elephant_2 = Elephant('b', 'g10')
        self._blue_horse_1 = Horse('b', 'c10')
        self._blue_horse_2 = Horse('b', 'h10')
        self._blue_guard_1 = Guard('b', 'd10')
        self._blue_guard_2 = Guard('b', 'f10')
        self._blue_general = General('b', 'e9')
        self._blue_cannon_1 = Cannon('b', 'b8')
        self._blue_cannon_2 = Cannon('b', 'h8')
        self._blue_soldier_1 = Soldier('b', 'a7')
        self._blue_soldier_2 = Soldier('b', 'c7')
        self._blue_soldier_3 = Soldier('b', 'e7')
        self._blue_soldier_4 = Soldier('b', 'g7')
        self._blue_soldier_5 = Soldier('b', 'i7')
        self._empty_space = EmptySpace()

        self._board = {
            1: {'a': self._red_chariot_1, 'b': self._red_elephant_1, 'c': self._red_horse_1, 'd': self._red_guard_1,
                'e': self._empty_space,
                'f': self._red_guard_2,
                'g': self._red_elephant_2, 'h': self._red_horse_2, 'i': self._red_chariot_2},
            2: {'a': self._empty_space, 'b': self._empty_space, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._red_general,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._empty_space, 'i': self._empty_space},
            3: {'a': self._empty_space, 'b': self._red_cannon_1, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._empty_space,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._red_cannon_2, 'i': self._empty_space},
            4: {'a': self._red_soldier_1, 'b': self._empty_space, 'c': self._red_soldier_2, 'd': self._empty_space,
                'e': self._red_soldier_3,
                'f': self._empty_space,
                'g': self._red_soldier_4, 'h': self._empty_space, 'i': self._red_soldier_5},
            5: {'a': self._empty_space, 'b': self._empty_space, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._empty_space,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._empty_space, 'i': self._empty_space},
            6: {'a': self._empty_space, 'b': self._empty_space, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._empty_space,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._empty_space, 'i': self._empty_space},
            7: {'a': self._blue_soldier_1, 'b': self._empty_space, 'c': self._blue_soldier_2, 'd': self._empty_space,
                'e': self._blue_soldier_3,
                'f': self._empty_space,
                'g': self._blue_soldier_4, 'h': self._empty_space, 'i': self._blue_soldier_5},
            8: {'a': self._empty_space, 'b': self._blue_cannon_1, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._empty_space,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._blue_cannon_2, 'i': self._empty_space},
            9: {'a': self._empty_space, 'b': self._empty_space, 'c': self._empty_space, 'd': self._empty_space,
                'e': self._blue_general,
                'f': self._empty_space,
                'g': self._empty_space, 'h': self._empty_space, 'i': self._empty_space},
            10: {'a': self._blue_chariot_1, 'b': self._blue_elephant_1, 'c': self._blue_horse_1,
                 'd': self._blue_guard_1, 'e': self._empty_space,
                 'f': self._blue_guard_2,
                 'g': self._blue_elephant_2, 'h': self._blue_horse_2, 'i': self._blue_chariot_2},
        }
        self._palace = [self._board[1]['d'], self._board[1]['e'], self._board[1]['f'],
                        self._board[2]['d'], self._board[2]['e'], self._board[2]['f'],
                        self._board[3]['d'], self._board[3]['e'], self._board[3]['f'],
                        self._board[8]['d'], self._board[8]['e'], self._board[8]['f'],
                        self._board[9]['d'], self._board[9]['e'], self._board[9]['f'],
                        self._board[10]['d'], self._board[10]['e'], self._board[10]['f'],
                        'd1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3',
                        'd8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']

        # Spaces where pieces can move along diagonal lines
        self._diagonal_spaces = ['d1', 'f1', 'e2', 'd3', 'f3',
                                 'd8', 'f8', 'e9', 'd10', 'f10']

    # Getter method returns board.
    def get_board(self):
        """
        Returns board in its current state
        :return:
        """
        return self._board

    def get_piece_in_position(self, position):
        """
        Returns instance of piece at given position
        :param position:
        :return:
        """
        column = position[0]
        row = int(position[1:])
        if column in self._letters and row in range(1, 11):
            return self._board[row][column]
        else:
            return False

    def get_list_of_pieces(self):
        """
        Iterates through board and returns a list containing all non-empty pieces
        :return:
        """
        red_pieces = []
        blue_pieces = []
        for key, value in self._board.items():
            for piece in value:
                if not value[piece].get_empty():
                    if value[piece].get_team_color() == 'r':
                        red_pieces.append(value[piece])
                    else:
                        blue_pieces.append(value[piece])
        return red_pieces, blue_pieces

    def get_position_initials(self, position):
        """
        Takes in position, and returns that position's get_initials method or None for empty space
        :param position:
        :return:
        """
        column = position[0]
        row = int(position[1:])
        if column in self._letters and row in range(1, 11):
            return self._board[row][column].get_initials()
        else:
            return False

    def get_position_team(self, position):
        """
        Takes in position, and returns that position's get_team_color method or None for empty space
        :param position:
        :return:
        """
        column = position[0]
        row = int(position[1:])
        if column in self._letters and row in range(1, 11):
            return self._board[row][column].get_team_color()
        else:
            return False

    # Setter method allows changes to the board
    def set_board(self, start_pos, end_pos):
        """
        Takes in starting position and ending position for a given move. Move must have been verified as legal
        before being sent.
        :param start_pos:
        :param end_pos:
        :return:
        """
        # Send in algebraic notation starting and ending positions.
        # Set start_column to letter and start_row to number sent in
        start_column = start_pos[0]
        start_row = int(start_pos[1:])
        # Set end_column to letter and end_row to number sent in.
        end_column = end_pos[0]
        end_row = int(end_pos[1:])
        # Set Piece object at end's position to None since it has now been captured
        # This will not effect EmptySpace object since its position is already None
        self._board[end_row][end_column].set_position(None)
        # Set Piece object at start's position to end position since it will now be there
        self._board[start_row][start_column].set_position(end_pos)
        # Set board at end_row, end_column to board at start_row, start_column
        self._board[end_row][end_column] = self._board[start_row][start_column]
        # Set board at start_row, start_column to empty_space
        self._board[start_row][start_column] = self._empty_space
        # Make sure to call update after set board
        return True

    def is_empty(self, position):
        """
        Position is sent in. Iterate through board and return if empty or not.
        :param position:
        :return:
        """
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        check_column = position[0]
        check_row = int(position[1:])
        if check_row not in range(1, 11) or check_column not in letters:
            return False
        else:
            return self._board[check_row][check_column].get_empty()

    def is_in_palace(self, position):
        """
        Position is sent in. Iterate through board and return whether space is in palace or not.
        :param position:
        :return:
        """
        if position in self._palace:
            return True
        else:
            return False

    def is_in_diagonal_space(self, position):
        """
        Position is sent in. Iterate through board and return whether space is in diagonal space or not.
        :param position:
        :return:
        """
        if position in self._diagonal_spaces:
            return True
        else:
            return False

    # Print method prints current board
    def print_board(self):
        """
        Prints board in its current state
        :return:
        """
        print("_" * 80)
        print(
            '    |   A       B       C       D       E       F       G       H       I   ')
        print('  1 ', end='')
        row_count = 2
        for i in self._board:
            for j in self._board[i]:
                if j == 'i':
                    print(self._board[i][j], end="|     \n")
                    if row_count < 10:
                        print('  ' + str(row_count) + ' ', end='')
                        row_count += 1
                    elif row_count == 10:
                        print(' ' + str(row_count) + ' ', end='')
                        row_count += 1
                else:
                    print(self._board[i][j], end="")
        print("_" * 80)
        return


class Team:
    """
    Definition for objects of the Team class. This class defines functions that are used by each individual team
    primarily for moving pieces and deciding which moves are possible.
    """

    def __init__(self):
        self._possible_moves = {}
        self._possible_moves_in_check = []
        self._color = ''
        self._pieces = []
        self._possible_moves_for_testing = {}

    def set_pieces(self, pieces_list):
        """
        Takes in a list of pieces and adds it to pieces list data member
        :param pieces_list:
        :return:
        """
        self._pieces = pieces_list
        return True

    def get_pieces(self):
        """
        Returns list of piece objects
        :return:
        """
        return self._pieces

    def get_color(self):
        """
        Returns team color. For red team, will return 'r', blue team will return 'b'.
        :return:
        """
        return self._color

    def get_possible_moves(self, board):
        """
        Returns list of possible moves
        :param board:
        :return:
        """
        for piece in self._pieces:
            if piece.get_possible_moves(board) is not None:
                self._possible_moves.update(piece.get_possible_moves(board))

        return self._possible_moves

    def get_possible_moves_test(self, board):
        """
        Returns list of possible moves
        :param board:
        :return:
        """
        for piece in self._pieces:
            if piece.get_possible_moves(board) is not None:
                self._possible_moves_for_testing.update(
                    piece.get_possible_moves(board))

        return self._possible_moves_for_testing


class Red(Team):
    """
    This defines objects of the red class which inherits from Team. The functions used by this class are inherited from
    Team. Through Team, this class interacts with JanggiGame and each individual piece class.
    """

    def __init__(self):
        super().__init__()
        self._color = 'r'


class Blue(Team):
    """
    This defines objects of the Red class which inherits from Team. The functions used by this class are inherited from
    Team. Through Team, this class interacts with JanggiGame and each individual piece class.
    """

    def __init__(self):
        super().__init__()
        self._color = 'b'


class EmptySpace:
    """
    Defines objects of the EmptySpace class, which is used on the board to represent an empty space
    """

    def __init__(self):
        self._position = None
        self._printable = "|-------"
        self._empty = True
        self._initials = None
        self._team_color = None

    def __repr__(self):
        """
        Returns how the space will be represented on the Board.
        :return:
        """
        return f'{self._printable}'

    def set_position(self, position):
        """
        Takes in parameter position and continues to set position to None so that error won't be raised on iterations
        :param position:
        :return:
        """
        self._position = None

    def get_position(self):
        """
        Returns position, which is always none
        :return:
        """
        return self._position

    def get_empty(self):
        """
        Returns status of tile, whether empty or not
        :return:
        """
        return self._empty

    def get_printable(self):
        """
        Returns how the space will be represented on the Board.
        :return:
        """
        return self._printable

    def get_initials(self):
        """
        Returns initials which in this case is a None value
        :return:
        """
        return self._initials

    def get_team_color(self):
        """
        Returns team color, which is None for empty space
        :return:
        """
        return self._team_color


class Piece:
    """
    Defines objects of the Piece class. Parent class for all game pieces. Color is input
    and assigned for team. This is represented by a character string r or b.
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        self._team_color = color
        self._position = position
        self._initials = ''
        self._empty = False
        self._column_num, self._row_num = JanggiGame.get_numbers_from_position(
            position)

    def __repr__(self):
        """
        Returns how the space will be represented on the Board.
        :return:
        """
        return f'{self._printable}'

    def get_team_color(self):
        """
        Returns single character string representing team color
        :return:
        """
        return self._team_color

    def get_position(self):
        """
        Returns current position of Piece
        :return:
        """
        return self._position

    def set_position(self, new_position):
        """
        Sets position to new input position
        :param new_position:
        :return:
        """
        self._position = new_position
        # Also set numbers to new position
        if new_position is None:
            self._column_num = None
            self._row_num = None
        else:
            self._column_num, self._row_num = JanggiGame.get_numbers_from_position(
                new_position)
        return True

    def get_position_numbers(self):
        """
        Returns column and row corresponding numbers for position
        :return:
        """
        return self._column_num, self._row_num

    def get_initials(self):
        """
        Returns three letter initials string for piece.
        :return:
        """
        return self._initials

    def get_possible_moves(self, board):
        """
        Uses position to determine all current possible moves. Creates a dictionary with these moves, with
        starting position as key and possible moves from there as values. Appends this dictionary to
        the possible_moves dictionary of its team. Parent class method is defined for Guard and General.
        :param board:
        :return:
        """
        # Create list to append legal_moves to and list for testing moves
        legal_moves = []
        if self.get_position() is None:
            moves_dict = None

        else:
            # Moves one space left or right, one space diagonally, or one backwards or forwards only in palace
            if self.get_team_color() == 'r':
                left_move = [self._column_num + 1, self._row_num]
                right_move = [self._column_num - 1, self._row_num]
                forward_move = [self._column_num, self._row_num + 1]
                backward_move = [self._column_num, self._row_num - 1]
                test_moves = [left_move, right_move,
                              forward_move, backward_move]
                if board.is_in_diagonal_space(self.get_position()):
                    diagonal_right = [self._column_num - 1, self._row_num + 1]
                    diagonal_left = [self._column_num + 1, self._row_num + 1]
                    back_diag_right = [self._column_num - 1, self._row_num - 1]
                    back_diag_left = [self._column_num + 1, self._row_num - 1]
                    test_moves.append(diagonal_right)
                    test_moves.append(diagonal_left)
                    test_moves.append(back_diag_right)
                    test_moves.append(back_diag_left)

                # Iterate through test moves. If move fails test, set that variable to None
                for i in test_moves:
                    # Create alpha numeric variable of position
                    j = JanggiGame.get_position_from_numbers(i[0], i[1])
                    if not board.is_in_palace(j):
                        j = None
                    if j is not None:
                        # Next check to be sure that position isn't filled by piece of same team
                        if board.get_position_team(j) == 'r':
                            j = None
                        # If both of these tests passed, append to list
                        else:
                            legal_moves.append(j)

            # Moves one space left or right, one space diagonally, or one backwards or forwards only in palace
            if self.get_team_color() == 'b':
                left_move = [self._column_num - 1, self._row_num]
                right_move = [self._column_num + 1, self._row_num]
                forward_move = [self._column_num, self._row_num - 1]
                backward_move = [self._column_num, self._row_num + 1]
                test_moves = [left_move, right_move,
                              forward_move, backward_move]
                if board.is_in_diagonal_space(self.get_position()):
                    diagonal_right = [self._column_num + 1, self._row_num + 1]
                    diagonal_left = [self._column_num - 1, self._row_num + 1]
                    back_diag_right = [self._column_num + 1, self._row_num - 1]
                    back_diag_left = [self._column_num - 1, self._row_num - 1]
                    test_moves.append(diagonal_right)
                    test_moves.append(diagonal_left)
                    test_moves.append(back_diag_right)
                    test_moves.append(back_diag_left)

                # Iterate through test moves. If move fails test, set that variable to None
                for i in test_moves:
                    # Create alpha numeric variable of position
                    j = JanggiGame.get_position_from_numbers(i[0], i[1])
                    if not board.is_in_palace(j):
                        j = None
                    if j is not None:
                        # Next check to be sure that position isn't filled by piece of same team
                        if board.get_position_team(j) == 'b':
                            j = None
                        # If both of these tests passed, append to list
                        else:
                            legal_moves.append(j)

            # Add starting position to legal_moves list so that skipping turn is an option
            legal_moves.append(self._position)
            # Create dictionary with key starting_position, values legal moves
            moves_dict = {self._position: legal_moves}
        return moves_dict

    def get_empty(self):
        """
        Returns status of tile, whether empty or not. Any piece will be False
        :return:
        """
        return self._empty


class General(Piece):
    """
    Defines objects of the General class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'GN'
        self._printable = "|- " + self._initials + " -"


class Guard(Piece):
    """
    Defines objects of the Guard class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'gd'
        self._printable = "|- " + self._initials + " -"


class Horse(Piece):
    """
    Defines objects of the Horse class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'hr'
        self._printable = "|- " + self._initials + " -"

    def get_possible_moves(self, board):
        """
        Uses position to determine all current possible moves. Creates a dictionary with these moves, with
        starting position as key and possible moves from there as values. Appends this dictionary to
        the possible_moves dictionary of its team.
        :param board:
        :return:
        """
        # Create list to append legal_moves to and list for testing moves
        legal_moves = []
        if self.get_position() is None:
            moves_dict = None

        else:
            # Moves one space forward, sideways, or backwards and then one space diagonally
            # Also set variables to alpha numeric positions
            if self.get_team_color() == 'r':
                left_move = [self._column_num + 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num - 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num + 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num - 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                # If position is empty and position is on board, check diagonals.
                if left_move_alpha:
                    if board.is_empty(left_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        left_up = [left_move[0] + 1, left_move[1] + 1]
                        left_up_alpha = JanggiGame.get_position_from_numbers(
                            left_up[0], left_up[1])
                        # If end position is empty and on board, append to legal moves list
                        if left_up_alpha:
                            if board.get_position_team(left_up_alpha) != 'r':
                                legal_moves.append(left_up_alpha)
                        left_down = [left_move[0] + 1, left_move[1] - 1]
                        left_down_alpha = JanggiGame.get_position_from_numbers(
                            left_down[0], left_down[1])
                        # If end position is empty and on board, append to legal moves list
                        if left_down_alpha:
                            if board.get_position_team(left_down_alpha) != 'r':
                                legal_moves.append(left_down_alpha)
                if right_move_alpha:
                    if board.is_empty(right_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        right_up = [right_move[0] - 1, right_move[1] + 1]
                        right_up_alpha = JanggiGame.get_position_from_numbers(
                            right_up[0], right_up[1])
                        # If end position is empty and on board, append to legal moves list
                        if right_up_alpha:
                            if board.get_position_team(right_up_alpha) != 'r':
                                legal_moves.append(right_up_alpha)
                        right_down = [right_move[0] - 1, right_move[1] - 1]
                        right_down_alpha = JanggiGame.get_position_from_numbers(
                            right_down[0], right_down[1])
                        if right_down_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(right_down_alpha) != 'r':
                                legal_moves.append(right_down_alpha)
                if forward_move_alpha:
                    if board.is_empty(forward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        forward_left = [
                            forward_move[0] + 1, forward_move[1] + 1]
                        forward_left_alpha = JanggiGame.get_position_from_numbers(
                            forward_left[0], forward_left[1])
                        if forward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(forward_left_alpha) != 'r':
                                legal_moves.append(forward_left_alpha)
                        forward_right = [
                            forward_move[0] - 1, forward_move[1] + 1]
                        forward_right_alpha = JanggiGame.get_position_from_numbers(
                            forward_right[0], forward_right[1])
                        if forward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(forward_right_alpha) != 'r':
                                legal_moves.append(forward_right_alpha)
                if backward_move_alpha:
                    if board.is_empty(backward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        backward_left = [
                            backward_move[0] + 1, backward_move[1] - 1]
                        backward_left_alpha = JanggiGame.get_position_from_numbers(
                            backward_left[0], backward_left[1])
                        if backward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(backward_left_alpha) != 'r':
                                legal_moves.append(backward_left_alpha)
                        backward_right = [
                            backward_move[0] - 1, backward_move[1] - 1]
                        backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                    backward_right[1])
                        if backward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(backward_right_alpha) != 'r':
                                legal_moves.append(backward_right_alpha)

            # Moves one space forward, sideways, or backwards and then one space diagonally
            if self.get_team_color() == 'b':
                left_move = [self._column_num - 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num + 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num - 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num + 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                if left_move_alpha:
                    # If position is empty and position is on board, check diagonals.
                    if board.is_empty(left_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        left_up = [left_move[0] - 1, left_move[1] - 1]
                        left_up_alpha = JanggiGame.get_position_from_numbers(
                            left_up[0], left_up[1])
                        if left_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(left_up_alpha) != 'b':
                                legal_moves.append(left_up_alpha)
                        left_down = [left_move[0] - 1, left_move[1] + 1]
                        left_down_alpha = JanggiGame.get_position_from_numbers(
                            left_down[0], left_down[1])
                        if left_down_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(left_down_alpha) != 'b':
                                legal_moves.append(left_down_alpha)
                if right_move_alpha:
                    if board.is_empty(right_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        right_up = [right_move[0] + 1, right_move[1] - 1]
                        right_up_alpha = JanggiGame.get_position_from_numbers(
                            right_up[0], right_up[1])
                        if right_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(right_up_alpha) != 'b':
                                legal_moves.append(right_up_alpha)
                        right_down = [right_move[0] + 1, right_move[1] + 1]
                        right_down_alpha = JanggiGame.get_position_from_numbers(
                            right_down[0], right_down[1])
                        if right_down_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(right_down_alpha) != 'b':
                                legal_moves.append(right_down_alpha)
                if forward_move_alpha:
                    if board.is_empty(forward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        forward_left = [
                            forward_move[0] - 1, forward_move[1] - 1]
                        forward_left_alpha = JanggiGame.get_position_from_numbers(
                            forward_left[0], forward_left[1])
                        if forward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(forward_left_alpha) != 'b':
                                legal_moves.append(forward_left_alpha)
                        forward_right = [
                            forward_move[0] + 1, forward_move[1] - 1]
                        forward_right_alpha = JanggiGame.get_position_from_numbers(
                            forward_right[0], forward_right[1])
                        if forward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(forward_right_alpha) != 'b':
                                legal_moves.append(forward_right_alpha)
                if backward_move_alpha:
                    if board.is_empty(backward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        backward_left = [
                            backward_move[0] - 1, backward_move[1] + 1]
                        backward_left_alpha = JanggiGame.get_position_from_numbers(
                            backward_left[0], backward_left[1])
                        if backward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(backward_left_alpha) != 'b':
                                legal_moves.append(backward_left_alpha)
                        backward_right = [
                            backward_move[0] + 1, backward_move[1] + 1]
                        backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                    backward_right[1])
                        if backward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.get_position_team(backward_right_alpha) != 'b':
                                legal_moves.append(backward_right_alpha)

            # Append start position to list and create dictionary with key as start position
            legal_moves.append(self.get_position())
            moves_dict = {self.get_position(): legal_moves}
        return moves_dict


class Elephant(Piece):
    """
    Defines objects of the Elephant class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'el'
        self._printable = "|- " + self._initials + " -"

    def get_possible_moves(self, board):
        """
        Uses position to determine all current possible moves. Creates a dictionary with these moves, with
        starting position as key and possible moves from there as values. Appends this dictionary to
        the possible_moves dictionary of its team.
        :param board:
        :return:
        """
        if self.get_position() is None:
            moves_dict = None

        else:
            # Create list to append legal_moves to and list for testing moves
            legal_moves = []

            # Moves one space forward, sideways, or backwards and then two spaces diagonally
            # Also set variables to alpha numeric positions
            if self.get_team_color() == 'r':
                left_move = [self._column_num + 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num - 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num + 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num - 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                if left_move_alpha:
                    # If position is empty and position is on board, check diagonals.
                    if board.is_empty(left_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        left_up = [left_move[0] + 1, left_move[1] + 1]
                        left_up_alpha = JanggiGame.get_position_from_numbers(
                            left_up[0], left_up[1])
                        if left_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(left_up_alpha):
                                # Variables for diagonals and alpha numeric positions
                                left_up_again = [
                                    left_up[0] + 1, left_up[1] + 1]
                                left_up_again_alpha = JanggiGame.get_position_from_numbers(left_up_again[0],
                                                                                           left_up_again[1])
                                if left_up_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(left_up_again_alpha) != 'r':
                                        legal_moves.append(left_up_again_alpha)
                        left_down = [left_move[0] + 1, left_move[1] - 1]
                        left_down_alpha = JanggiGame.get_position_from_numbers(
                            left_down[0], left_down[1])
                        if left_down_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(left_down_alpha):
                                # Variables for diagonals and alpha numeric positions
                                left_down_again = [
                                    left_down[0] + 1, left_down[1] - 1]
                                left_down_again_alpha = JanggiGame.get_position_from_numbers(left_down_again[0],
                                                                                             left_down_again[1])
                                if left_down_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(left_down_again_alpha) != 'r':
                                        legal_moves.append(
                                            left_down_again_alpha)
                if right_move_alpha:
                    if board.is_empty(right_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        right_up = [right_move[0] - 1, right_move[1] + 1]
                        right_up_alpha = JanggiGame.get_position_from_numbers(
                            right_up[0], right_up[1])
                        if right_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(right_up_alpha):
                                right_up_again = [
                                    right_up[0] - 1, right_up[1] + 1]
                                right_up_again_alpha = JanggiGame.get_position_from_numbers(right_up_again[0],
                                                                                            right_up_again[1])
                                if right_up_again_alpha:
                                    if board.get_position_team(right_up_again_alpha) != 'r':
                                        legal_moves.append(
                                            right_up_again_alpha)
                        right_down = [right_move[0] - 1, right_move[1] - 1]
                        right_down_alpha = JanggiGame.get_position_from_numbers(
                            right_down[0], right_down[1])
                        # If end position is empty and on board, append to legal moves list
                        if right_down_alpha:
                            if board.is_empty(right_down_alpha):
                                right_down_again = [
                                    right_down[0] - 1, right_down[1] - 1]
                                right_down_again_alpha = JanggiGame.get_position_from_numbers(right_down_again[0],
                                                                                              right_down_again[1])
                                if right_down_again_alpha:
                                    if board.get_position_team(right_down_again_alpha) != 'r':
                                        legal_moves.append(
                                            right_down_again_alpha)
                if forward_move_alpha:
                    if board.is_empty(forward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        forward_left = [
                            forward_move[0] + 1, forward_move[1] + 1]
                        forward_left_alpha = JanggiGame.get_position_from_numbers(
                            forward_left[0], forward_left[1])
                        if forward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(forward_left_alpha):
                                forward_left_again = [
                                    forward_left[0] + 1, forward_left[1] + 1]
                                forward_left_again_alpha = JanggiGame.get_position_from_numbers(forward_left_again[0],
                                                                                                forward_left_again[1])
                                if forward_left_again_alpha:
                                    if board.get_position_team(forward_left_again_alpha) != 'r':
                                        legal_moves.append(
                                            forward_left_again_alpha)
                        forward_right = [
                            forward_move[0] - 1, forward_move[1] + 1]
                        forward_right_alpha = JanggiGame.get_position_from_numbers(
                            forward_right[0], forward_right[1])
                        if forward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(forward_right_alpha):
                                forward_right_again = [
                                    forward_right[0] - 1, forward_right[1] + 1]
                                forward_right_again_alpha = JanggiGame.get_position_from_numbers(forward_right_again[0],
                                                                                                 forward_right_again[1])
                                if forward_right_again_alpha:
                                    if board.get_position_team(forward_right_again_alpha) != 'r':
                                        legal_moves.append(
                                            forward_right_again_alpha)
                if backward_move_alpha:
                    if board.is_empty(backward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        backward_left = [
                            backward_move[0] + 1, backward_move[1] - 1]
                        backward_left_alpha = JanggiGame.get_position_from_numbers(
                            backward_left[0], backward_left[1])
                        if backward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(backward_left_alpha):
                                backward_left_again = [
                                    backward_left[0] + 1, backward_left[1] - 1]
                                backward_left_again_alpha = JanggiGame.get_position_from_numbers(backward_left_again[0],
                                                                                                 backward_left_again[1])
                                if backward_left_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(backward_left_again_alpha) != 'r':
                                        legal_moves.append(
                                            backward_left_again_alpha)
                        backward_right = [
                            backward_move[0] - 1, backward_move[1] - 1]
                        backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                    backward_right[1])
                        if backward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(backward_right_alpha):
                                backward_right_again = [
                                    backward_right[0] - 1, backward_right[1] - 1]
                                backward_right_again_alpha = JanggiGame.get_position_from_numbers(
                                    backward_right_again[0], backward_right_again[1])
                                if backward_right_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(backward_right_again_alpha) != 'r':
                                        legal_moves.append(
                                            backward_right_again_alpha)

            # Moves one space forward, sideways, or backwards and then two spaces diagonally
            # Also set variables to alpha numeric positions
            if self.get_team_color() == 'b':
                left_move = [self._column_num - 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num + 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num - 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num + 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                if left_move_alpha:
                    # If position is empty and position is on board, check diagonals.
                    if board.is_empty(left_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        left_up = [left_move[0] - 1, left_move[1] - 1]
                        left_up_alpha = JanggiGame.get_position_from_numbers(
                            left_up[0], left_up[1])
                        if left_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(left_up_alpha):
                                # Variables for diagonals and alpha numeric positions
                                left_up_again = [
                                    left_up[0] - 1, left_up[1] - 1]
                                left_up_again_alpha = JanggiGame.get_position_from_numbers(left_up_again[0],
                                                                                           left_up_again[1])
                                if left_up_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(left_up_again_alpha) != 'b':
                                        legal_moves.append(left_up_again_alpha)
                        left_down = [left_move[0] - 1, left_move[1] + 1]
                        left_down_alpha = JanggiGame.get_position_from_numbers(
                            left_down[0], left_down[1])
                        if left_down_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(left_down_alpha):
                                # Variables for diagonals and alpha numeric positions
                                left_down_again = [
                                    left_down[0] - 1, left_down[1] + 1]
                                left_down_again_alpha = JanggiGame.get_position_from_numbers(left_down_again[0],
                                                                                             left_down_again[1])
                                if left_down_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(left_down_again_alpha) != 'b':
                                        legal_moves.append(
                                            left_down_again_alpha)
                if right_move_alpha:
                    if board.is_empty(right_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        right_up = [right_move[0] + 1, right_move[1] - 1]
                        right_up_alpha = JanggiGame.get_position_from_numbers(
                            right_up[0], right_up[1])
                        if right_up_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(right_up_alpha):
                                right_up_again = [
                                    right_up[0] + 1, right_up[1] - 1]
                                right_up_again_alpha = JanggiGame.get_position_from_numbers(right_up_again[0],
                                                                                            right_up_again[1])
                                if right_up_again_alpha:
                                    if board.get_position_team(right_up_again_alpha) != 'b':
                                        legal_moves.append(
                                            right_up_again_alpha)
                        right_down = [right_move[0] + 1, right_move[1] + 1]
                        right_down_alpha = JanggiGame.get_position_from_numbers(
                            right_down[0], right_down[1])
                        # If end position is empty and on board, append to legal moves list
                        if right_down_alpha:
                            if board.is_empty(right_down_alpha):
                                right_down_again = [
                                    right_down[0] + 1, right_down[1] + 1]
                                right_down_again_alpha = JanggiGame.get_position_from_numbers(right_down_again[0],
                                                                                              right_down_again[1])
                                if right_down_again_alpha:
                                    if board.get_position_team(right_down_again_alpha) != 'b':
                                        legal_moves.append(
                                            right_down_again_alpha)
                if forward_move_alpha:
                    if board.is_empty(forward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        forward_left = [
                            forward_move[0] - 1, forward_move[1] - 1]
                        forward_left_alpha = JanggiGame.get_position_from_numbers(
                            forward_left[0], forward_left[1])
                        if forward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(forward_left_alpha):
                                forward_left_again = [
                                    forward_left[0] - 1, forward_left[1] - 1]
                                forward_left_again_alpha = JanggiGame.get_position_from_numbers(forward_left_again[0],
                                                                                                forward_left_again[1])
                                if forward_left_again_alpha:
                                    if board.get_position_team(forward_left_again_alpha) != 'b':
                                        legal_moves.append(
                                            forward_left_again_alpha)
                        forward_right = [
                            forward_move[0] + 1, forward_move[1] - 1]
                        forward_right_alpha = JanggiGame.get_position_from_numbers(
                            forward_right[0], forward_right[1])
                        if forward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(forward_right_alpha):
                                forward_right_again = [
                                    forward_right[0] + 1, forward_right[1] - 1]
                                forward_right_again_alpha = JanggiGame.get_position_from_numbers(forward_right_again[0],
                                                                                                 forward_right_again[1])
                                if forward_right_again_alpha:
                                    if board.get_position_team(forward_right_again_alpha) != 'b':
                                        legal_moves.append(
                                            forward_right_again_alpha)
                if backward_move_alpha:
                    if board.is_empty(backward_move_alpha):
                        # Variables for diagonals and alpha numeric positions
                        backward_left = [
                            backward_move[0] - 1, backward_move[1] + 1]
                        backward_left_alpha = JanggiGame.get_position_from_numbers(
                            backward_left[0], backward_left[1])
                        if backward_left_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(backward_left_alpha):
                                backward_left_again = [
                                    backward_left[0] - 1, backward_left[1] + 1]
                                backward_left_again_alpha = JanggiGame.get_position_from_numbers(backward_left_again[0],
                                                                                                 backward_left_again[1])
                                if backward_left_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(backward_left_again_alpha) != 'b':
                                        legal_moves.append(
                                            backward_left_again_alpha)
                        backward_right = [
                            backward_move[0] + 1, backward_move[1] + 1]
                        backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                    backward_right[1])
                        if backward_right_alpha:
                            # If end position is empty and on board, append to legal moves list
                            if board.is_empty(backward_right_alpha):
                                backward_right_again = [
                                    backward_right[0] + 1, backward_right[1] + 1]
                                backward_right_again_alpha = JanggiGame.get_position_from_numbers(
                                    backward_right_again[0], backward_right_again[1])
                                if backward_right_again_alpha:
                                    # If end position is empty and on board, append to legal moves list
                                    if board.get_position_team(backward_right_again_alpha) != 'b':
                                        legal_moves.append(
                                            backward_right_again_alpha)

            # Append start position to list and create dictionary with key as start position
            legal_moves.append(self.get_position())
            moves_dict = {self.get_position(): legal_moves}
        return moves_dict


class Chariot(Piece):
    """
    Defines objects of the  class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'ch'
        self._printable = "|- " + self._initials + " -"

    def get_possible_moves(self, board):
        # Set legal_moves list to empty list
        legal_moves = []
        is_in_diagonal_spaces = board.is_in_diagonal_space(self.get_position())
        if self.get_position() is None:
            moves_dict = None

        else:
            # Moves one space forward, sideways, or backwards and then two spaces diagonally
            # Also set variables to alpha numeric positions
            if self.get_team_color() == 'r':
                left_move = [self._column_num + 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num - 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num + 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num - 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])

                if is_in_diagonal_spaces:
                    # If it is in diagonal spaces, create variables forward_right, backward_right,
                    # backward_left, forward_left (and alpha versions) that are the current position plus
                    # or minus numbers that would take it diagonally that direction
                    forward_right = [self._column_num - 1, self._row_num + 1]
                    forward_right_alpha = JanggiGame.get_position_from_numbers(
                        forward_right[0], forward_right[1])
                    backward_right = [self._column_num - 1, self._row_num - 1]
                    backward_right_alpha = JanggiGame.get_position_from_numbers(
                        backward_right[0], backward_right[1])
                    backward_left = [self._column_num + 1, self._row_num - 1]
                    backward_left_alpha = JanggiGame.get_position_from_numbers(
                        backward_left[0], backward_left[1])
                    forward_left = [self._column_num + 1, self._row_num + 1]
                    forward_left_alpha = JanggiGame.get_position_from_numbers(
                        forward_left[0], forward_left[1])

                    # while forward right and while forward right alpha is in palace
                    while forward_right_alpha and board.is_in_palace(forward_right_alpha):
                        # Check if empty
                        if board.is_empty(forward_right_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(forward_right_alpha)
                            forward_right = [
                                forward_right[0] - 1, forward_right[1] + 1]
                            forward_right_alpha = JanggiGame.get_position_from_numbers(forward_right[0],
                                                                                       forward_right[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(forward_right_alpha) == 'r':
                            # If same team, set move to false
                            forward_right_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(forward_right_alpha)
                            forward_right_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while backward_right_alpha and board.is_in_palace(backward_right_alpha):
                        # Check if empty
                        if board.is_empty(backward_right_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(backward_right_alpha)
                            backward_right = [
                                backward_right[0] - 1, backward_right[1] - 1]
                            backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                        backward_right[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(backward_right_alpha) == 'r':
                            # If same team, set move to false
                            backward_right_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(backward_right_alpha)
                            backward_right_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while backward_left_alpha and board.is_in_palace(backward_left_alpha):
                        # Check if empty
                        if board.is_empty(backward_left_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(backward_left_alpha)
                            backward_left = [
                                backward_left[0] + 1, backward_left[1] - 1]
                            backward_left_alpha = JanggiGame.get_position_from_numbers(backward_left[0],
                                                                                       backward_left[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(backward_left_alpha) == 'r':
                            # If same team, set move to false
                            backward_left_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(backward_left_alpha)
                            backward_left_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while forward_left_alpha and board.is_in_palace(forward_left_alpha):
                        # Check if empty
                        if board.is_empty(forward_left_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(forward_left_alpha)
                            forward_left = [
                                forward_left[0] + 1, forward_left[1] + 1]
                            forward_left_alpha = JanggiGame.get_position_from_numbers(
                                forward_left[0], forward_left[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(forward_left_alpha) == 'r':
                            # If same team, set move to false
                            forward_left_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(forward_left_alpha)
                            forward_left_alpha = False

                # while forward alpha is true
                while forward_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(forward_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(forward_move_alpha)
                        forward_move = [forward_move[0], forward_move[1] + 1]
                        forward_move_alpha = JanggiGame.get_position_from_numbers(
                            forward_move[0], forward_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(forward_move_alpha) == 'r':
                        # If same team, set move to false
                        forward_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(forward_move_alpha)
                        forward_move_alpha = False

                # while right alpha is true
                while right_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(right_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(right_move_alpha)
                        right_move = [right_move[0] - 1, right_move[1]]
                        right_move_alpha = JanggiGame.get_position_from_numbers(
                            right_move[0], right_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(right_move_alpha) == 'r':
                        # If same team, set move to false
                        right_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(right_move_alpha)
                        right_move_alpha = False

                # while backward alpha is true
                while backward_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(backward_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(backward_move_alpha)
                        backward_move = [
                            backward_move[0], backward_move[1] - 1]
                        backward_move_alpha = JanggiGame.get_position_from_numbers(
                            backward_move[0], backward_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(backward_move_alpha) == 'r':
                        # If same team, set move to false
                        backward_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(backward_move_alpha)
                        backward_move_alpha = False

                # while left alpha is true
                while left_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(left_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(left_move_alpha)
                        left_move = [left_move[0] + 1, left_move[1]]
                        left_move_alpha = JanggiGame.get_position_from_numbers(
                            left_move[0], left_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(left_move_alpha) == 'r':
                        # If same team, set move to false
                        left_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(left_move_alpha)
                        left_move_alpha = False

            # Moves one space forward, sideways, or backwards and then two spaces diagonally
            # Also set variables to alpha numeric positions
            if self.get_team_color() == 'b':
                left_move = [self._column_num - 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num + 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num - 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num + 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])

                if is_in_diagonal_spaces:
                    # If it is in palace, create variables forward_right, backward_right,
                    # backward_left, forward_left (and alpha versions) that are the current position plus
                    # or minus numbers that would take it diagonally that direction
                    forward_right = [self._column_num + 1, self._row_num - 1]
                    forward_right_alpha = JanggiGame.get_position_from_numbers(
                        forward_right[0], forward_right[1])
                    backward_right = [self._column_num + 1, self._row_num + 1]
                    backward_right_alpha = JanggiGame.get_position_from_numbers(
                        backward_right[0], backward_right[1])
                    backward_left = [self._column_num - 1, self._row_num + 1]
                    backward_left_alpha = JanggiGame.get_position_from_numbers(
                        backward_left[0], backward_left[1])
                    forward_left = [self._column_num - 1, self._row_num - 1]
                    forward_left_alpha = JanggiGame.get_position_from_numbers(
                        forward_left[0], forward_left[1])

                    # while forward right and while forward right alpha is in palace
                    while forward_right_alpha and board.is_in_palace(forward_right_alpha):
                        # Check if empty
                        if board.is_empty(forward_right_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(forward_right_alpha)
                            forward_right = [
                                forward_right[0] + 1, forward_right[1] - 1]
                            forward_right_alpha = JanggiGame.get_position_from_numbers(forward_right[0],
                                                                                       forward_right[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(forward_right_alpha) == 'b':
                            # If same team, set move to false
                            forward_right_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(forward_right_alpha)
                            forward_right_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while backward_right_alpha and board.is_in_palace(backward_right_alpha):
                        # Check if empty
                        if board.is_empty(backward_right_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(backward_right_alpha)
                            backward_right = [
                                backward_right[0] + 1, backward_right[1] + 1]
                            backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                        backward_right[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(backward_right_alpha) == 'b':
                            # If same team, set move to false
                            backward_right_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(backward_right_alpha)
                            backward_right_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while backward_left_alpha and board.is_in_palace(backward_left_alpha):
                        # Check if empty
                        if board.is_empty(backward_left_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(backward_left_alpha)
                            backward_left = [
                                backward_left[0] - 1, backward_left[1] + 1]
                            backward_left_alpha = JanggiGame.get_position_from_numbers(backward_left[0],
                                                                                       backward_left[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(backward_left_alpha) == 'b':
                            # If same team, set move to false
                            backward_left_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(backward_left_alpha)
                            backward_left_alpha = False

                    # while forward right and while forward right alpha is in palace
                    while forward_left_alpha and board.is_in_palace(forward_left_alpha):
                        # Check if empty
                        if board.is_empty(forward_left_alpha):
                            # If empty, append position and add iteration of move
                            legal_moves.append(forward_left_alpha)
                            forward_left = [
                                forward_left[0] - 1, forward_left[1] - 1]
                            forward_left_alpha = JanggiGame.get_position_from_numbers(
                                forward_left[0], forward_left[1])
                        # If not check if it is the same team as piece
                        elif board.get_position_team(forward_left_alpha) == 'b':
                            # If same team, set move to false
                            forward_left_alpha = False
                        # If different team, append move to list and then set to false
                        else:
                            legal_moves.append(forward_left_alpha)
                            forward_left_alpha = False

                # while forward alpha is true
                while forward_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(forward_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(forward_move_alpha)
                        forward_move = [forward_move[0], forward_move[1] - 1]
                        forward_move_alpha = JanggiGame.get_position_from_numbers(
                            forward_move[0], forward_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(forward_move_alpha) == 'b':
                        # If same team, set move to false
                        forward_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(forward_move_alpha)
                        forward_move_alpha = False

                # while right alpha is true
                while right_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(right_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(right_move_alpha)
                        right_move = [right_move[0] + 1, right_move[1]]
                        right_move_alpha = JanggiGame.get_position_from_numbers(
                            right_move[0], right_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(right_move_alpha) == 'b':
                        # If same team, set move to false
                        right_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(right_move_alpha)
                        right_move_alpha = False

                # while backward alpha is true
                while backward_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(backward_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(backward_move_alpha)
                        backward_move = [
                            backward_move[0], backward_move[1] + 1]
                        backward_move_alpha = JanggiGame.get_position_from_numbers(
                            backward_move[0], backward_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(backward_move_alpha) == 'b':
                        # If same team, set move to false
                        backward_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(backward_move_alpha)
                        backward_move_alpha = False

                # while left alpha is true
                while left_move_alpha:
                    # If it is, check if empty
                    if board.is_empty(left_move_alpha):
                        # If empty append to legal_moves and add another iteration of move and create another alpha version
                        legal_moves.append(left_move_alpha)
                        left_move = [left_move[0] - 1, left_move[1]]
                        left_move_alpha = JanggiGame.get_position_from_numbers(
                            left_move[0], left_move[1])
                    # If not empty, check team.
                    elif board.get_position_team(left_move_alpha) == 'b':
                        # If same team, set move to false
                        left_move_alpha = False
                    # If different team, append to legal_moves list and set move to false
                    else:
                        legal_moves.append(left_move_alpha)
                        left_move_alpha = False

            # Append start position to list and create dictionary with key as start position
            legal_moves.append(self.get_position())
            moves_dict = {self.get_position(): legal_moves}
        return moves_dict


class Cannon(Piece):
    """
    Defines objects of the Cannon class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'cn'
        self._printable = "|- " + self._initials + " -"

    def get_possible_moves(self, board):

        # Set legal_moves list to empty list
        legal_moves = []
        # Check if start position is in palace
        board.is_in_palace(self.get_position())
        if self.get_position() is None:
            moves_dict = None

        else:
            # If get team from position is 'r'
            if board.get_position_team(self.get_position()) == 'r':
                # Create variables forward, right, backward, left (and alpha versions) that are the
                # current position plus or minus numbers that would take it that direction
                left_move = [self._column_num + 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num - 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num + 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num - 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                # Check if start position is in palace
                is_in_palace = board.is_in_palace(self.get_position())

                # If it is in palace, create variables forward_right, backward_right,
                # backward_left, forward_left (and alpha versions) that are the current position plus
                # or minus numbers that would take it diagonally that direction
                forward_right = [self._column_num - 1, self._row_num + 1]
                forward_right_alpha = JanggiGame.get_position_from_numbers(
                    forward_right[0], forward_right[1])
                backward_right = [self._column_num - 1, self._row_num - 1]
                backward_right_alpha = JanggiGame.get_position_from_numbers(
                    backward_right[0], backward_right[1])
                backward_left = [self._column_num + 1, self._row_num - 1]
                backward_left_alpha = JanggiGame.get_position_from_numbers(
                    backward_left[0], backward_left[1])
                forward_left = [self._column_num + 1, self._row_num + 1]
                forward_left_alpha = JanggiGame.get_position_from_numbers(
                    forward_left[0], forward_left[1])

                # If in palace...
                if is_in_palace:

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while forward_right alpha
                    while forward_right_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(forward_right_alpha):
                                # If empty, iterate to next move
                                forward_right_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(forward_right_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                forward_right_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                forward_right = [
                                    forward_right[0] - 1, forward_right[1] + 1]
                                forward_right_alpha = JanggiGame.get_position_from_numbers(forward_right[0],
                                                                                           forward_right[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(forward_right_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(forward_right_alpha)
                                forward_right_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(forward_right_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    forward_right_alpha).get_team_color() == 'r':
                                # If piece is one of these, set move to False
                                forward_right_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(forward_right_alpha)
                                forward_right_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while backward_right alpha
                    while backward_right_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(backward_right_alpha):
                                # If empty, iterate to next move
                                backward_right_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(backward_right_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                backward_right_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                backward_right = [
                                    backward_right[0] - 1, backward_right[1] - 1]
                                backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                            backward_right[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(backward_right_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(backward_right_alpha)
                                backward_right_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(backward_right_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    backward_right_alpha).get_team_color() == 'r':
                                # If piece is one of these, set move to False
                                backward_right_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(backward_right_alpha)
                                backward_right_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while backward_left alpha
                    while backward_left_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(backward_left_alpha):
                                # If empty, iterate to next move
                                backward_left_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(backward_left_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                backward_left_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                backward_left = [
                                    backward_left[0] + 1, backward_left[1] - 1]
                                backward_left_alpha = JanggiGame.get_position_from_numbers(backward_left[0],
                                                                                           backward_left[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(backward_left_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(backward_left_alpha)
                                backward_left_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(backward_left_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    backward_left_alpha).get_team_color() == 'r':
                                # If piece is one of these, set move to False
                                backward_left_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(backward_left_alpha)
                                backward_left_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while forward_left alpha
                    while forward_left_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(forward_left_alpha):
                                # If empty, iterate to next move
                                forward_left_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(forward_left_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                forward_left_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                forward_left = [
                                    forward_left[0] + 1, forward_left[1] + 1]
                                forward_left_alpha = JanggiGame.get_position_from_numbers(forward_left[0],
                                                                                          forward_left[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(forward_left_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(forward_left_alpha)
                                forward_left_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(forward_left_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(forward_left_alpha).get_team_color() == 'r':
                                # If piece is one of these, set move to False
                                forward_left_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(forward_left_alpha)
                                forward_left_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while forward_move alpha
                while forward_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(forward_move_alpha):
                            # If empty, iterate again, set new alpha
                            forward_move = [
                                forward_move[0], forward_move[1] + 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(forward_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            forward_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            forward_move = [
                                forward_move[0], forward_move[1] + 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(forward_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(forward_move_alpha)
                            forward_move = [
                                forward_move[0], forward_move[1] + 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(forward_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(forward_move_alpha).get_team_color() == 'r':
                            # If piece is one of these, set move to False
                            forward_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(forward_move_alpha)
                            forward_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while right_move alpha
                while right_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(right_move_alpha):
                            # If empty, iterate again, set new alpha
                            right_move = [right_move[0] - 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(right_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            right_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            right_move = [right_move[0] - 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(right_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(right_move_alpha)
                            right_move = [right_move[0] - 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(right_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(right_move_alpha).get_team_color() == 'r':
                            # If piece is one of these, set move to False
                            right_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(right_move_alpha)
                            right_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while backward_move alpha
                while backward_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(backward_move_alpha):
                            # If empty, iterate again, set new alpha
                            backward_move = [
                                backward_move[0], backward_move[1] + 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(backward_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            backward_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            backward_move = [
                                backward_move[0], backward_move[1] + 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(backward_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(backward_move_alpha)
                            backward_move = [
                                backward_move[0], backward_move[1] + 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(backward_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(backward_move_alpha).get_team_color() == 'r':
                            # If piece is one of these, set move to False
                            backward_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(backward_move_alpha)
                            backward_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while left_move alpha
                while left_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(left_move_alpha):
                            # If empty, iterate again, set new alpha
                            left_move = [left_move[0] + 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(left_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            left_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            left_move = [left_move[0] + 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(left_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(left_move_alpha)
                            left_move = [left_move[0] + 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(left_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(left_move_alpha).get_team_color() == 'r':
                            # If piece is one of these, set move to False
                            left_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(left_move_alpha)
                            left_move_alpha = False

            # If get team from position is 'b'
            if board.get_position_team(self.get_position()) == 'b':
                # Create variables forward, right, backward, left (and alpha versions) that are the
                # current position plus or minus numbers that would take it that direction
                left_move = [self._column_num - 1, self._row_num]
                left_move_alpha = JanggiGame.get_position_from_numbers(
                    left_move[0], left_move[1])
                right_move = [self._column_num + 1, self._row_num]
                right_move_alpha = JanggiGame.get_position_from_numbers(
                    right_move[0], right_move[1])
                forward_move = [self._column_num, self._row_num - 1]
                forward_move_alpha = JanggiGame.get_position_from_numbers(
                    forward_move[0], forward_move[1])
                backward_move = [self._column_num, self._row_num + 1]
                backward_move_alpha = JanggiGame.get_position_from_numbers(
                    backward_move[0], backward_move[1])
                # Check if start position is in palace
                is_in_palace = board.is_in_palace(self.get_position())

                # If it is in palace, create variables forward_right, backward_right,
                # backward_left, forward_left (and alpha versions) that are the current position plus
                # or minus numbers that would take it diagonally that direction
                forward_right = [self._column_num + 1, self._row_num - 1]
                forward_right_alpha = JanggiGame.get_position_from_numbers(
                    forward_right[0], forward_right[1])
                backward_right = [self._column_num + 1, self._row_num + 1]
                backward_right_alpha = JanggiGame.get_position_from_numbers(
                    backward_right[0], backward_right[1])
                backward_left = [self._column_num - 1, self._row_num + 1]
                backward_left_alpha = JanggiGame.get_position_from_numbers(
                    backward_left[0], backward_left[1])
                forward_left = [self._column_num - 1, self._row_num - 1]
                forward_left_alpha = JanggiGame.get_position_from_numbers(
                    forward_left[0], forward_left[1])

                # If in palace...
                if is_in_palace:

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while forward_right alpha
                    while forward_right_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(forward_right_alpha):
                                # If empty, iterate to next move
                                forward_right_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(forward_right_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                forward_right_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                forward_right = [
                                    forward_right[0] + 1, forward_right[1] - 1]
                                forward_right_alpha = JanggiGame.get_position_from_numbers(forward_right[0],
                                                                                           forward_right[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(forward_right_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(forward_right_alpha)
                                forward_right_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(forward_right_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    forward_right_alpha).get_team_color() == 'b':
                                # If piece is one of these, set move to False
                                forward_right_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(forward_right_alpha)
                                forward_right_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while backward_right alpha
                    while backward_right_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(backward_right_alpha):
                                # If empty, iterate to next move
                                backward_right_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(backward_right_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                backward_right_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                backward_right = [
                                    backward_right[0] + 1, backward_right[1] + 1]
                                backward_right_alpha = JanggiGame.get_position_from_numbers(backward_right[0],
                                                                                            backward_right[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(backward_right_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(backward_right_alpha)
                                backward_right_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(backward_right_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    backward_right_alpha).get_team_color() == 'b':
                                # If piece is one of these, set move to False
                                backward_right_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(backward_right_alpha)
                                backward_right_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while backward_left alpha
                    while backward_left_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(backward_left_alpha):
                                # If empty, iterate to next move
                                backward_left_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(backward_left_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                backward_left_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                backward_left = [
                                    backward_left[0] - 1, backward_left[1] + 1]
                                backward_left_alpha = JanggiGame.get_position_from_numbers(backward_left[0],
                                                                                           backward_left[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(backward_left_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(backward_left_alpha)
                                backward_left_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(backward_left_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(
                                    backward_left_alpha).get_team_color() == 'b':
                                # If piece is one of these, set move to False
                                backward_left_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(backward_left_alpha)
                                backward_left_alpha = False

                    # Set variable jump_piece to False
                    jump_piece = False
                    # while forward_left alpha
                    while forward_left_alpha:
                        # If jump_piece is false, cannon has not found jump piece yet
                        if not jump_piece:
                            # Check if empty
                            if board.is_empty(forward_left_alpha):
                                # If empty, iterate to next move
                                forward_left_alpha = False
                            # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                            # then use Piece's get initials method and check if last two characters are 'cn')
                            elif board.get_piece_in_position(forward_left_alpha).get_initials()[1:] == 'cn':
                                # If cannon, set move to false
                                forward_left_alpha = False
                            # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                            else:
                                jump_piece = True
                                forward_left = [
                                    forward_left[0] - 1, forward_left[1] - 1]
                                forward_left_alpha = JanggiGame.get_position_from_numbers(forward_left[0],
                                                                                          forward_left[1])
                        # If jump_piece is True
                        else:
                            # Check if empty
                            if board.is_empty(forward_left_alpha):
                                # If empty, append move alpha to list and set move to false
                                legal_moves.append(forward_left_alpha)
                                forward_left_alpha = False
                            # If not empty, check if piece occupying is other team OR if piece is cannon
                            elif board.get_piece_in_position(forward_left_alpha).get_initials()[
                                    1:] == 'cn' or board.get_piece_in_position(forward_left_alpha).get_team_color() == 'b':
                                # If piece is one of these, set move to False
                                forward_left_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                            else:
                                legal_moves.append(forward_left_alpha)
                                forward_left_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while forward_move alpha
                while forward_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(forward_move_alpha):
                            # If empty, iterate again, set new alpha
                            forward_move = [
                                forward_move[0], forward_move[1] - 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(forward_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            forward_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            forward_move = [
                                forward_move[0], forward_move[1] - 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(forward_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(forward_move_alpha)
                            forward_move = [
                                forward_move[0], forward_move[1] - 1]
                            forward_move_alpha = JanggiGame.get_position_from_numbers(
                                forward_move[0], forward_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(forward_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(forward_move_alpha).get_team_color() == 'b':
                            # If piece is one of these, set move to False
                            forward_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(forward_move_alpha)
                            forward_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while right_move alpha
                while right_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(right_move_alpha):
                            # If empty, iterate again, set new alpha
                            right_move = [right_move[0] + 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(right_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            right_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            right_move = [right_move[0] + 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(right_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(right_move_alpha)
                            right_move = [right_move[0] + 1, right_move[1]]
                            right_move_alpha = JanggiGame.get_position_from_numbers(
                                right_move[0], right_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(right_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(right_move_alpha).get_team_color() == 'b':
                            # If piece is one of these, set move to False
                            right_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(right_move_alpha)
                            right_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while backward_move alpha
                while backward_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(backward_move_alpha):
                            # If empty, iterate again, set new alpha
                            backward_move = [
                                backward_move[0], backward_move[1] - 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(backward_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            backward_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            backward_move = [
                                backward_move[0], backward_move[1] - 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(backward_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(backward_move_alpha)
                            backward_move = [
                                backward_move[0], backward_move[1] - 1]
                            backward_move_alpha = JanggiGame.get_position_from_numbers(backward_move[0],
                                                                                       backward_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(backward_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(backward_move_alpha).get_team_color() == 'b':
                            # If piece is one of these, set move to False
                            backward_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(backward_move_alpha)
                            backward_move_alpha = False

                # Set variable jump_piece to False
                jump_piece = False
                # while left_move alpha
                while left_move_alpha:
                    # If jump_piece is false, cannon has not found jump piece yet
                    if not jump_piece:
                        # Check if empty
                        if board.is_empty(left_move_alpha):
                            # If empty, iterate again, set new alpha
                            left_move = [left_move[0] - 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])
                        # If not empty, check to see if piece is a cannon (use board's get piece from position method,
                        # then use Piece's get initials method and check if last two characters are 'cn')
                        elif board.get_piece_in_position(left_move_alpha).get_initials()[1:] == 'cn':
                            # If cannon, set move to false
                            left_move_alpha = False
                        # If not cannon, set jump_piece to True and then iterate again and reset variable alpha
                        else:
                            jump_piece = True
                            left_move = [left_move[0] - 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])
                    # If jump_piece is True
                    else:
                        # Check if empty
                        if board.is_empty(left_move_alpha):
                            # If empty, append position alpha to list. Then iterate again and set new alpha
                            legal_moves.append(left_move_alpha)
                            left_move = [left_move[0] - 1, left_move[1]]
                            left_move_alpha = JanggiGame.get_position_from_numbers(
                                left_move[0], left_move[1])

                        # If not empty, check if piece occupying is other team OR if piece is cannon
                        elif board.get_piece_in_position(left_move_alpha).get_initials()[
                                1:] == 'cn' or board.get_piece_in_position(left_move_alpha).get_team_color() == 'b':
                            # If piece is one of these, set move to False
                            left_move_alpha = False
                            # If piece is not one of those, append move to list and set move to False
                        # If piece is not one of those, append move to list and set move to False
                        else:
                            legal_moves.append(left_move_alpha)
                            left_move_alpha = False

            # Append start position to list and create dictionary with key as start position
            legal_moves.append(self.get_position())
            moves_dict = {self.get_position(): legal_moves}
        return moves_dict


class Soldier(Piece):
    """
    Defines objects of the Soldier class which inherits from the Piece class. This
    object represents a playable piece from a Janggi Game and will interact with the
    Board class
    :param color:
    :param position:
    """

    def __init__(self, color, position):
        super().__init__(color, position)
        self._initials = self._team_color + 'sr'
        self._printable = "|- " + self._initials + " -"

    def get_possible_moves(self, board):
        """
        Check through all possible moves for Piece and append these to possible moves dictionary
        :param board:
        :return:
        """
        # Variable to check if piece is starting in palace
        in_palace = board.is_in_palace(self.get_position())

        # Create list to append legal_moves to and list for testing moves
        legal_moves = []
        if self.get_position() is None:
            moves_dict = None

        else:
            # Moves one space left or right, or one space forward only unless in palace
            if self.get_team_color() == 'r':
                left_move = [self._column_num + 1, self._row_num]
                right_move = [self._column_num - 1, self._row_num]
                forward_move = [self._column_num, self._row_num + 1]
                test_moves = [left_move, right_move, forward_move]
                # Diagonal tests if piece in palace. Get alpha numeric position from numbers. If start and end
                # positions are in palace, add end position to test_moves list
                if in_palace:
                    diagonal_right = [self._column_num - 1, self._row_num + 1]
                    diagonal_left = [self._column_num + 1, self._row_num + 1]
                    diagonal_right_alpha = JanggiGame.get_position_from_numbers(
                        diagonal_right[0], diagonal_right[1])
                    diagonal_left_alpha = JanggiGame.get_position_from_numbers(
                        diagonal_left[0], diagonal_left[1])
                    if board.is_in_palace(diagonal_right_alpha):
                        test_moves.append(diagonal_right)
                    if board.is_in_palace(diagonal_left_alpha):
                        test_moves.append(diagonal_left)
                # Iterate through test moves. If move fails test, set that variable to None
                for i in test_moves:
                    # First check that new position is on the board
                    if i[0] not in range(1, 10) or i[1] not in range(1, 11):
                        i = None
                    if i is not None:
                        # Next check to be sure that position isn't filled by piece of same team
                        if board.get_position_team(JanggiGame.get_position_from_numbers(i[0], i[1])) == 'r':
                            i = None
                        # If both of these tests passed, append to list
                        else:
                            legal_moves.append(
                                JanggiGame.get_position_from_numbers(i[0], i[1]))

            # Moves one space left or right, or one space forward only unless in palace
            if self.get_team_color() == 'b':
                left_move = [self._column_num - 1, self._row_num]
                right_move = [self._column_num + 1, self._row_num]
                forward_move = [self._column_num, self._row_num - 1]
                test_moves = [left_move, right_move, forward_move]
                # Diagonal tests if piece in palace. Get alpha numeric position from numbers. If start and end
                # positions are in palace, add end position to test_moves list
                if in_palace:
                    diagonal_right = [self._column_num + 1, self._row_num - 1]
                    diagonal_left = [self._column_num - 1, self._row_num - 1]
                    diagonal_right_alpha = JanggiGame.get_position_from_numbers(
                        diagonal_right[0], diagonal_right[1])
                    diagonal_left_alpha = JanggiGame.get_position_from_numbers(
                        diagonal_left[0], diagonal_left[1])
                    if board.is_in_palace(diagonal_right_alpha):
                        test_moves.append(diagonal_right)
                    if board.is_in_palace(diagonal_left_alpha):
                        test_moves.append(diagonal_left)
                # Iterate through test moves. If move fails test, set that variable to None
                for i in test_moves:
                    # First check that new position is on the board
                    if i[0] not in range(1, 10) or i[1] not in range(1, 11):
                        i = None
                    if i:
                        # Next check to be sure that position isn't filled by piece of same team
                        if board.get_position_team(JanggiGame.get_position_from_numbers(i[0], i[1])) == 'b':
                            i = None
                        # If both of these tests passed, append to list
                        else:
                            legal_moves.append(
                                JanggiGame.get_position_from_numbers(i[0], i[1]))
            # Add starting position to legal_moves list so that skipping turn is an option
            legal_moves.append(self._position)
            # Create dictionary with key starting_position, values legal moves
            moves_dict = {self._position: legal_moves}
        return moves_dict


def main():
    # pass
    game = JanggiGame()
    # move_result = game.make_move('c1', 'e3')  # should be False because it's not Red's turn
    # move_result = game.make_move('a7', 'b7')  # should return True
    # game.print_board()
    # blue_in_check = game.is_in_check('blue')  # should return False
    # game.make_move('a4', 'a5')  # should return True
    # state = game.get_game_state()  # should return UNFINISHED
    # print(state)
    # print(game.make_move('b7', 'b6'))  # should return True
    # print(game.make_move('b3', 'b6'))  # should return False because it's an invalid move
    # print(game.make_move('a1', 'a4'))  # should return True
    # print(game.make_move('c7', 'd7'))  # should return True
    # print(game.make_move('a4', 'a4'))  # this will pass the Red's turn and return True


if __name__ == '__main__':
    main()
