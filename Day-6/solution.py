from functools import reduce
from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def calculate_column_part1(line: list[str]) -> int:
    # Remove empty spaces around operator
    operation = line[-1].strip()
    numbers = map(int, line[:-1])
    if operation == "+":
        return sum(numbers)
    if operation == "*":

        def multiply(x: int, y: int) -> int:
            return x * y

        return reduce(multiply, numbers)
    return -1


def calculate_column_part2(line: list[str]) -> int:
    # Remove empty spaces around operator
    operation = line[-1].strip()

    # Extract numbers correctly
    numbers_str = line[:-1]
    longest_number_len = len(numbers_str[0])

    numbers: list[int] = []
    for i in range(longest_number_len - 1, -1, -1):
        current_number: list[str] = []
        for number in numbers_str:
            if len(number) <= i:
                continue
            current_number.append(number[i])
        numbers.append(int("".join(current_number)))

    if operation == "+":
        return sum(numbers)
    if operation == "*":

        def multiply(x: int, y: int) -> int:
            return x * y

        return reduce(multiply, numbers)
    return -1


def solve(input_text: str) -> tuple[int, int]:
    lines = [line for line in input_text.split("\n")]

    # Detect columns with empty spaces
    spaces_columns_indeces: list[int] = []
    for column_index in range(len(lines[0])):
        line_is_separator = True
        for line in lines:
            if line[column_index] != " ":
                line_is_separator = False
                break
        if line_is_separator:
            spaces_columns_indeces.append(column_index)
    # Include last column of numbers and operator
    spaces_columns_indeces.append(-1)

    # Collect columns by group
    sanitized_input: list[list[str]] = []
    prev_column_index = 0
    for column_index in spaces_columns_indeces:
        current_column: list[str] = []
        for line in lines:
            if column_index != -1:
                current_column.append(line[prev_column_index:column_index])
            else:
                # Include last character of a line
                current_column.append(line[prev_column_index:])
        prev_column_index = column_index + 1
        sanitized_input.append(current_column)

    my_sum_part1 = 0
    for line in sanitized_input:
        my_sum_part1 += calculate_column_part1(line)

    my_sum_part2 = 0
    for line in sanitized_input:
        my_sum_part2 += calculate_column_part2(line)
    return my_sum_part1, my_sum_part2


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 4277556

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 3263827

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()