from game import Game
from memory_game import memory_game
from database_connection import database_connection
from highscore_connection import highscore_connection

data_connection = database_connection()
score_connection = highscore_connection()

def main():
    while True:
        print("")
        print("Welcome to Muistipeli!\n")
        choice = input(
            f"What u wanna do? (Login status: {game.get_username()})\n"
            "1. Play on!!\n"
            "2. Register\n"
            "3. Login\n"
            "4. Print scoreboard\n"
            "5. Print all users\n"
            "6. Print all users (as admin)\n"
            "7. Exit\n"
        )
        print("")
        if choice == "1":
            memory_game(game)
        elif choice == "2":
            game.register_user()
        elif choice == "3":
            game.login_user()
        elif choice == "4":
            game.print_scores()
        elif choice == "5":
            game.print_users("user")
        elif choice == "6":
            game.print_users("admin")
        elif choice == "7":
            print("Auf Wiedersehen!")
            game.data_connection.close()
            break
        else:
            print("Hell no! Please try again.")

game = Game(data_connection, score_connection)
main()
