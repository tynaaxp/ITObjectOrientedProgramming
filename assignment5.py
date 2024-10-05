"""
Phuong Thai
phuongtranxuanthai@usf.edu
U32184606
"""

from string import ascii_lowercase
import random

class GLGException(Exception):
    """The base Exception for all GuessingLetterGame Exceptions"""
    pass

class NotLetterError(GLGException):
    """Exception raised when the input is not a letter."""
    pass


# GuessingLetterGame class
class GuessingLetterGame:
    list_games = []  # Class variable to track all games

    def __init__(self) -> None:
        """Initialize a new game, pick a secret letter and add the game to the list of games."""
        self._pick_letter()
        self.list_guesses = []
        self.correctly_guessed = False
        self.still_playing = True
        GuessingLetterGame.list_games.append(self)
        print("A new game is started.")

    @property
    def secret_letter(self) -> str:
        """Set the secret letter that players try to guess."""
        return self._secret_letter

    @secret_letter.setter
    def secret_letter(self, value: str) -> None:
        """Property to set the secret letter. Let them know if the value is not in ascii_lowercase."""
        if value.lower() in ascii_lowercase:
            self._secret_letter = value.lower()
        else:
            print("The letter should be from a to z.")
        
    def play(self, value: str) -> str:
        """Method to take a user's guess and compare it with the computer's letter."""
        if not self.still_playing:
            raise GLGException("The game has already ended.")

        guess = value.lower()
        if not guess.isalpha() or len(guess) != 1:
            return("The letter should be from a to z.")
        if guess in self.list_guesses:
            return(f"You already guessed {guess} before.\nPlease pick a different letter.")
        
        self.list_guesses.append(guess)
        if guess == self._secret_letter:
            self.correctly_guessed = True
            self.still_playing = False
            self.display_info()
            return f"The letter was {guess}.\nYou won the game.\nGuesses: {self.list_guesses}\nGame ended"
        elif ascii_lowercase.index(guess) < ascii_lowercase.index(self._secret_letter):
            return f"LetterAfter: The letter comes after {guess}."
        else:
            return f"LetterBefore: The letter comes before {guess}."
        
    def display_info(self) -> str:
        """
        Provides the current game status, including whether the player has won or lost and the letters guessed so far.
        Returns a message detailing the current game status (win, loss, or ongoing play) and the letters that have been guessed so far.
        """
        if not self.still_playing and not self.correctly_guessed:
            status = "You lost the game."
        elif not self.still_playing and self.correctly_guessed:
            status = "You won the game."
        else:
            status = "You are still playing the game."

        if self.list_guesses:
            guesses = "', '".join(self.list_guesses)  # Join with quotes only if there are guesses
            return f"{status}\nGuesses: ['{guesses}']"
        else:
            return f"{status}\nGuesses: []"  # Empty list without quotes
        
    def _pick_letter(self) -> None:
        """
        Randomly selects a secret letter from the alphabet for the user to guess.
        """
        self._secret_letter = random.choice(ascii_lowercase)

    def end(self) -> str:
        """Method to end the game."""
        self.still_playing = False
        if not self.correctly_guessed:
            return self.display_info()
        
# Stand-alone function for summarizing game statistics
def summary_guessinglettergame() -> str:
    """Function to display statistics of Guessing Letter Game."""
    active_games = sum(1 for game in GuessingLetterGame.list_games if game.still_playing)
    games_won = sum(1 for game in GuessingLetterGame.list_games if game.correctly_guessed)
    # games_lost should be the count of games that are not active and not won
    games_lost = sum(1 for game in GuessingLetterGame.list_games if not game.still_playing and not game.correctly_guessed)
    return f"Active games: {active_games}\nGames won: {games_won}\nGames lost: {games_lost}\nTotal games: {len(GuessingLetterGame.list_games)}"

# Example usage
if __name__ == "__main__":
    game1 = GuessingLetterGame()
    print(game1.display_info())
    print(game1.play('m'))
    print(game1.display_info())
    print(game1.play('m')) 
    print(game1.play('F'))
    print(game1.play('i'))
    print(game1.play('k'))
    print(game1.play('L'))
    print(summary_guessinglettergame())
