# sql injection example

import sqlite3

# create the table with 'bob and eve'
CREATE_TABLE = '''
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (username text, password text);
    INSERT INTO users (username, password) VALUES ('bob', 'bob_p');
    INSERT INTO users (username, password) VALUES ('alice', 'alice_p');
    '''


def main():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.executescript(CREATE_TABLE)
    
    # get username and password from the user
    username = input("please enter your username: ")  # enter "bob' --"
    password = input("please enter your password: ")  # enter "' OR '1'='1"
    
    # the bad way
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    
    # the good way
    # c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    
    res = c.fetchall()
    # print the result to the screen
    print(res)
    
    # the test for user loged in
    if res:
        print(f"you are {username} and successfully logged in")
    
    conn.close()


if __name__ == '__main__':
    main()
