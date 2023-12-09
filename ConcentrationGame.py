"""
COMP.CS.100 Graafinen käyttöliittymä
Tehtävä 13.10
Tehnyt Jonatan Tevaniemi
Opiskelijanumero: 150176680

ARVIOIJALLE / TO THE GRADER:
Tämä projekti tavoittelee kehittyneen (200 p.) käyttöliittymän pisteitä.
This project is designed with the 200 point criteria in mind.

KÄYTTÖOHJEET:
Tämä ohjelma toteuttaa muistipelin, joka mittaa aikaa.
Valitse alkuvalikosta määrä pareja, jotka haluat ratkaista.
Paina sitten "Ready"-nappia. Valitse "Yes", jos haluat jatkaa valituilla
asetuksilla. Klikkaa kahta korttia, ja yritä löytää pareja korteista.
Kun olet löytänyt kaikki parit, ohjelma vie sinut loppunäyttöön josta näet
pelin koon, voittoajan sekä selvitysajan paria kohti. Valitse "Play again" tai
"Quit" riippuen, mitä haluat tehdä.

INSTRUCTIONS:
This program is a Concentration game (Tile matching game, memory game...)
that measures time to solve the puzzle. In the start menu, choose amount of
pairs to solve. Then press "Ready". Choose "Yes" if you wish to continue with
the chosen settings. Choose two cards and try to find pairs in the grid of
cards. When you have found all pairs, the program will take you to an end
screen and shows you information about the game you just played.
Choose "Play again" or "Quit" depending on what you wish to do.
"""

from tkinter import *
import random
import time


class Startmenu:
    """
    This class is the start menu for the game. In this the player chooses
    the size of the game and whether they are playing with someone or not.
    """
    def __init__(self):
        # Initialize menu window.
        self.__mainwindow = Tk()
        self.__mainwindow.iconbitmap("gameicon.gif")
        self.__mainwindow.title("Main Menu")

        # Main label.
        self.__main_label = Label(self.__mainwindow,
                                  text="Concentration game. Select amount of "
                                  "pairs.",
                                  padx=30, pady=10,
                                  font=("Arial", 12),
                                  borderwidth=2,
                                  relief=RIDGE
                                  )

        # Dropdown menu for amount of pairs.
        self.__options_pairs = ["5", "6", "7", "8", "9", "10"]
        self.__selected_pairs = StringVar()
        self.__selected_pairs.set("5")

        # The asterisk is to unpack the list.
        self.__dropdown_pairs = OptionMenu(self.__mainwindow,
                                           self.__selected_pairs,
                                           *self.__options_pairs
                                           )
        # Dropdown menu label.
        self.__label_pairs = Label(self.__mainwindow,
                                   text="Select amount of pairs (5-10):",
                                   padx=10, pady=10,
                                   font=("Arial", 10)
                                   )

        # Quit button.
        self.__quit_button = Button(self.__mainwindow,
                                    text="Quit",
                                    command=self.quit
                                    )

        # Ready button.
        self.__ready_button = Button(self.__mainwindow,
                                     text="Ready!",
                                     command=self.confirm_options
                                     )

        self.__main_label.grid(row=0, column=0, columnspan=2, sticky="nwe")
        self.__quit_button.grid(row=3, column=0, sticky="swe")
        self.__label_pairs.grid(row=1, column=0, sticky="swe")
        self.__dropdown_pairs.grid(row=2, column=0, columnspan=2, sticky="nwe")
        self.__ready_button.grid(row=3, column=1, sticky="swe")

    def quit(self):
        """
        Quits program
        """
        self.__mainwindow.destroy()

    def start(self):
        """
        Starts the main window loop.
        """
        self.__mainwindow.mainloop()

    def confirm_options(self):
        """
        Proceeds to confirm window.
        """
        self.__mainwindow.destroy()
        type(self.__selected_pairs.get())
        Confirm(self.__selected_pairs.get())


class Confirm:
    """
    Confirmation window for the game parameters.
    """
    def __init__(self, size):
        """
        For user to confirm settings.
        :param size: str, user set size of game
        """
        self.__mainwindow = Tk()
        self.__mainwindow.iconbitmap("gameicon.gif")
        self.__mainwindow.title("Are you sure?")
        self.__size = size

        self.__main_label = Label(self.__mainwindow,
                                  text="Current options:"
                                  )
        self.__label = Label(self.__mainwindow,
                             text=f"Game size: {size} pairs."
                                  f" Continue with these settings?",
                             padx=30, pady=10,
                             font=("Arial", 10)
                             )

        self.__yes_button = Button(self.__mainwindow,
                                   text="Yes!",
                                   command=self.yes
                                   )

        self.__no_button = Button(self.__mainwindow,
                                  text="No, take me back!",
                                  command=self.no
                                  )

        self.__label.pack()
        self.__yes_button.pack(side=RIGHT, expand=TRUE, fill=BOTH)
        self.__no_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.__mainwindow.mainloop()

    def yes(self):
        self.__mainwindow.destroy()
        Game(self.__size)

    def no(self):
        self.__mainwindow.destroy()
        Startmenu()


