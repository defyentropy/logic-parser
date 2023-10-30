from lib import (
    shunting_yard,
    evaluate_postfix,
    count_identifiers,
    produce_truth_combinations,
    get_subexps,
)

import sys
import csv

# ASCII escape codes to print the truth values in colour
RED = "\033[0;31m"
GREEN = "\033[0;32m"
ENDCOLOUR = "\033[0m"


def main():
    if len(sys.argv) == 2:
        exp = sys.argv[1]
        output_to_file = False
    elif len(sys.argv) == 4 and sys.argv[1] == "-o":
        exp = sys.argv[3]
        output_to_file = True
        file_name = sys.argv[2]

    postfix = shunting_yard(exp)
    count, identifiers = count_identifiers(exp)
    truth_combinations = produce_truth_combinations(count, identifiers)
    subexps = get_subexps(postfix, list_format=True)

    if output_to_file:
        with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
            ttable_writer = csv.writer(csv_file)

            ttable_writer.writerow(identifiers + subexps)

            for truth_combination in truth_combinations:
                row = [
                    "T" if truth_combination[identifier] else "F"
                    for identifier in truth_combination
                ]
                row.extend(
                    [
                        "T" if val else "F"
                        for val in evaluate_postfix(postfix, truth_combination)
                    ]
                )

                ttable_writer.writerow(row)
    else:
        for identifier in identifiers:
            print(identifier, end="\t")

        print(f"| Output")
        print("-" * 8 * (count + 1))  # tab width is 8, so 8 "-"s for every tab

        for truth_combination in truth_combinations:
            for identifier in truth_combination:
                if truth_combination[identifier]:
                    print("T", end="\t")
                else:
                    print("F", end="\t")

            if evaluate_postfix(postfix, truth_combination)[-1]:
                print("| " + GREEN + "T" + ENDCOLOUR)
            else:
                print("| " + RED + "F" + ENDCOLOUR)


if __name__ == "__main__":
    main()
