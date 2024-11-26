import os
import sqlite3

def create_connection(user_data="user_data.db"):
    connection = sqlite3.connect(user_data)
    return connection