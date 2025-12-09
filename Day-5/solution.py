from pathlib import Path

input_path = Path(__file__).parent / "input.txt"
input_text = input_path.read_text()
input_example_path = Path(__file__).parent / "example_input.txt"
input_example_text = input_example_path.read_text()


def parse_input(input_text: str):
    ranges: list[tuple[int, int]] = []
    collected_ids: list[int] = []

    second_part = False
    for line in input_text.split("\n"):
        if line.strip() == "":
            second_part = True
            continue

        if second_part is False:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
        else:
            collected_ids.append(int(line.strip()))

    ranges.sort(key=lambda i: i[0])
    collected_ids.sort()
    return ranges, collected_ids


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    [10-20, 15-25] => [10-25]
    """
    new_ranges = [ranges[0]]
    for start, end in ranges[1:]:
        last_range_start, last_range_end = new_ranges[-1]
        if last_range_start <= start <= last_range_end:
            new_ranges[-1] = last_range_start, max(end, last_range_end)
        else:
            new_ranges.append((start, end))
    return new_ranges


def solve(input_text: str) -> tuple[int, int]:
    ranges, collected_ids = parse_input(input_text)

    # Sanity check: do duplicates exist?
    assert len(set(collected_ids)) == len(collected_ids)

    fresh_ids: set[int] = set()
    for start, end in ranges:
        for number in collected_ids:
            if number < start:
                continue
            if end < number:
                break
            fresh_ids.add(number)

    merged_ranges = merge_ranges(ranges)
    answer_part2 = sum(end - start + 1 for start, end in merged_ranges)

    return len(fresh_ids), answer_part2


def main():
    # Part 1
    solution_example = solve(input_text=input_example_text)
    answer_example_part1 = solution_example[0]
    print(f"The solution for the example for part1 is: {answer_example_part1=}")
    assert answer_example_part1 == 3

    solution = solve(input_text)
    answer_part1 = solution[0]
    print(f"The solution for the part1 is: {answer_part1=}")

    # Part 2
    answer_example_part2 = solution_example[1]
    print(f"The solution for the example for part2 is: {answer_example_part2=}")
    assert answer_example_part2 == 14

    answer_part2 = solution[1]
    print(f"The solution for the part2 is: {answer_part2=}")


if __name__ == "__main__":
    main()