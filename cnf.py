""" BIDIRECTIONAL ELIMINATION (See: https://en.wikipedia.org/wiki/Logical_biconditional) """


def bidirectional_elimination(components):
    if components[0] == "iff":
        literal_1 = components[1]
        literal_2 = components[2]
        components[0] = "and"
        components[1] = ["implies", literal_1, literal_2]
        components[2] = ["implies", literal_2, literal_1]

    for literal in components:
        if len(literal) > 1:
            bidirectional_elimination(literal)


""" IMPLICATION ELIMINATION (See: http://web.stanford.edu/class/cs221/lectures/logic2-6pp.pdf)"""


def implication_elimination(components):
    if components[0] == "implies":
        literal_1 = components[1]
        components[0] = "or"
        components[1] = ["not", literal_1]

    for literal in components:
        if len(literal) > 1:
            implication_elimination(literal)


""" DE-MORGAN'S LAW """


def parse_components_using_demorgan_law(components):
    if components[0] == "not":
        literal = components[1]

        if literal[0] == "not":
            del components[:]

            if len(literal[1]) == 1:
                components.append(literal[1])
            else:
                for literal_1 in literal[1]:
                    components.append(literal_1)

                if len(components) > 1:
                    parse_components_using_demorgan_law(components)

        elif literal[0] == "or":
            del components[:]

            components.append("and")

            for literal_1 in literal:
                if literal_1 == "or":
                    continue
                else:
                    components.append(["not", literal_1])

        elif literal[0] == "and":
            del components[:]

            components.append("or")

            for literal_1 in literal:
                if literal_1 == "and":
                    continue
                else:
                    components.append(["not", literal_1])

    for literal in components:
        if len(literal) > 1:
            parse_components_using_demorgan_law(literal)


""" DISTRIBUTIVE LAW """


def distributivity(components):
    if components[0] == "or":
        if len(components[2]) > 1 and components[2][0] == "and":
            literal_1 = components[1]
            literal_2 = components[2]

            del components[:]

            components.append("and")

            for literal_x in literal_2:
                if literal_x == "and":
                    continue

                components.append(["or", literal_1, literal_x])
        elif len(components[1]) > 1 and components[1][0] == "and":
            literal_1 = components[1]
            literal_2 = components[2]

            del components[:]

            components.append("and")

            for literal_x in literal_1:
                if literal_x == "and":
                    continue

                components.append(["or", literal_x, literal_2])

    for literal in components:
        if len(literal) > 1:
            distributivity(literal)


""" OUTER RECURSIVE DISTRIBUTIVE LAW """


def distributivity_recursion(components):
    if components[0] == "or":
        if len(components[2]) > 1 and components[2][0] == "and":
            literal_1 = components[1]
            literal_2 = components[2]

            del components[:]

            components.append("and")

            for literal_x in literal_2:
                if literal_x == "and":
                    continue

                components.append(["or", literal_1, literal_x])
        elif len(components[1]) > 1 and components[1][0] == "and":
            literal_1 = components[1]
            literal_2 = components[2]

            del components[:]

            components.append("and")

            for literal_x in literal_1:
                if literal_x == "and":
                    continue

                components.append(["or", literal_x, literal_2])


""" ASSOCIATIVE LAW """


def parse_components_using_association_law(components):
    if components[0] == "and":
        temp_components = [component for component in components]

        del components[:]

        for literal in temp_components:
            if literal == "and":
                components.append("and")
            else:
                if literal[0] != "and":
                    components.append(literal)
                else:
                    for literal_x in literal:

                        if literal_x == "and":
                            continue
                        else:
                            components.append(literal_x)

    if components[0] == "or":
        temp_components = [component for component in components]

        del components[:]

        for literal in temp_components:
            if literal == "or":
                components.append("or")
            else:
                if literal[0] != "or":
                    components.append(literal)
                else:
                    for literal_x in literal:
                        if literal_x == "or":
                            continue
                        else:
                            components.append(literal_x)

    for literal in components:
        if len(literal) > 1:
            parse_components_using_association_law(literal)


""" REMOVE PARENTS """


def remove_parents(components):
    i = 0
    for literal in components:
        if len(literal) == 1:
            aux = str(literal)

            if len(aux) > 1:
                components[i] = aux[2]
        elif len(literal) > 1:
            remove_parents(literal)

        i = i + 1


""" REMOVE DUPLICATES """


def remove_duplicates(components):
    delete_literals = []

    if components[0] == "and" or components[0] == "or":
        for x in range(0, len(components)):
            for y in range(x + 1, len(components)):
                literal_1 = sorted(components[x])
                literal_2 = sorted(components[y])

                if literal_1 == literal_2:
                    delete_literals.append(components[y])

    if len(delete_literals) >= 1:
        temp_components = []

        for literal in delete_literals:
            flag = 1

            for literal_x in components:
                if literal == literal_x and flag == 1:
                    flag = 0
                    continue
                else:
                    temp_components.append(literal_x)

        del components[:]

        for literal in temp_components:
            components.append(literal)

    for literal in components:
        if len(literal) > 1:
            remove_duplicates(literal)


""" REMOVE SINGLE LITERALS WITH AND-OR """


def remove_single_literals(components):
    if len(components) == 2 and components[0] != "not":
        del components[0]

    for literal in components:
        if len(literal) > 1 and isinstance(literal, list):
            remove_single_literals(literal)


def quality_check(components):
    if len(components) == 1 and len(components[0]) > 1:
        literal = components[0]

        del components[:]

        for literal_x in literal:
            components.append(literal_x)

    for literal in components:
        if len(literal) > 1:
            quality_check(literal)


def get_cnf_from_list(sentence_list):
    components = eval(sentence_list)  # convert string to list

    bidirectional_elimination(components)
    implication_elimination(components)
    parse_components_using_demorgan_law(components)
    distributivity(components)
    flag = 1

    while components[0] == "or" and flag == 1:
        if len(components[2]) > 1 and components[2][0] == "and":
            distributivity_recursion(components)
            flag = 1
        elif len(components[1]) > 1 and components[1][0] == "and":
            distributivity_recursion(components)
            flag = 1
        else:
            flag = 0

    parse_components_using_association_law(components)
    remove_parents(components)
    remove_duplicates(components)
    remove_single_literals(components)
    quality_check(components)
    remove_parents(components)

    check = 1
    if components[0] == "and":
        temp_literal = components[1]

        for x in range(1, len(components)):
            if temp_literal != components[x]:
                check = 0

    if check == 1:
        remove_duplicates(components)
        remove_single_literals(components)
        quality_check(components)
        remove_parents(components)

    return components


""" 
    Main part of the program 
"""

sentence = get_cnf_from_list('["or", "A", ["and", ["not", "B"], "C"]]')

print sentence
