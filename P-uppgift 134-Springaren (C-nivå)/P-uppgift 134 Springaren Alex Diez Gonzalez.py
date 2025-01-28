"""
Författare: Alexander Diez Gonzalez
Datum: 2022-04-10
Ev. revisionsdatum: YYYY-MM-DD
"""

import os
import json
from numpy import *


class Board:
    """
    Alla attribut:
    tiles: Lista med schackbrädets rutor, en samling av typen dict
    board_tiles: Nästlad lista (matris) på schackbrädets rutor inklusive buffertrutor, en samling av typen list
    med element av typen dict
    knight_position: Sträng på springarens nuvarande position
    horizontal_tiles: Sträng för rutornas namngivning på brädet i horisontell led
    vertical_tiles: Sträng för rutornas namngivning på brädet i vertikal led
    position_list: Lista på schackbrädets rutor som springaren har vandrat på
    position_counter: Räknare för antalet positioner springaren vandrat på
    correct_position_list: Lista på springarens korrekta möjliga positioner att gå till
    board_coordinate_y: Springarens koordinat-position i vertikal led
    board_coordinate_x: Springarens koordinat-position i horisontell led
    """

    def __init__(self):
        self.tiles = {}
        self.board_tiles = []
        self.knight_position = ""
        self.vertical_tiles: str = "ABCDEFGH"
        self.horizontal_tiles: str = "87654321"
        self.position_list = []
        self.position_counter = 0
        self.correct_position_list = []
        self.board_coordinate_x = 0
        self.board_coordinate_y = 0

    def get_tiles_dict_from_file(self):
        """
        Hämtar listan på schackbrädets rutor från en extern JSON-fil
        """
        tiles_dir = os.path.dirname(__file__)
        tiles_path = os.path.join(tiles_dir, "tiles_dict.json")
        with open(tiles_path) as dict_file:
            self.tiles = json.load(dict_file)
            dict_file.close()

    def update_tiles_dict(self):
        """
        Uppdaterar listan på schackbrädets rutor
        """
        self.tiles.update({self.knight_position: self.position_counter})

    def get_board_list_from_file(self):
        """
        Hämtar listan på schackbrädets rutor inklusive buffertrutor från en extern JSON-fil
        """
        board_tiles_dir = os.path.dirname(__file__)  # Get the directory of the script
        board_tiles_path = os.path.join(board_tiles_dir, "board_list.json")
        with open(board_tiles_path) as list_file:
            self.board_tiles = json.load(list_file)
            list_file.close()

    def update_board_list(self):
        """
        Uppdaterar listan på schackbrädets rutor inklusive buffertrutor
        """
        self.board_tiles[self.board_coordinate_x][self.board_coordinate_y] = {
            self.knight_position: self.position_counter}

    def valid_move(self):
        """
        Flyttar springaren ett steg till en giltig ruta
        """
        move = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for position in move:
            # Hitta alla möjliga rutor för springaren
            new_move = self.board_tiles[self.board_coordinate_x + position[0]][
                self.board_coordinate_y + position[1]]

            if new_move.get(str(new_move)[2:4]) == 0:
                # Om springaren ej har varit här, bygg på korrekta listan
                self.correct_position_list.append(str(new_move)[2:4])
        next_random_position = self.random_position()

        if next_random_position > -1:
            # Springaren har möjligt att flytta ett steg till en giltig ruta
            self.knight_position = self.correct_position_list[next_random_position]
            self.position_list.append(self.knight_position)
            self.position_counter += 1
            self.board_coordinate_x = self.horizontal_tiles.index(self.knight_position[1:]) + 2
            self.board_coordinate_y = self.vertical_tiles.index(self.knight_position[:1]) + 2
            # Uppdatera/rensa listorna och upprepa metoden
            self.update_tiles_dict()
            self.update_board_list()
            self.correct_position_list.clear()
            self.valid_move()
        else:
            # Springaren har slut på giltiga rutor att flytta till
            self.board_print(1)
            print(f"\nSpringaren vandrade från startrutan \"{self.position_list[0]}\""
                  f" till slutrutan \"{self.position_list[len(self.position_list) - 1]}\""
                  f" och besökte totalt {self.position_counter} unika rutor i schackbrädet.")

    def knight_journey(self):
        """
        Flyttar springaren genom schackbrädet om användaren matar in en startposition
        """
        self.position_list.append(self.knight_position)
        self.position_counter += 1
        self.board_coordinate_x = self.horizontal_tiles.index(self.knight_position[1:]) + 2
        self.board_coordinate_y = self.vertical_tiles.index(self.knight_position[:1]) + 2
        self.update_tiles_dict()
        self.update_board_list()
        self.valid_move()

    def random_position(self):
        """
        Slumpar fram och returnerar antingen en slumpad index på ett element från
        listan med springarens giltiga positioner eller -1 ifall listan är tom.
        """
        if len(self.correct_position_list) > 0:
            return random.randint(0, len(self.correct_position_list))
        else:
            return -1

    def knight_walk(self):
        """
        Flyttar springaren genom schackbrädet om användaren skriver en egen springarvandring
        """
        global error_counter
        self.position_counter += 1
        self.board_coordinate_y = self.vertical_tiles.index(self.knight_position[:1]) + 2
        self.board_coordinate_x = self.horizontal_tiles.index(self.knight_position[1:]) + 2
        self.update_tiles_dict()
        self.update_board_list()

        move = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for position in move:
            new_move = self.board_tiles[self.board_coordinate_x + position[0]][
                self.board_coordinate_y + position[1]]

            if new_move.get(str(new_move)[2:4]) == 0:
                self.correct_position_list.append(str(new_move)[2:4])

        if len(self.correct_position_list) > 0 and len(self.position_list) > self.position_counter:
            # Om längden på listan med giltiga rutor inte är tom och det finns fler rutor att undersöka
            if self.position_list[self.position_counter] in self.correct_position_list:
                # Om alla angivna rutor är korrekta
                self.knight_position = self.position_list[self.position_counter]
                self.correct_position_list.clear()
                self.knight_walk()
            else:
                error_counter += 1
                if error_counter < 6:
                    user_input: str = input(f"Elementet #{self.position_counter + 1}"
                                            f" \"{self.position_list[self.position_counter]}\" är inte en"
                                            f" giltig ruta för springaren att flytta till. Ange din springarvandring"
                                            f" med giltiga rutor enligt notationen i schackbrädet ovanför: ")
                    # Återställ alla de parametrar som använts och undersök användarens input igen
                    self.position_counter = 0
                    self.position_list.clear()
                    self.correct_position_list.clear()
                    self.board_coordinate_x = 0
                    self.board_coordinate_y = 0
                    self.get_tiles_dict_from_file()
                    self.get_board_list_from_file()
                    check_user_input(user_input.upper())
                else:
                    print("\nFör många felinmatningar! Avslutar programmet...")
        else:
            self.board_print(1)
            print(f"\nVar så god, här är er egna springarvandring!\nSpringaren vandrade från startrutan"
                  f" \"{self.position_list[0]}\" till slutrutan \"{self.position_list[len(self.position_list) - 1]}\""
                  f" och besökte totalt {self.position_counter} unika rutor i schackbrädet.")

    def board_print(self, intro):
        """
        Utskrift av schackbrädet
        :param intro: Väljare för vilken sorts schackbräda som ska skrivas ut, antingen i början eller i slutet
        av programkörningen.
        """
        # Första raden med övre högra hörnet för utsmyckning
        print()
        for i in range(len(self.vertical_tiles) + 4):
            print(f"----", end="")
        print('-')
        # Andra raden med A-H
        print(f"|   ", end="")
        for i in range(len(self.vertical_tiles)):
            print(f"  {self.vertical_tiles[i]}  ", end="")
        print(f"    |")
        # Första mellanraden för rutorna
        print(f"|   ", end="")
        for i in range(len(self.vertical_tiles)):
            print(f"-----", end="")
        print(f"-   |")
        # Rutorna
        for i in range(len(self.horizontal_tiles)):
            print(f"| {self.horizontal_tiles[i]} |", end="")
            for j in range(len(self.vertical_tiles)):
                if intro == 0:
                    # Presentation av schackbrädet åt användaren med synliga notationer
                    print(f" {self.vertical_tiles[j]}{self.horizontal_tiles[i]} |", end="")
                else:
                    # Presentation av schackbrädet åt användaren med springarens vandring med nödvändig utsmyckning
                    if (self.tiles[self.vertical_tiles[j] + self.horizontal_tiles[i]]) > 9:
                        print(f" {self.tiles[self.vertical_tiles[j] + self.horizontal_tiles[i]]} |", end="")
                    elif (self.tiles[self.vertical_tiles[j] + self.horizontal_tiles[i]]) == 0:
                        print(f"    |", end="")
                    else:
                        print(f"  {self.tiles[self.vertical_tiles[j] + self.horizontal_tiles[i]]} |", end="")
            print(f" {self.horizontal_tiles[i]} |")
            # Nedersta linjen
            print(f"|   ", end="")
            for j in range(len(self.vertical_tiles)):
                print(f"-----", end="")
            print(f"-   |")
        # Näst sista raden
        print(f"|   ", end="")
        for i in range(len(self.vertical_tiles)):
            print(f"  {self.vertical_tiles[i]}  ", end="")
        print(f"    |")
        # Sista raden med nedre högra hörnet för utsmyckning
        for i in range(len(self.vertical_tiles) + 4):
            print(f"----", end="")
        print('-')


