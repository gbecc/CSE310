# 1. Name:
#      Gabriel Beccari
# 2. Assignment Name:
#      Lab 02: Authentication
# 3. Assignment Description:
#      Reads usernames and passwords from Lab02.json and authsenticate/validates a user by
#      checking that the username and password match at the same list index.
# 4. What was the hardest part? Be as specific as possible.
#      Research. I didn't remember much at all on how to prepare each of these steps in Python, so it took me a lot of time to go around find the concepts.
#       I ran into errors I didn't think of that I had to address, such as being in the right working directory 100% of the time. 
# 5. How long did it take for you to complete the assignment?
#      5 hours

import json
import os
import sys

FILENAME = "Lab02.json"

def file_path(name: str) -> str:
    # Keep it simple: look next to this script. 
    # This helps find the document wherever needed. Had issues with VS changing working directory.
    base = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    return os.path.join(base, name)

def load_credentials(json_filename: str):
    path = file_path(json_filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        print(f"Unable to open file {json_filename}.")
        sys.exit(0)

    usernames = data.get("username", [])
    passwords = data.get("password", [])

    # Make sure they're lists, & counts match.
    if not isinstance(usernames, list) or not isinstance(passwords, list) or len(usernames) != len(passwords):
        print("Data format error.")
        sys.exit(0)

    return usernames, passwords

def authenticate(usernames, passwords, user, pwd) -> bool:
    try:
        idx = usernames.index(user)
    except ValueError:
        return False
    return passwords[idx] == pwd

def main():
    usernames, passwords = load_credentials(FILENAME)
    user = input("Username: ")
    pwd = input("Password: ")
    if authenticate(usernames, passwords, user, pwd):
        print("You are authenticated!")
    else:
        print("You are not authorized to use the system.")

if __name__ == "__main__":
    main()