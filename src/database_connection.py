import sqlite3

def database_connection(user_data="user_data.db"):
    data_connection = sqlite3.connect(user_data)
    return data_connection
