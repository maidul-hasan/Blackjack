import random
import time

players_dict = {}
bankrupt_players = {}
deck_of_cards = 4 * list(range(1, 14))
cards_name = {1: "Ace", 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: "King", 12: "Queen",
              13: "Jack", }
card_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10}
play_round = [0]


class Player:
    def __init__(self, name, bankroll_amount):
        self.name = name
        self.bankroll = bankroll_amount
        self.chips = self.bankroll / 100
        self.bet = 0
        self.cards_points = 0
        self.win_status = "_"


class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.bankroll = 100000
        self.chips = self.bankroll / 100
        self.cards_points = 0
        self.cards = []


def welcome_screen():
    print("""
    
                                    #===================================#
                                    #       WELCOME TO BLACKJACK        #
                                    #===================================#
                                    
    """)
    time.sleep(1)


def game_starting_screen():
    print(f"\nRound '{play_round[0]}' is STARTING..", end="")
    time.sleep(1)
    print(".....", end="")
    time.sleep(.5)
    print("..............")
    time.sleep(.5)
    print("\n")


def players():
    # instantiating players and their attributes
    while True:
        try:
            print("Select the number of payers at the table (1~5): ", end="")
            num_players = int(input())
            if num_players < 1 or num_players > 5:
                print("Please enter a valid number. ", end="")
                continue
            else:
                break
        except ValueError:
            print("Please enter a number. ", end="")
    for item in range(num_players):
        while True:
            player_name = input(f"\nPlease enter a name for the player at spot {item + 1}: ")
            if len(player_name) == 0:
                print("Please enter a valid name. ", end="")
                continue
            else:
                break
        while True:
            try:
                player_bankroll = int(input(
                    f"Mr./Mrs. '{player_name}' please enter your initial bankroll amount (in multiples of 100): $ "))
                if player_bankroll < 300:
                    print("Your bankroll must be at least $300. ", end="")
                    continue
                if player_bankroll % 100 != 0 and player_bankroll > 300:
                    print("Bankroll amounts must be in multiples of $100 (a single chip value). ", end="")
                    continue
                else:
                    break
            except ValueError:
                print("Please Enter a Valid amount. ", end="")
        players_dict.update({item: Player(player_name, player_bankroll)})

    # instantiating dealer and dealer's attributes
    dealer = Dealer()
    total_bankroll = 0
    for itm in range(num_players):
        total_bankroll += players_dict[itm].bankroll
    if total_bankroll * 10 > dealer.bankroll:
        dealer.bankroll = total_bankroll * 10
    players_dict.update({"dealer": dealer})


def place_bets():
    for key in range(len(players_dict.keys()) - 1):
        if players_dict[key].chips == 0:
            print(f"Mr./Mrs. '{players_dict[key].name}' does not have enough money to continue playing.")
            bankrupt_players.update({key: players_dict[key]})
    for key in range(len(players_dict.keys()) - 1):
        if key not in bankrupt_players.keys():
            while True:
                try:
                    bet = int(input(
                        "Mr./Mrs. '{}', How many chips do you want to bet? You must bet at least $100 (1 chip). (you "
                        "have total of {} chips.): ".format(players_dict[key].name, players_dict[key].chips)))
                    if bet == 0:
                        print("You must bet at least $100 (1 chip). ", end="")
                        continue
                    elif bet > players_dict[key].chips:
                        print("You can't bet more than what you have. ", end="")
                        continue
                    else:
                        players_dict[key].bet = bet
                        break
                except ValueError:
                    print("Please enter a valid value. ", end="")


def deal_players_hand():
    time.sleep(1)
    for key in range(len(players_dict.keys()) - 1):
        if key not in bankrupt_players.keys():
            rand_card = random.choice(deck_of_cards)
            deck_of_cards.remove(rand_card)
            value = 0
            print(f"\n*** Mr./Mrs. '{players_dict[key].name}' got {cards_name[rand_card]} ***", end="\t")
            if cards_name[rand_card] == "Ace":
                while True:
                    try:
                        res = int(input("Which value do you want to use (1. 1  or 2. 11): "))
                        if res == 1:
                            value = 1
                            break
                        elif res == 2:
                            value = 11
                            break
                        elif res < 1 or res > 2:
                            print("Please enter (1/2) to select from the options. ", end="")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Please enter (1/2) to select from the options. ", end="")

            else:
                value = card_values[rand_card]
            players_dict[key].cards_points += value


