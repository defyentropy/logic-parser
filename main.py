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
    exps = [
        "(p ∨ q) ⇔ (q ∨ p)",
        "(p ∧ q) ⇔ (q ∧ p)",
        "(p ∧ (q ∧ r)) ⇔ ((p ∧ q) ∧ r)",
        "(p ∨ (q ∧ r)) ⇔ ((p ∨ q) ∧ (p ∨ r))",
        "(p ∧ (q ∨ r)) ⇔ ((p ∧ q) ∨ (p ∧ r))",
        "(p ∨ p) ⇔ (p)",
        "(p ∧ p) ⇔ (p)",
        # "(p ∨ ¬p) ⇔ (True)",
        # "(p ∧ ¬p) ⇔ (False)",
        "(¬(¬p)) ⇔ (p)",
        "(p ⇒ q) ⇔ (¬p ∨ q)",
        "(¬(p ∧ q)) ⇔ (¬p ∨ ¬q)",
        "(¬(p ∨ q)) ⇔ (¬p ∧ ¬q)",
        "(p ⇔ q) ⇔ ((p ⇒ q) ∧ (q ⇒ p))",
    ]

    for exp in exps:
        generate_truth_table(exp)
        print()
        # print(exp)

    print("Complete!")


def generate_truth_table(exp: str, file_name=""):
    postfix = shunting_yard(exp)
    count, identifiers = count_identifiers(exp)
    truth_combinations = produce_truth_combinations(count, identifiers)
    subexps = get_subexps(postfix, list_format=True)

    if file_name:
        with open(f"output/{file_name}", "a", newline="", encoding="utf-8") as csv_file:
            ttable_writer = csv.writer(csv_file)
            ttable_writer.writerow([exp])
            ttable_writer.writerow([])
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
            ttable_writer.writerow([])
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
