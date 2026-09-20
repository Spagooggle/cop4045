# -*- coding: utf-8 -*-
import csv


def add_user(sn: dict, username: str, fullname: str) -> bool:
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print(f"There was a problem adding the user: {error}")
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    try:
        if user1 not in sn or user2 not in sn:
            return False

        if user1 == user2:
            return False

        friends1 = sn[user1][1]
        friends2 = sn[user2][1]

        if user2 not in friends1:
            friends1.append(user2)

        if user1 not in friends2:
            friends2.append(user1)

        return True

    except Exception as error:
        print(f"There was a problem adding the friend: {error}")
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    try:
        if user1 not in sn or distance < 1:
            return []

        found = []
        current = [user1]

        for _ in range(distance):
            next_users = []

            for user in current:
                for friend in sn[user][1]:
                    if friend != user1 and friend not in found:
                        found.append(friend)
                        next_users.append(friend)

            current = next_users

            if not current:
                break

        return found

    except Exception as error:
        print(f"There was a problem getting the friends: {error}")
        raise


def save_network(filename: str, sn: dict) -> None:
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for username, info in sn.items():
                fullname = info[0]
                friends = info[1]

                writer.writerow([username, fullname] + friends)

    except Exception as error:
        print(f"There was a problem saving the network: {error}")
        raise


def load_network(filename: str) -> dict:
    try:
        sn = {}

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                username = row[0]
                fullname = row[1]
                friends = row[2:]

                sn[username] = (fullname, friends)

        return sn

    except Exception as error:
        print(f"There was a problem loading the network: {error}")
        raise


def main() -> None:

    sn = {
        "alice": ("Alice Smith", ["maria"]),
        "maria": ("Maria Cortez", ["alice", "joe", "david"]),
        "joe": ("Joseph Adams", ["maria", "eve"]),
        "eve": ("Evelyn Cooper", ["joe"]),
        "david": ("David Benson", ["maria"]),
    }

    print("Original network:")
    print(sn)
    print()

    print("Testing add_user:")
    print(add_user(sn, "brian", "Brian Fornaro"))
    print(add_user(sn, "alice", "Alice Smith"))
    print(sn)
    print()

    print("Testing add_friend:")
    print(add_friend(sn, "brian", "alice"))
    print(add_friend(sn, "brian", "unknown"))
    print(sn)
    print()

    print("Testing get_friends:")
    print("Alice distance 1:", get_friends(sn, "alice", 1))
    print("Alice distance 2:", get_friends(sn, "alice", 2))
    print("Alice distance 3:", get_friends(sn, "alice", 3))
    print()

    print("Testing save_network:")
    save_network("social_network.csv", sn)
    print("Network saved.")
    print()

    print("Testing load_network:")
    loaded_network = load_network("social_network.csv")
    print(loaded_network)


if __name__ == "__main__":
    main()

