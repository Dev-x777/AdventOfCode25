from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()

start_position = 50


def rotate(position: int, amount: int) -> int:
    return position + amount


def rotate_from_value(position: int, value: str) -> tuple[int, int]:
    """Returns tuple:
    end_position: int
    amount_of_times_crossed_zero: int
    """
    letter = value[0]
    assert letter in {"L", "R"}
    amount = int(value[1:])
    amount = amount if letter == "R" else -amount

    end_position = rotate(position, amount)
    amount_of_times_crossed_zero = abs(end_position // 100)
    end_position = end_position % 100
    if letter == "R" and end_position == 0:
        amount_of_times_crossed_zero -= 1
    if letter == "L" and position == 0:
        amount_of_times_crossed_zero -= 1
    return end_position, amount_of_times_crossed_zero


def solve(file_input: str) -> tuple[int, int]:
    current_position = start_position
    count_on_zero = 0
    count_crossed_zero = 0

    for line in file_input.split("\n"):
        line = line.strip()
        if line == "":
            continue

        current_position, amount_crossed_zero = rotate_from_value(
            current_position, line
        )
        if current_position == 0:
            count_on_zero += 1

        count_crossed_zero += amount_crossed_zero
    return count_on_zero, count_crossed_zero


def main():
    # Sanity checks part 1
    # print(len(input_text.split("\n")))
    assert rotate_from_value(95, "R5")[0] == 0
    assert rotate_from_value(0, "L5")[0] == 95

    # Sanity checks part 2
    assert rotate_from_value(0, "L5")[0] == 95
    assert rotate_from_value(0, "L5")[1] == 0
    assert rotate_from_value(1, "L2")[1] == 1
    assert rotate_from_value(50, "L68")[1] == 1
    assert rotate_from_value(99, "R2")[1] == 1
    assert rotate_from_value(1, "L1")[1] == 0
    assert rotate_from_value(99, "R1")[1] == 0

    solution_example = solve(input_example_text)
    assert solution_example[0] == 3
    assert solution_example[0] + solution_example[1] == 6, (
        solution_example[0],
        solution_example[1],
    )

    solution_part1 = solve(input_text)
    answer_part1 = solution_part1[0]
    print(f"Solution to day 01 part 1 is: {answer_part1=}")

    solution_part2 = solve(input_text)
    answer_part2 = solution_part2[0] + solution_part2[1]
    print(f"Solution to day 01 part 2 is: {answer_part2=}")


if __name__ == "__main__":
    main()