from game import Game
from memory_game import memory_game

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
                Game.register_user()
            elif choice == "3":
                Game.login_user()
            elif choice == "4":
                Game.print_users()
            elif choice == "5":
                print("Auf Wiedersehen!")
                Game.connection.close()
                break
            else:
                print("Hell no! Please try again.")

main()