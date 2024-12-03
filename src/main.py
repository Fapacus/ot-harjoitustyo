from game import Game
from memory_game import memory_game
from database_connection import create_connection

database_connection = create_connection()

def main():
        while True:
            choice = input(
                "What u wanna do?\n"
                "1. Play on!!\n"
                "2. Register\n"
                "3. Login\n"
                "4. Print all users\n"
                "5. Exit\n"
            )

            if choice == "1":
                memory_game()
            elif choice == "2":
                game.register_user()
            elif choice == "3":
                game.login_user()
            elif choice == "4":
                game.print_users()
            elif choice == "5":
                print("Auf Wiedersehen!")
                game.connection.close()
                break
            else:
                print("Hell no! Please try again.")

game = Game(database_connection)
main()