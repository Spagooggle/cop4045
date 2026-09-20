# -*- coding: utf-8 -*-
import csv


def display_top_collaborations(
        rated_file: str, casts_file: str) -> None:
    try:
        rated_movies = set()

        with open(rated_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                title = row["Title"]
                year = row["Year"]
                rated_movies.add((title, year))

        collaborations = {}

        with open(casts_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                title = row[0]
                year = row[1]
                director = row[2]
                actors = row[3:]

                if (title, year) in rated_movies:
                    for actor in actors:
                        pair = (director, actor)

                        if pair in collaborations:
                            collaborations[pair] += 1
                        else:
                            collaborations[pair] = 1

        ranking = [
            (director, actor, count)
            for (director, actor), count in collaborations.items()
        ]

        ranking.sort(key=lambda item: item[2], reverse=True)

        print("Top Collaborations:")

        for item in ranking:
            print(item)

    except Exception as error:
        print(f"There was a problem reading the files: {error}")
        raise


def display_top_actors(
        grossing_file: str, casts_file: str) -> None:
    try:
        grossing_movies = {}

        with open(grossing_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                title = row["Title"]
                year = row["Year"]

                money = row["USA Box Office"]
                money = money.replace("$", "")
                money = money.replace(",", "")
                money = float(money)

                grossing_movies[(title, year)] = money

        actor_totals = {}

        with open(casts_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                title = row[0]
                year = row[1]
                actors = row[3:]

                movie = (title, year)

                if movie in grossing_movies:
                    money = grossing_movies[movie]

                    for actor in actors:
                        if actor in actor_totals:
                            actor_totals[actor] += money
                        else:
                            actor_totals[actor] = money

        ranking = list(actor_totals.items())
        ranking.sort(key=lambda item: item[1], reverse=True)

        print("Top Actors:")

        for actor, money in ranking:
            print(actor, money)

    except Exception as error:
        print(f"There was a problem reading the files: {error}")
        raise


def main() -> None:
    
    display_top_collaborations(
        "imdb-top-rated.csv",
        "imdb-top-casts.csv",
    )

    print()

    display_top_actors(
        "imdb-top-grossing.csv",
        "imdb-top-casts.csv",
    )


if __name__ == "__main__":
    main()
                    


