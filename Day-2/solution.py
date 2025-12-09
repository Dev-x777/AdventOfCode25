from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def number_is_valid_part1(value: str) -> bool:
    length = len(value)
    if length % 2 == 1:
        return True
    half_length = length // 2
    first_half = value[:half_length]
    second_half = value[half_length:]
    return first_half != second_half


def number_is_valid_part2(value: str) -> bool:
    value_length = len(value)
    for length in range(1, value_length // 2 + 1):
        first_part = value[:length]
        factor = value_length // len(first_part)
        generated = factor * first_part
        if generated == value:
            return False
    return True


def solve(input_text: str) -> tuple[int, int]:
    invalid_ids_part1: list[int] = []
    invalid_ids_part2: list[int] = []

    number_ranges = input_text.strip().split(",")
    number_ranges_split = [my_range.split("-") for my_range in number_ranges]
    for start_value, end_value in number_ranges_split:
        # print(f"ranges: {start_value=} {end_value=}")
        for value in range(int(start_value), int(end_value) + 1):
            if not number_is_valid_part1(str(value)):
                # print(value)
                invalid_ids_part1.append(value)
            if not number_is_valid_part2(str(value)):
                # print(value)
                invalid_ids_part2.append(value)
    return sum(invalid_ids_part1), sum(invalid_ids_part2)


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 1227775554

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 4174379265

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()