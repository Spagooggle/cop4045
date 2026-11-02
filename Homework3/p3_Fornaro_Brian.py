# -*- coding: utf-8 -*-

from __future__ import annotations
import random
import matplotlib.pyplot as plt


class Island:
    """A grid containing prey, predators, and humans."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0, count_humans: int = 0) -> None:
        """Create the island and add the starting animals."""
        if n <= 0 or min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Invalid island size or animal count")
        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Too many animals for the grid")

        self.grid_size = n
        self.grid: list[list[Animal | int]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Place the animals in random empty spots."""
        for animal_type, count in [(Prey, prey_count), (Predator, predator_count),
                                   (Human, count_humans)]:
            for _ in range(count):
                x = random.randrange(self.grid_size)
                y = random.randrange(self.grid_size)
                while self.animal(x, y) != 0:
                    x = random.randrange(self.grid_size)
                    y = random.randrange(self.grid_size)
                self.register(animal_type(self, x, y))

    def clear_all_moved_flags(self) -> None:
        """Reset the moved flags before each turn."""
        for row in self.grid:
            for animal in row:
                if isinstance(animal, Animal):
                    animal.clear_moved_flag()

    def size(self) -> int:
        """Return the size of the grid."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Put an animal on the grid."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove an animal from the grid."""
        if self.animal(animal.x, animal.y) is animal:
            self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Animal | int:
        """Return the animal at x, y, or -1 if outside the grid."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Return a string showing the island grid."""
        result = ""
        for y in range(self.grid_size - 1, -1, -1):
            for x in range(self.grid_size):
                animal = self.animal(x, y)
                result += ("." if animal == 0 else str(animal)) + "  "
            result += "\n"
        return result

    def count_prey(self) -> int:
        """Return the number of prey."""
        return sum(isinstance(a, Prey) for row in self.grid for a in row)

    def count_predators(self) -> int:
        """Return the number of predators."""
        return sum(type(a) is Predator for row in self.grid for a in row)

    def count_humans(self) -> int:
        """Return the number of humans."""
        return sum(isinstance(a, Human) for row in self.grid for a in row)


class Animal:
    """An animal that can move and breed."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """Set the animal's position and symbol."""
        self.island = island
        self.x = x
        self.y = y
        self.name = s
        self.moved = False
        self.breed_clock = 0

    def position(self) -> tuple[int, int]:
        """Return the animal's position."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the animal's symbol."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> tuple[int, int] | None:
        """Return a neighboring spot of the given type, or None."""
        directions = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                      (1, 0), (-1, -1), (0, -1), (1, -1)]
        for dx, dy in directions:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < self.island.size() and 0 <= y < self.island.size():
                if type(self.island.animal(x, y)) is type_looking_for:
                    return x, y
        return None

    def move(self) -> None:
        """Move to an empty neighboring spot if possible."""
        if not self.moved:
            spot = self.check_grid()
            if spot is not None:
                self.island.remove(self)
                self.x, self.y = spot
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Create a new animal when the breeding clock reaches zero."""
        if self.breed_clock <= 0:
            spot = self.check_grid()
            if spot is not None:
                self.breed_clock = self.breed_time
                baby = type(self)(self.island, spot[0], spot[1])
                self.island.register(baby)

    def clear_moved_flag(self) -> None:
        """Allow the animal to move next turn."""
        self.moved = False


class Prey(Animal):
    """An animal that moves and breeds."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """Initialize a prey animal."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Update the breeding clock."""
        self.breed_clock -= 1


class Predator(Animal):
    """An animal that eats prey and can starve."""

    breed_time: int = 6
    starve_time: int = 5
    food_type: type[Animal] = Prey

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """Initialize a predator and its clocks."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time

    def clock_tick(self) -> None:
        """Update the clocks and remove a starving predator."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat a neighboring food animal if one is found."""
        if not self.moved:
            spot = self.check_grid(self.food_type)
            if spot is not None:
                food = self.island.animal(spot[0], spot[1])
                if isinstance(food, Animal):
                    self.island.remove(food)
                self.island.remove(self)
                self.x, self.y = spot
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


class Human(Predator):
    """A human that hunts predators instead of prey."""

    breed_time: int = 15
    starve_time: int = 15
    hunt_time: int = 4
    food_type: type[Animal] = Predator

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """Initialize a human and its hunting clock."""
        super().__init__(island, x, y, s)
        self.age = 0

    def eat(self) -> None:
        """Hunt a predator every hunt_time turns."""
        if (self.age + 1) % self.hunt_time == 0:
            super().eat()

    def clock_tick(self) -> None:
        """Update the human's age, breeding, and starving clocks."""
        self.age += 1
        super().clock_tick()


def main(predator_breed_time: int = 6, predator_starve_time: int = 5,
         initial_predators: int = 10, prey_breed_time: int = 3,
         initial_prey: int = 50, size: int = 10, ticks: int = 1000,
         human_breed_time: int = 15, human_starve_time: int = 15,
         human_hunt_time: int = 4, initial_humans: int = 3) -> None:
    """Run the simulation and graph all three populations."""
    if min(predator_breed_time, predator_starve_time, prey_breed_time,
           human_breed_time, human_starve_time, human_hunt_time) <= 0:
        raise ValueError("Time values must be positive")

    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    random.seed(7)
    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print("Z23672108")
    print("\nStarting island:")
    print(isle)

    prey_list = [isle.count_prey()]
    predator_list = [isle.count_predators()]
    human_list = [isle.count_humans()]
    stable = 0

    for tick in range(1, min(ticks, 1000) + 1):
        isle.clear_all_moved_flags()
        animals = [a for row in isle.grid for a in row if isinstance(a, Animal)]

        for animal in animals:
            if isle.animal(animal.x, animal.y) is not animal:
                continue
            if isinstance(animal, Predator):
                animal.eat()
            animal.move()
            animal.breed()
            animal.clock_tick()

        prey_list.append(isle.count_prey())
        predator_list.append(isle.count_predators())
        human_list.append(isle.count_humans())

        current = (prey_list[-1], predator_list[-1], human_list[-1])
        previous = (prey_list[-2], predator_list[-2], human_list[-2])
        if tick % 10 == 0:
            print(f"Tick {tick}: Prey={current[0]}, Predators={current[1]}, Humans={current[2]}")

        if current == previous:
            stable += 1
        else:
            stable = 0
        if stable >= max(30, prey_breed_time, predator_breed_time,
                         human_breed_time, human_starve_time):
            print(f"Populations stabilized at tick {tick}.")
            break

    print("\nEnding island:")
    print(isle)
    print(f"Final populations: Prey={prey_list[-1]}, "
          f"Predators={predator_list[-1]}, Humans={human_list[-1]}")

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.title("Prey, Predator, and Human Populations")
    plt.xlabel("Time (ticks)")
    plt.ylabel("Population")
    plt.legend()
    plt.grid(True)
    plt.savefig("p3_population_chart.png")
    plt.show()


if __name__ == "__main__":
    main()

