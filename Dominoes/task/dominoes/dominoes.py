# Dominoes

import random


def find_max(list_of_dominoes):
    """Find the maximum value of a domino in a list of dominoes"""
    max_l = 0
    for L in list_of_dominoes:
        if sum(L) > max_l:
            max_l = sum(L)
    return max_l


def largest_domino(list_of_dominoes):
    """returns the domino with max value from dominoes in a list"""
    max_l = 0
    large_domino = []
    for L in list_of_dominoes:
        if sum(L) > max_l:
            max_l = sum(L)
            large_domino = L
    return large_domino


def print_screen():
    """call this function to print the screen"""
    global stock_pieces
    global computer_pieces
    global player_pieces
    global domino_snake
    for i in range(70):
        print("=", end="")
    print()
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}")
    print()
    if len(domino_snake) > 6:
        print(domino_snake[0], domino_snake[1], domino_snake[2], "...",
              domino_snake[-3], domino_snake[-2], domino_snake[-1])
    else:
        for dom in range(len(domino_snake)):
            print(domino_snake[dom], end="")
    print()
    print()
    print("Your pieces: ")
    j = 1
    for p in player_pieces:
        print(f"{j}: {p}")
        j += 1
    print()


def place_domino(place_dom):
    """
    This function will check if domino placement is legal.
    place_dom is the domino to be placed and new_dom is this domino flipped round.
    following checks place_dom is either added to the domino_snake if legal
    or nothing is added. Status is printed and a boolean is returned.
    If place_domino is True a move has occurred!
    domino_snake[0][0] is the left most integer of the snake,
    whereas domino_snake[-1][1] is the right most integer.
    place_dom[0] is the left of the domino and [1] is the right.
    if left and right match or vice versa place_dom is placed
    if right and right or left and left match new_dom is placed
    """
    global domino_snake
    placement = False
    if domino_snake[0][0] == place_dom[0]:
        new_dom = [place_dom[1], place_dom[0]]
        domino_snake.insert(0, new_dom)
        placement = True
        return placement
    elif domino_snake[0][0] == place_dom[1]:
        domino_snake.insert(0, place_dom)
        placement = True
        return placement
    elif domino_snake[-1][1] == place_dom[0]:
        domino_snake.append(place_dom)
        placement = True
        return placement
    elif domino_snake[-1][1] == place_dom[1]:
        new_dom = [place_dom[1], place_dom[0]]
        domino_snake.append(new_dom)
        placement = True
        return placement
    return placement


def try_best_move(computer_piece_index):
    """
    This is the AI for the computer!
    It takes the index of the item in the list of computer pieces for
    the first domino identified with the max score
    Max score calculations are completed outside the function.
    if the piece is placed it is removed from the list.
    Otherwise the score value sent to the function is reset to zero
    and the boolean returned allows the AI to try another move
    """
    global AI_domino_scores
    global computer_pieces
    global status
    try_again = True
    if place_domino(computer_pieces[computer_piece_index]):
        computer_pieces.remove(computer_pieces[computer_piece_index])
        status = "player"
        try_again = False
    else:
        AI_domino_scores[computer_piece_index] = 0
    return try_again


# create all the domino pieces for the game
full_domino_list = []
for m in range(7):
    for d in range(7 - m):
        d += m
        full_domino_list.append([d, m])
        d += 1
    m += 1

# These global variables will be assigned value later
stock_pieces = []
computer_pieces = []
player_pieces = []
domino_snake = []
status = ""
playing = True
shuffle = True

# logic loop shuffles dominoes, checks for doubles and re-shuffles if not found
while shuffle:
    random.shuffle(full_domino_list)

    # though its strictly unnecessary as the shuffle has randomised pieces,
    # I used steps in my list slicing to recreate the act of taking turns to choose pieces
    # the pieces remaining following slicing are the stock pieces
    computer_pieces = full_domino_list[0:14:2]
    player_pieces = full_domino_list[1:14:2]
    stock_pieces = full_domino_list[14::]

    # recombine the list to check for doubles in both lists
    # if doubles are found in playable pieces stop shuffling.
    starting_pieces = player_pieces + computer_pieces
    for n in range(7):
        if [n, n] not in starting_pieces:
            shuffle = True
            n += 1
        else:
            shuffle = False
            break

# the starting domino and who goes first are both decided once shuffling is complete
# the starting domino is the domino with the highest value
if find_max(player_pieces) > find_max(computer_pieces):
    domino_snake.append(largest_domino(player_pieces))
    player_pieces.remove(largest_domino(player_pieces))
    status = "computer"
else:
    domino_snake.append(largest_domino(computer_pieces))
    computer_pieces.remove(largest_domino(computer_pieces))
    status = "player"

# Beginning the game loop
print_screen()
while playing:
    if status == "player":
        # the first message is outside the loop to accommodate different feedback for the player within loop
        print("Status: It's your turn to make a move. Enter your command. ")
        while status == "player":
            # an initial int value makes the rest of the code easier but is prone to value error
            try:
                player_move = abs(int(input()))
                if player_move > len(player_pieces):  # Too high
                    print("Invalid input. Please try again.")
                elif player_move == 0:  # Get more dominoes
                    if len(stock_pieces) > 0:
                        player_pieces.append(stock_pieces[0])
                        stock_pieces.remove(stock_pieces[0])
                        status = "computer"
                    else:  # unless there are none left
                        status = "computer"
                elif place_domino(player_pieces[player_move - 1]):  # a move has happened!
                    player_pieces.remove(player_pieces[player_move - 1])  # remove the placed domino from player list
                    status = "computer"
                else:
                    print("Illegal move. Please try again. ")
            except ValueError:
                print("Invalid input. Please try again.")
    else:
        input("Status: Computer is about to make a move. Press Enter to continue... ")

        # Create the AI dictionary of scores that guide the most effective computer moves
        AI_score_calc = {}
        score_variable = 0
        for score_variable in range(7):
            counter = 0
            for d in domino_snake:
                counter += d.count(score_variable)
            for c in computer_pieces:
                counter += c.count(score_variable)
            AI_score_calc[score_variable] = counter

        # With the dictionary complete, apply the scores to the computers dominoes as a list
        # the index value of domino_score corresponds to the index value in computer_pieces
        AI_domino_scores = []
        for c in computer_pieces:
            piece_score = 0
            for value in c:
                piece_score += AI_score_calc[value]
            AI_domino_scores.append(piece_score)

        # the function try best move is completed on loop eliminating computer moves until
        # computer is forced to draw a domino
        while max(AI_domino_scores) > 0:
            if not try_best_move(AI_domino_scores.index(max(AI_domino_scores))):
                break
        if max(AI_domino_scores) == 0:
            if len(stock_pieces) > 0:
                computer_pieces.append(stock_pieces[0])
                stock_pieces.remove(stock_pieces[0])
                status = "player"
            else:
                status = "player"

    # following the move print the screen and check draw and win conditions
    print_screen()

    for value in range(7):
        draw_con = 0
        for domino in domino_snake:
            draw_con += domino.count(value)
        if draw_con >= 8:
            playing = False
            print("Status: The game is over. It's a draw!")

    if len(player_pieces) <= 0:
        playing = False
        print("Status: The game is over. You won!")
    elif len(computer_pieces) <= 0:
        playing = False
        print("Status: The game is over. The computer won!")
