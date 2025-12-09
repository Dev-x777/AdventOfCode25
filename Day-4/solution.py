from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def get_neighbors(lines: list[str], y: int, x: int) -> int:
    height = len(lines)
    width = len(lines[0])
    offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
    assert len(offsets) == 8

    count_neighbors = 0
    for offset in offsets:
        new_y = offset[0] + y
        new_x = offset[1] + x
        if new_x < 0 or new_y < 0 or width <= new_x or height <= new_y:
            continue
        if lines[new_y][new_x] == "@":
            count_neighbors += 1
    return count_neighbors


def calculate_number_grid(lines: list[str]) -> list[list[int]]:
    height = len(lines)
    width = len(lines[0])
    number_grid = [[-1 if value == "." else 0 for value in line] for line in lines]
    for y in range(height):
        for x in range(width):
            count_neighbors = get_neighbors(lines, y, x)
            number_grid[y][x] = count_neighbors
    return number_grid


def calculate_removable(lines: list[str], number_grid: list[list[int]]) -> int:
    total_less_than_4 = 0
    for y in range(len(number_grid)):
        for x in range(len(number_grid[0])):
            if lines[y][x] == "@" and number_grid[y][x] < 4:
                total_less_than_4 += 1
    return total_less_than_4


def calculate_next_grid(lines: list[str], number_grid: list[list[int]]) -> list[str]:
    lines_copy = list(lines)
    for y in range(len(lines)):
        lines_copy[y] = "".join(
            "." if char == "." or number_grid[y][x] < 4 else "@"
            for x, char in enumerate(lines[y])
        )
    return lines_copy


def solve(input_text: str) -> tuple[int, int]:
    lines = input_text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    number_grid = calculate_number_grid(lines)
    part_1_count = calculate_removable(lines, number_grid)

    part_2_count = 0
    while 1:
        number_grid = calculate_number_grid(lines)
        change_conut = calculate_removable(lines, number_grid)
        if change_conut == 0:
            break
        part_2_count += change_conut
        lines = calculate_next_grid(lines, number_grid)

    # Part1, part2
    return part_1_count, part_2_count


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 13

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 43

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()