def check_user_input(user_input):
    """
    Hanterar användarens inputs
    :param user_input: Tar emot användarens inmatningar och kontrollerar att alla inmatningar
    stämmer överens med schackbrädets rutor
    """
    global error_counter
    broken = False
    invalid_tile = ""
    invalid_index = 0
    user_input = user_input.strip()
    user_tiles_list = user_input.split(",")

    for element in user_tiles_list:
        if chess_board.tiles.get(element.strip(), -1) >= 0:
            # Det strippade elementet finns i listan med schackbrädets rutor
            chess_board.knight_position = element.strip
            chess_board.position_list.append(element.strip())
        else:
            invalid_tile = element.strip()
            invalid_index = len(chess_board.position_list)
            broken = True
            break

    if broken:
        error_counter += 1
        if error_counter < 6:
            if invalid_tile == "":
                user_input: str = input(f"Element #{invalid_index + 1} är tom. Var vänlig ange"
                                        f" en bra lista enligt notationen i schackbrädan ovanför: ")
            else:
                user_input: str = input(f"Elementet #{invalid_index + 1} \"{invalid_tile}\" är inte en giltig ruta"
                                        f" som springaren kan flytta till. Var vänlig ange enligt notationen i"
                                        f" schackbrädan ovanför: ")
            # Återställ alla de parametrar som använts och undersök användarens input igen
            chess_board.knight_position = ""
            chess_board.position_list.clear()
            check_user_input(user_input.upper())
        else:
            print("\nFör många felinmatningar! Avslutar programmet...")
    else:
        chess_board.knight_position = chess_board.position_list[0]
        if len(chess_board.position_list) == 1:
            chess_board.knight_journey()
        else:
            chess_board.knight_walk()


error_counter = 0
chess_board = Board()
chess_board.get_tiles_dict_from_file()
chess_board.get_board_list_from_file()
print()
print("Hej och varmt välkommen till springarens vandringsprogram!")
chess_board.board_print(0)
print("\nNi har möjligheten att:\n- antingen ange en startposition åt springaren så kommer springaren vandra slumpvis"
      " genom schackbrädet utan att besöka samma ruta mer än en gång\n- eller istället ange en komma-separerad"
      " inmatning av den springarvandring som du vill ha så kommer springaren vandra genom schackbrädet enligt din"
      " komma-separerade inmatning.\n\nVänligen observera notationen av schackbrädan ovan och mata in er inmatning i"
      " enlighet med den så kommer er inmatning bli korrekt.\n")
tile_input: str = input("Ange er inmatning här: ")
check_user_input(tile_input.upper())
