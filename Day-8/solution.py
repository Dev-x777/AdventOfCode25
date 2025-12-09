from functools import reduce
import math
from pathlib import Path
from collections import Counter

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Vec = tuple[int, int, int]


def distance(vec1: Vec, vec2: Vec) -> float:
    return math.dist(vec1, vec2)


def parse_input(text: str) -> list[Vec]:
    lines = text.strip().split("\n")
    coords = [tuple(map(int, line.split(","))) for line in lines]
    return coords  # pyright: ignore[reportReturnType]


def add_connections(
    connections: dict[Vec, set[Vec]],
    vec1: Vec,
    vec2: Vec,
):
    if vec1 not in connections:
        connections[vec1] = set()
    if vec2 not in connections:
        connections[vec2] = set()
    connections[vec1].add(vec2)
    connections[vec2].add(vec1)


def step_part1(
    colored_coords: dict[Vec, int],
    connections: dict[Vec, set[Vec]],
    closest_pairs: list[tuple[Vec, Vec, float]],
):
    # Find closest pair, that is not yet connected
    pair: list[Vec] = []
    for vec1, vec2, dist in closest_pairs:
        # Not connected
        if vec1 in connections and vec2 in connections[vec1]:
            continue
        # Not itself
        if dist <= 0:
            continue
        pair = [vec1, vec2]
        # closest_pairs is already sorted by closest distance, so we can break here
        break

    # Assign color to junction box
    vec1, vec2 = pair
    new_color = max(colored_coords.values()) + 1
    color1 = colored_coords[vec1]
    color2 = colored_coords[vec2]
    new_color = color1 or color2 or new_color
    # Merge two circuits
    if color1 != 0 and color2 != 0:
        for vec, color in colored_coords.items():
            if color == color1 or color == color2:
                colored_coords[vec] = new_color
    # Set new color to the new connections
    colored_coords[vec1] = new_color
    colored_coords[vec2] = new_color
    add_connections(connections, vec1, vec2)

    # Return solution part2
    if min(colored_coords.values()) == max(colored_coords.values()):
        return vec1[0] * vec2[0]
    return None


def calc_part2(
    colored_coords: dict[Vec, int],
    connections: dict[Vec, set[Vec]],
    closest_pairs: list[tuple[Vec, Vec, float]],
):
    # Find closest pair, that is not yet connected
    for vec1, vec2, dist in closest_pairs:
        # Not connected
        if vec1 in connections and vec2 in connections[vec1]:
            continue
        # Not itself
        if dist <= 0:
            continue

        # Assign color to junction box
        new_color = max(colored_coords.values()) + 1
        color1 = colored_coords[vec1]
        color2 = colored_coords[vec2]
        new_color = color1 or color2 or new_color
        # Merge two circuits
        if color1 != 0 and color2 != 0:
            for vec, color in colored_coords.items():
                if color == color1 or color == color2:
                    colored_coords[vec] = new_color
        # Set new color to the new connections
        colored_coords[vec1] = new_color
        colored_coords[vec2] = new_color
        add_connections(connections, vec1, vec2)

        # Return solution part2
        if min(colored_coords.values()) == max(colored_coords.values()):
            return vec1[0] * vec2[0]
    return -1


def solve(input_text: str, repeat: int) -> tuple[int, int]:
    # Parse input file
    coords = parse_input(input_text)
    # Assign each vertex the color 0
    colored_coords = {i: 0 for i in coords}
    # Keep track of which vertices are connected
    connections: dict[Vec, set[Vec]] = {}
    # Pre-calculate the distances for each pair once
    closest_pairs = [
        (vec1, vec2, distance(vec1, vec2)) for vec1 in coords for vec2 in coords
    ]
    # Sort by distance ascending order
    closest_pairs.sort(key=lambda i: i[2])

    for _ in range(repeat):
        step_part1(colored_coords, connections, closest_pairs)

    # Soluton for part 1
    count = Counter(colored_coords.values())
    count.pop(0)
    top3 = count.most_common(3)
    solution_part1 = reduce(lambda i, j: i * j, (i[1] for i in top3))

    # Solution for part 2
    solution_part2 = calc_part2(colored_coords, connections, closest_pairs)

    return solution_part1, solution_part2


def main():
    # Part 1
    solution_example_part1 = solve(input_example_text, 10)
    answer_example_part1 = solution_example_part1[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 40

    solution = solve(input_text, 1000)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    solution_example_part2 = solve(input_example_text, 10)
    answer_example_part2 = solution_example_part2[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 25272

    solution_part2 = solve(input_text, 10)
    answer_part2 = solution_part2[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()