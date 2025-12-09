from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def step(diagram: list[list[int]], row: int) -> int:
    # Return the new diagram
    # Return the number of splits happened in this split

    # Skip when reaching last line
    if len(diagram) <= row + 1:
        return 0

    split_count = 0
    for index, char in enumerate(diagram[row]):
        if char == -2:
            diagram[row + 1][index] = 1
        if 0 < char and diagram[row + 1][index] == -1:
            split_count += 1
            if 0 <= diagram[row + 1][index - 1]:
                diagram[row + 1][index - 1] += char
            if 0 <= diagram[row + 1][index + 1]:
                diagram[row + 1][index + 1] += char
        if 0 < char and 0 <= diagram[row + 1][index]:
            diagram[row + 1][index] += char

    return split_count


def solve(input_text: str) -> tuple[int, int]:
    parsed = [list(line.strip()) for line in input_text.split("\n") if line.strip()]

    # Copy 2d array and replace '.' with 0
    # '.' is marked as 0, '^' is marked as -1, 'S' is marked as -2
    new_diagram = [[0 if i == "." else i for i in line] for line in parsed]
    new_diagram = [[-1 if i == "^" else i for i in line] for line in new_diagram]
    new_diagram2: list[list[int]] = [
        [-2 if i == "S" else i for i in line] for line in new_diagram
    ]  # pyright: ignore[reportAssignmentType]
    total_splits = 0
    for line_number, _line in enumerate(parsed):
        split_this_step = step(new_diagram2, line_number)
        total_splits += split_this_step

    timelines_count = 0
    for last_line_char in new_diagram2[-1]:
        if 0 < last_line_char:
            timelines_count += last_line_char

    return total_splits, timelines_count


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 21

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 40

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()