def deal_dealers_hand():
    rand_card = random.choice(deck_of_cards)
    players_dict["dealer"].cards.append(cards_name[rand_card])
    deck_of_cards.remove(rand_card)
    if cards_name[rand_card] == "Ace":
        if players_dict['dealer'].cards_points + 11 <= 21:
            value = 11
        else:
            value = 1
    else:
        value = card_values[rand_card]
    players_dict['dealer'].cards_points += value


def players_turn():
    for key in range(len(players_dict.keys()) - 1):
        if key not in bankrupt_players.keys():
            print(f"\n\nMr./Mrs. '{players_dict[key].name}' you have total {players_dict[key].cards_points} points.")
            if players_dict[key].cards_points == 21:
                print(f"Mr./Mrs. '{players_dict[key].name}' you Won :)")
                players_dict[key].win_status = "Won"
                players_dict[key].chips += players_dict[key].bet
                players_dict[key].bankroll += players_dict[key].bet * 100
                players_dict["dealer"].chips -= players_dict[key].bet
                players_dict["dealer"].bankroll -= players_dict[key].bet * 100
            elif players_dict[key].win_status == "_":
                while True:
                    try:
                        response = int(
                            input(f"Mr./Mrs. '{players_dict[key].name}' please chose from (1. Hit me or 2. Stand): "))
                        if response == 1:
                            rand_card = random.choice(deck_of_cards)
                            deck_of_cards.remove(rand_card)
                            print(f"Mr./Mrs. '{players_dict[key].name}' you got {cards_name[rand_card]}.", end="  ")
                            if cards_name[rand_card] == "Ace":
                                while True:
                                    try:
                                        res = int(input("Which value do you want to use (1. 1  or 2. 11): "))
                                        if res == 1:
                                            value = 1
                                            players_dict[key].cards_points += value
                                            break
                                        elif res == 2:
                                            value = 11
                                            players_dict[key].cards_points += value
                                            break
                                        elif res < 1 or res > 2:
                                            print("Please enter (1/2) to select from the options. ", end="")
                                            continue
                                        else:
                                            value = card_values[rand_card]
                                            players_dict[key].cards_points += value
                                            break
                                    except ValueError:
                                        print("Please enter (1/2) to select from the options. ", end="")

                            elif cards_name[rand_card] != "Ace":
                                value = card_values[rand_card]
                                players_dict[key].cards_points += value
                            print(
                                f"\nMr./Mrs. '{players_dict[key].name}' you have total {players_dict[key].cards_points} points.")
                            if players_dict[key].cards_points > 21:
                                print(f"Mr./Mrs. '{players_dict[key].name}' you lost :(")
                                players_dict[key].win_status = "Lost"
                                players_dict[key].chips -= players_dict[key].bet
                                players_dict[key].bankroll -= players_dict[key].bet * 100
                                players_dict["dealer"].chips += players_dict[key].bet
                                players_dict["dealer"].bankroll += players_dict[key].bet * 100
                                break
                            elif players_dict[key].cards_points == 21:
                                break
                            else:
                                continue
                        elif response == 2:
                            break
                        elif response < 1 or response > 2:
                            print("Please chose a valid option. ", end="")
                            continue
                    except ValueError:
                        print("Please chose a valid option. ", end="")


