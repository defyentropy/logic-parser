from lib import shunting_yard, evaluate_postfix, count_identifiers, produce_truth_combinations

# ASCII escape codes to print the truth values in colour
RED = "\033[0;31m"
GREEN = "\033[0;32m"
ENDCOLOUR = "\033[0m"

def main():
    exp = "(p ∨ q) ∧ (p ∨ r)"

    postfix = shunting_yard(exp)
    count, identifiers = count_identifiers(exp)
    truth_combinations = produce_truth_combinations(count, identifiers)

    for identifier in identifiers:
        print(identifier, end="\t")

    print("| Output")
    print("-" * 8 * (count + 1))

    for truth_combination in truth_combinations:
        for identifier in truth_combination:
            if truth_combination[identifier]:
                print("T", end="\t")
            else:
                print("F", end="\t")

        if evaluate_postfix(postfix, truth_combination):
            print("| " + GREEN + "T" + ENDCOLOUR)
        else:
            print("| " + RED + "F" + ENDCOLOUR)
    
if __name__ == "__main__":
    main()