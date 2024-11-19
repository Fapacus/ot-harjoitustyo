user_data = "user_data.txt"

def load_users():
    users = {}

    try:
        with open(user_data, "r") as file:
            for line in file:
                username, password = line.strip().split(": ")
                users[username] = password
    except FileNotFoundError:
        pass
    
    return users

def save_users(users):
    with open(user_data, "w") as file:
        for username, password in users.items():
            file.write(f"{username}: {password}\n")

def register_user(users):
    while True:
        username = input("Enter username: ").strip()
        if username in users:
            print("Username already exists. Pls try again!")
        else:
            password = input("Enter password: ").strip()
            users[username] = password
            save_users(users)
            print("All done n dusted!")
            break
    
    return 

def main():
    users = load_users()
    register_user(users)
    print(users)


if __name__ == "__main__":
    main()