def dealers_turn():
    print(f"\n*** Dealer have total {players_dict['dealer'].cards_points} points. ***")
    players_points = []
    for key in range(len(players_dict.keys()) - 1):
        if key not in bankrupt_players.keys():
            if players_dict[key].win_status == "_":
                players_points.append(players_dict[key].cards_points)
    max_players_points = max(players_points)
    while True:
        try:
            for ky in range(len(players_dict.keys()) - 1):
                if ky not in bankrupt_players.keys():
                    if players_dict[ky].win_status == "_":
                        # if it's a draw
                        if players_dict["dealer"].cards_points <= 21 and players_dict[
                            "dealer"].cards_points == max_players_points:
                            print(f"*** It's a draw between Dealer and '{players_dict[ky].name}' ***")
                            players_dict[ky].win_status = "Draw"
                            for k in range(len(players_dict.keys()) - 1):
                                if k not in bankrupt_players.keys():
                                    if players_dict[k].win_status == "_":
                                        players_dict[k].win_status = "Lost"
                                        print(f"*** Mr./Mrs. {players_dict[k].name} lost. ***")
                                        players_dict[k].chips -= players_dict[k].bet
                                        players_dict[k].bankroll -= players_dict[k].bet * 100
                                        players_dict["dealer"].chips += players_dict[k].bet
                                        players_dict["dealer"].bankroll += players_dict[k].bet * 100

                        # when player have less than 21 points and dealer can win with first two hands
                        elif 21 > players_dict["dealer"].cards_points > max_players_points or players_dict[
                            "dealer"].cards_points == 21:
                            print("Dealer Wins !!!!!!!!!!")
                            for key in range(len(players_dict.keys()) - 1):
                                if key not in bankrupt_players.keys():
                                    if players_dict[key].win_status == "_":
                                        players_dict[key].win_status = "Lost"
                                        print(f"*** Mr./Mrs. {players_dict[key].name} lost :(")
                                        players_dict[key].chips -= players_dict[key].bet
                                        players_dict[key].bankroll -= players_dict[key].bet * 100
                                        players_dict["dealer"].chips += players_dict[key].bet
                                        players_dict["dealer"].bankroll += players_dict[key].bet * 100

                        # when dealer has less points
                        elif players_dict["dealer"].cards_points < max_players_points:
                            deal_dealers_hand()
                            r_cards = players_dict['dealer'].cards[::-1]
                            print(
                                f"*** Dealer got {r_cards[0]} *** \n*** Dealer have total {players_dict['dealer'].cards_points} points. ***")
                            if 21 > players_dict["dealer"].cards_points > max_players_points or players_dict[
                                "dealer"].cards_points == 21:
                                continue
                            elif players_dict["dealer"].cards_points > 21:
                                print("Dealer Busts.........")
                                for key in range(len(players_dict.keys()) - 1):
                                    if key not in bankrupt_players.keys():
                                        if players_dict[key].win_status == "_":
                                            players_dict[key].win_status = "Won"
                                            print(f"*** Mr./Mrs. '{players_dict[key].name}' Won :) ")
                                            players_dict[key].chips += players_dict[key].bet
                                            players_dict[key].bankroll += players_dict[key].bet * 100
                                            players_dict["dealer"].chips -= players_dict[key].bet
                                            players_dict["dealer"].bankroll -= players_dict[key].bet * 100

        except ValueError:
            pass
        else:
            break


def players_stats():
    print("\n")
    for key in range(len(players_dict.keys()) - 1):
        if key not in bankrupt_players.keys():
            print(
                f"After round {play_round[0]} Mr./Mrs. {players_dict[key].name} has $ {players_dict[key].bankroll} and ",
                end="")
            if players_dict[key].win_status == "Won":
                print(f"he has Won ${players_dict[key].bet * 100} in this round.")
            elif players_dict[key].win_status == "Lost":
                print(f"he has Lost ${players_dict[key].bet * 100} in this round.\n")
            elif players_dict[key].win_status == "Draw":
                print(f"he has Drawn in this round.")
            players_dict[key].win_status = "_"
            players_dict[key].cards_points = 0
    players_dict["dealer"].cards_points = 0
    players_dict["dealer"].cards = []


def play_another_hand():
    print("\n\nDo you want to play another hand? (1. Yes 2. No): ", end="")
    while True:
        try:
            choice = int(input())
            if choice < 1 or choice > 2:
                print("Please enter (1/2): ", end="")
                continue
            else:
                break
        except ValueError:
            print("Enter (1/2) to select from the options: ", end="")
    if choice == 1:
        return True
    elif choice == 2:
        return False


def quitting():
    print(f"Quiting.......", end="")
    time.sleep(1)
    print(".....", end="")
    time.sleep(.5)
    print(".......")
    time.sleep(.5)
    print("\n")


def all_bankrupt():
    total_bankroll = 0
    for key in range(len(players_dict.keys()) - 1):
        total_bankroll += players_dict[key].bankroll
    if total_bankroll == 0:
        print("All players Went bankrupt.", end="")
        return True


def play_blackjack():
    global deck_of_cards
    welcome_screen()
    players()
    while True:
        play_round[0] += len(play_round)
        game_starting_screen()
        place_bets()
        print("""\n
        Dealing the first hand.........
        """)
        deal_players_hand()
        deal_dealers_hand()
        print(f"\n*** '{players_dict['dealer'].name}' got {players_dict['dealer'].cards[0]} ***")

        print("""\n
        Dealing the second hand.........
        """)
        deal_players_hand()
        deal_dealers_hand()
        players_turn()

        # scenario - all of the players has already lost or won
        players_win_status = []
        for key in range(len(players_dict) - 1):
            if key not in bankrupt_players.keys():
                players_win_status.append(players_dict[key].win_status)
        if "_" in players_win_status:
            dealers_turn()
        else:
            print("!!!!! Match settled before Dealers Turn. !!!!!!!")
        # resetting deck
        deck_of_cards = 4 * list(range(1, 14))
        players_stats()
        if all_bankrupt():
            quitting()
            break
        if not play_another_hand():
            quitting()
            break


play_blackjack()
