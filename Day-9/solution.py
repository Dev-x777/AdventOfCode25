from functools import reduce  # kept for your style, not used
import math  # not used
from pathlib import Path
from collections import Counter  # not used

from itertools import combinations
from shapely.geometry import Polygon, box
from shapely.prepared import prep

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

type Point = tuple[int, int]


def parse_input(text: str) -> list[Point]:
    lines = text.strip().split("\n")
    coords: list[Point] = []
    for line in lines:
        if not line.strip():
            continue
        x_str, y_str = line.split(",")
        coords.append((int(x_str), int(y_str)))
    return coords


def max_rectangle_area_part1(points: list[Point]) -> int:
    """Largest rectangle with red corners, no restriction on inside tiles."""
    n = len(points)
    if n < 2:
        return 0

    max_area = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area


def max_rectangle_area_part2(points: list[Point]) -> int:
    """
    Largest rectangle with red corners where every tile in the rectangle
    is red or green (i.e. the whole rectangle lies inside the polygon).
    """
    n = len(points)
    if n < 2:
        return 0

    # Polygon formed by the red tiles in given order
    poly = Polygon(points)
    prepared_poly = prep(poly)

    max_area = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        min_x, max_x = (x1, x2) if x1 <= x2 else (x2, x1)
        min_y, max_y = (y1, y2) if y1 <= y2 else (y2, y1)

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        area = width * height

        # Prune small rectangles
        if area <= max_area:
            continue

        # Continuous rectangle region
        rect = box(min_x, min_y, max_x, max_y)

        # covers() allows boundary to lie exactly on the polygon edge,
        # which matches "red or green tiles" (boundary + inside).
        if prepared_poly.covers(rect):
            max_area = area

    return max_area


def solve(text: str) -> tuple[int, int]:
    points = parse_input(text)
    part1 = max_rectangle_area_part1(points)
    part2 = max_rectangle_area_part2(points)
    return part1, part2


def main():
    # Example check
    example_part1, example_part2 = solve(input_example_text)
    print(f"The solution for the example is: {example_part1=}, {example_part2=}")
    assert example_part1 == 50
    assert example_part2 == 24

    # Real input
    part1, part2 = solve(input_text)
    print(f"The solution for the input is: {part1=}, {part2=}")


if __name__ == "__main__":
    main()
