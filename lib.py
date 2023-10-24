PRECEDENCE = {
    "¬" : 5,
    "∧" : 4,
    "∨" : 3,
    "⇒" : 2,
    "⇔" : 1
}

def is_proposition(token: str) -> bool:
    """Takes a token from a logical formula and returns whether that token is 
    a valid propositional identifier. In the version of the logical language
    that this parser uses, a valid propositional identifier can only be a
    single alphabetical character."""
    if token.isalpha() and len(token) == 1:
        return True
    return False

def is_operator(token: str) -> str:
    """Takes a token from a logical formula and returns whether that token is
    an operator or not. Valid operators are ¬, ∧, ∨, ⇒, and ⇔."""
    if token in PRECEDENCE:
        return True
    return False

def pad_zeros(num: str, length: int) -> str:
    """Takes a string representation of a binary number and pads it with zeros
    on the left side until it is the required `length`."""
    while len(num) != length:
        num = "0" + num
    return num

def count_identifiers(exp: str) -> tuple[int, list]:
    """Takes a logical formula `exp` and counts the number of unique
    propositional identifiers that appear in it."""
    exp = exp.replace(" ", "")

    # using  set to get rid of duplicates
    identifiers = set()

    for token in exp:
        if is_proposition(token):
            identifiers.add(token)

    return (len(identifiers), sorted(list(identifiers)))

def produce_truth_combinations(count: int, identifiers: list) -> list[dict]:
    """Takes a list of individual prime propositions and returns a list of
    dictionaries, each of which represents a unique combination of truth values
    for the propositions."""

    truth_combinations = []

    # basically count down in binary
    for i in range(pow(2, len(identifiers)) - 1, -1, -1):
        combination = {}
        binary = pad_zeros(str(bin(i))[2:], count)

        for i in range(count):
            if binary[i] == "0":
                combination[identifiers[i]] = False
            else:
                combination[identifiers[i]] = True
        
        truth_combinations.append(combination)

    return truth_combinations

def shunting_yard(exp: str) -> str:
    """Takes an infix propositional logic expression and returns the matrix 
    converted to postfix (Reverse Polish) notation."""
    # get rid of any spaces in the infix expression
    exp = exp.replace(" ", "")

    output_queue = []
    operator_stack = []

    for token in exp:
        # propositions are directly pushed to the output queue
        if is_proposition(token):
            output_queue.append(token)

        # operators are pushed to the operator stack after all
        # higher-precedence operators from the stack are
        # popped off and pushed to the output queue
        elif is_operator(token):
            while len(operator_stack) and operator_stack[-1] != "(" and PRECEDENCE[operator_stack[-1]] > PRECEDENCE[token]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)

        # left parens are directly pushed to the output queue
        # they help maintain the specified order of operations
        # during parsing but due to the nature of RPN, they are unnecesary
        # in the final expression and are discarded later on
        elif token == "(":
            operator_stack.append(token)

        # the only possibility left is a right parens and this is a bit
        # complicated because we have to make sure every right parens
        # has a matching left parens because otherwise the formula
        # is not well-formed
        else:
            # there must be at least one element left in the stack:
            # the matching left parens
            assert len(operator_stack) != 0

            # everything else gets popped off and pushed to the output queue
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())

                # check that the queue isn't empty before we reach a left parens
                assert len(operator_stack) != 0

            assert operator_stack[-1] == "("

            # pop off and discard the left parens because they are unnecessary
            #  in RPN
            operator_stack.pop()
    
    # any remaining operators get indiscriminately popped off and pushed to the
    #  output queue
    while len(operator_stack):
        # hedging against missing right parens at the end of the formula
        assert operator_stack[-1] != "("

        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate_postfix(exp: str, truth_values: dict) -> bool:
    """Takes a postfix (RPN) expression and evaluates it, using `truth_values`
    to assign truth values to the prime propositions in the order that they
    are encountered in the expression."""

    eval_stack = list(exp)
    current = []

    # while there are still propositions left on the stack or there is an 
    # operator left to be applied to the propositions in `current`
    while len(eval_stack) > 1 or is_operator(eval_stack[0]):
        if isinstance(eval_stack[0], bool):
            current.append(eval_stack.pop(0))

        elif is_proposition(eval_stack[0]):
            current.append(truth_values[eval_stack.pop(0)])
        
        else:
            operator = eval_stack.pop(0)
            # negation is a unary operator
            # strictly speaking, this is a shortcut: i should have put the
            # negation of the proposition back onto the stack and then
            # pulled it back out but eh
            if operator == "¬":
                current[-1] = not current[-1]
            else:
                match operator:
                    case "∧":
                        eval_stack.insert(0, current[-2] and current[-1])
                    case "∨":
                        eval_stack.insert(0, current[-2] or current[-1])
                    case "⇒":
                        eval_stack.insert(0, (not current[-2]) or current[-1])
                    case "⇔":
                        eval_stack.insert(0, current[-2] == current[-1])
                
                current = current[0: -2]
    
    return eval_stack[0]

def main():
    print(produce_truth_combinations(*(count_identifiers("¬p ∧ q ∨ ¬q ∧ r"))))

if __name__ == "__main__":
    main()