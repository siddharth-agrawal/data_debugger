import json

def verify_input(inp, options):
    # natural numbers attached to each option starting from 1
    if not inp.isdigit():
        return False, inp

    value = int(inp)
    if value < 0 or value > len(options):
        return False, value

    return True, value


def get_input(init_message, options, info_dict=None):
    """
    Ask for input and check if it's valid using the provided information.
    """
    print('\n\n')

    # dict block for printing data example information
    if info_dict is not None:
        print(json.dumps(info_dict, indent=2))

    # information related to input being asked for
    print(init_message)

    for idx, option in enumerate(options):
        print(f'[{idx+1}]. {option}')

    print('Use 0 to exit app')

    valid = False

    # keep looping until valid input is provided
    while not valid:
        inp = input()
        valid, value = verify_input(inp, options)

        if not valid:
            print(f'{value} is not a valid input, please try again.')

    return value