class Game:
    """
    This class is the window of the game itself.
    """
    def __init__(self, size):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Concentration Game")
        self.__mainwindow.iconbitmap("gameicon.gif")
        self.__size = int(size)

        self.__back_image = PhotoImage(file="cards/back.png")

        self.__cards = self.cards_set()
        self.__buttons = []

        self.__revealed_cards = {}
        self.__matched_cards = {}

        self.__timer_label = Label(self.__mainwindow, text="Timer: 0:00",
                                   font=("Arial", 14))
        self.__timer_label.grid(row=0, column=0, columnspan=4)
        self.__start_time = time.time()
        self.__elapsed_time = 0
        self.update_timer()
        self.__win_time = None

        self.grid()

        self.__mainwindow.mainloop()

    def update_timer(self):
        """
        Updates the timer on screen.
        """

        elapsed_time = time.time() - self.__start_time
        timer_text = f"Timer: {elapsed_time:.3f}"
        self.__timer_label.config(text=timer_text)
        if not len(self.__matched_cards) == 2 * self.__size:
            self.__mainwindow.after(200, self.update_timer)

    def cards_set(self):
        """
        Creates the identifying numbers for the cards and shuffles them.
        """
        cards = [i for i in range(self.__size)] * 2
        random.shuffle(cards)
        return cards

    def grid(self):
        """
        This function creates the grid of cards (or buttons) for the game
        """
        # This is the "identifier" (?) for the button itself.
        count = 0
        for i in range(len(self.__cards)):
            # This is the identifier for the card "in" the button.
            index = self.__cards.pop(0)

            # This has to have a lambda function because else it will be
            # called at button creation.
            card = Button(self.__mainwindow,
                          image=self.__back_image,
                          command=lambda idx=index, counter=count:
                          self.show_card(idx, counter)
                          )
            card.image = self.__back_image
            card.front_image = None

            card.grid(row=1+(i // 4), column=i % 4)
            self.__buttons.append(card)
            count += 1

    def show_card(self, idx, counter):
        """
        Reveal a card when clicked, showing its front image. When two are
        pressed, determine what to do with them.
        :param idx: int, the identifier for the card
        :param counter: int, the identifier for the button
        """
        button = self.__buttons[counter]
        # Change the image to the front image of the card
        front_image = PhotoImage(file=f"cards/{idx + 1}.png")
        button.config(image=front_image)
        button.front_image = front_image

        self.__revealed_cards[button] = idx

        # In this game, only two cards can be shown at a time.
        if len(self.__revealed_cards) == 2:

            # Check if the two revealed cards is a pair.
            if len(set(self.__revealed_cards.values())) == 1:
                self.handle_pair()
                self.check_win_condition()

            # If it is not a pair, disable buttons (so player can't cheat)
            # and hide the cards.
            else:
                self.disable_buttons()

    def handle_pair(self):
        """
        Update matched cards to a dict and disable buttons for matched cards.
        """
        for button in self.__revealed_cards:
            self.__matched_cards[button] = self.__revealed_cards[button]

        # Disable the buttons for the matched cards.
        for card_button in self.__revealed_cards:
            card_button.config(state=DISABLED)

        # This dictionary doesn't need information about pairs.
        self.__revealed_cards = {}

    def disable_buttons(self):
        """
        Disables every button so the player can't cheat (press more than 2 at
        a time)
        """
        for button in self.__buttons:
            button.config(state=DISABLED)
        # hide cards after a delay
        self.__mainwindow.after(1000, self.hide_cards)

    def check_win_condition(self):
        """
        Checks if all pairs are matched and goes to end screen.
        """
        if len(self.__matched_cards) == 2 * self.__size:
            self.__win_time = self.get_elapsed_time()
            self.__mainwindow.after(1500, self.end_game)

    def hide_cards(self):
        """
        Hides cards that are not found pairs
        """
        for card in self.__revealed_cards:
            card.config(image=self.__back_image)

        for button in self.__buttons:
            if button not in self.__matched_cards:
                button.config(state=NORMAL)

        # No cards are revealed after this (except for found pairs
        # but they are not saved in this dict).
        self.__revealed_cards = {}

    def end_game(self):
        """
        Ends the game.
        """
        self.__mainwindow.destroy()
        EndScreen(self.__win_time, self.__size)

    def get_elapsed_time(self):
        """
        Returns time elapsed (for the end screen)
        :return: float, time elapsed
        """
        return time.time() - self.__start_time


class EndScreen:
    """
    This is the end screen.
    """
    def __init__(self, time_win, size):
        self.__time_win = time_win
        self.__size = size
        self.__mainwindow = Tk()
        self.__mainwindow.title("Concentration Game")
        self.__mainwindow.iconbitmap("gameicon.gif")

        self.__congratulations_label = Label(self.__mainwindow,
                                             text="Congratulations! You won!",
                                             font=("Arial", 14),
                                             relief=RIDGE
                                             )
        self.__size_label = Label(self.__mainwindow,
                                  text=f"Game size was {size} pairs "
                                       f"({size * 2} total cards).",
                                  font=("Arial", 12),
                                  )
        self.__time_label = Label(self.__mainwindow,
                                  text=f"Total time: "
                                       f"{time_win:.3f} seconds."
                                       f" Time per pair: {time_win / size:.3f}"
                                       f" seconds.",
                                  font=("Arial", 12)
                                  )

        self.__again_button = Button(self.__mainwindow,
                                     text="Play again",
                                     command=self.play_again,
                                     font=("Arial", 12)
                                     )

        self.__quit_button = Button(self.__mainwindow,
                                    text="Quit",
                                    command=self.quit,
                                    font=("Arial", 12)
                                    )

        self.__congratulations_label.grid(row=0, column=0,
                                          sticky="we", columnspan=2)
        self.__time_label.grid(row=1, column=1, padx=10, pady=10)
        self.__size_label.grid(row=1, column=0, padx=10, pady=10)

        self.__again_button.grid(row=2, column=0, padx=10, pady=10)
        self.__quit_button.grid(row=2, column=1, padx=10, pady=10)

        self.__mainwindow.mainloop()

    def play_again(self):
        """
        Starts the program again.
        """
        self.__mainwindow.destroy()
        Startmenu()

    def quit(self):
        """
        Exits program.
        """
        self.__mainwindow.destroy()


def main():
    menu = Startmenu()

    menu.start()


if __name__ == "__main__":
    main()
