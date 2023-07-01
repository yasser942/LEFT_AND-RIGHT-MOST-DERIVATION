FILE_LL = "ll2.txt"
FILE_LR = "lr2.txt"
FILE_INPUT = "input2.txt"



def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            print(f"\nRead input strings from file {FILE_INPUT}.", end="\n\n\n")
            lines = file.readlines()
            lines = lines[1:]
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"{filename} not found! The program will exit!")
        exit(1)


# Get new action according to the element in the stack and input
def getXY(table, non_terminal_list, terminal_list, action, stack, inputStr):
    x = 0
    y = 0
    if (len(stack) >= 1):
        for i in range(len(non_terminal_list)):
            if non_terminal_list[i] == stack[-1]:
                x = i

        for j in range(len(terminal_list)):
            if terminal_list[j] == inputStr[0]:
                y = j

        action[0] = table[x + 1][y + 1]
    else:
        action[0] = "ACCEPTED"


def readTable(filename):
    # open the file
    with open(filename, 'r') as f:
        # read the contents of the file
        contents = f.read()

    # split the contents into lines
    lines = contents.split('\n')

    # split each line into fields using semicolon as the delimiter and remove spaces
    fields = [line.split(';') for line in lines]
    fields = [[field.strip() for field in line] for line in fields]

    # retrieve the list and replace 'Ïµ' with 'ϵ'
    for i in range(len(fields)):
        for j in range(len(fields[i])):
            if 'Ïµ' in fields[i][j]:
                fields[i][j] = fields[i][j].replace('Ïµ', 'ϵ')

    return fields


def sliceAction(a, terminal_list, non_terminal_list, stack):
    i = len(a) - 1
    while i >= 0:
        found = False
        for term in terminal_list:
            if a[i - len(term) + 1:i + 1] == term:
                if term == 'ϵ':
                    stack.pop()
                else:
                    stack.append(term)
                i -= len(term)
                found = True
                break
        if not found:
            for non_term in non_terminal_list:
                if a[i - len(non_term) + 1:i + 1] == non_term:
                    stack.append(non_term)
                    i -= len(non_term)
                    found = True
                    break
        if not found:
            i -= 1


def LL_table(ll_table, input):
    stack = []
    stack.append("$")
    inputStr = splitLL_input(input, ll_table[0][1:])  # Split the input
    # depending on the terminals
    action = []

    action.append(ll_table[1][1])

    # Extract the terminal list from the first row starting at index 0, column 1
    terminal_list = ll_table[0][1:]

    # Extract the non-terminal list from the first column starting at index
    # 1, row 1
    non_terminal_list = [ll_table[i][0] for i in range(1, len(ll_table))]

    print(f"{'NO':<5}  | {'STACK':<10} | {'INPUT':<12} | {'ACTION':<20}")
    print("-" * 60)
    print(
        f"{1:<5}  | {''.join(stack):<10} | {''.join(inputStr):<12} | {action[0]:<10}")
    sliceAction(action[0].split('>')[1], terminal_list, non_terminal_list,
                stack)  # Splitting the elements in the action, reverses them
    # and pushes them into the stack

    counter = 2
    while (len(inputStr) != 0):  # This runs until nothing is left in the
        # input string

        if (len(action[0]) == 0):  # Reject when there's no matching action
            print(
                f"{counter:<5}  | {''.join(stack):<10} |"
                f" {''.join(inputStr):<12} | REJECTED")
            break
        else:
            print(f"{counter:<5}", end="")

            if (stack[len(stack) - 1] == inputStr[0]):
                print(f"  | {''.join(stack):<10} | {''.join(inputStr):<12} | ",
                      end="")
                removed = stack.pop()
                inputStr.pop(0)
                if (action[0] == "ACCEPTED"):
                    print(f"{'ACCEPTED':<20}")
                    break
                elif (len(action[0]) == 0):
                    print(f"{'REJECTED':<20}")
                    break
                else:
                    action[0] = removed
                    if (removed == '$'):
                        print(f"{'ACCEPTED':<10}")
                    else:
                        print(f"Match and remove {action[0]:<10}")

                getXY(ll_table, non_terminal_list, terminal_list, action, stack,
                      inputStr)  # Get new action according to the element in
                # the stack and input

            else:
                print(f"  | {''.join(stack):<10} | {''.join(inputStr):<12} | ",
                      end="")
                getXY(ll_table, non_terminal_list, terminal_list, action, stack,
                      inputStr)
                if (len(action[0]) == 0):
                    print(f"{'REJECTED':<20}")
                    break
                else:
                    print(f"{action[0]:<20}")
                stack.pop()
                sliceAction(action[0].split('>')[1], terminal_list,
                            non_terminal_list, stack)
            counter += 1


def check_ll_input(inputStr, terminals):  # Check if the input string is valid
    for elem in inputStr:
        if elem not in terminals:
            return False
    return True


def check_lr_input(inputStr, term_line):  # Check if the input string is valid
    terminals = [x for x in term_line if
                 x.islower() or x == '$']  # filter non-terminals
    first_terminals = terminals[:terminals.index(
        '$') + 1]  # slice first terminals and include '$'
    for elem in inputStr:
        if elem not in first_terminals:
            return False
    return True


def LR_table(lr_table, input):
    new_table = lr_table[1:]  # slice to remove the first row
    halt = True
    stack = []
    stack.append("1")
    line = 1
    pointer = 0
    no = 1

    print("{:<3} | {:<11} | {:<4} | {:<5} | {:<6}".format("NO", "STATE STACK",
                                                          "READ", "INPUT",
                                                          "ACTION"))
    print("-" * 60)

    while (halt):
        current_state = new_table[line][lr_table[1].index(input[pointer])]
        read = input[pointer]
        print(f"{str(no):<3} | {' '.join(stack):<11} | {read:<4} | ", end="")
        #  Three possible conditions, otherwise reject the input
        if (current_state.startswith("State")):
            pointer += 1  # Point to next character of the input
            next = current_state.split('_')  # Get the number of the state to
            # go next
            stack.append(next[1])  # Push the number of the state to the stack
            line = int(next[1])  # Get the index of the line of the next state
            action = "Shift to state " + ''.join(next[1])
            print(f"{input:<5} | {action:<6}")
        elif (current_state.startswith("Accept")):
            action = "ACCEPTED"
            print(f"{input:<5} | {action:<6}")
            break
        elif ('>' in current_state):  # This means we have a rule
            action = "Reverse " + current_state
            print(f"{input:<5} | {action:<6}")
            RH = current_state.split('>')[1]  # Right hand side
            LH = current_state.split('>')[0].replace('-', '')  # Left hand side

            substring = input[:-1][-len(RH):]  # Slice from the input a
            # substring depending on the length of the right hand side of the
            # rule
            if (substring == RH):  # Pop the characters if they all match
                for _ in range(len(substring)):
                    stack.pop()

                line = int(stack[len(stack) - 1])  # Determining the index of
                # the new line of the state
                pointer = pointer - len(substring)  # Move the pointer left
                # according to the length of the previous substring

                input = input.replace(substring, "")  # Delete the substring
                # from the input
                inputList = list(input)
                inputList.insert(len(inputList) - 1, LH)  # Insert the left
                # hand side of the rule to the input
                input = ''.join(inputList)
            else:
                action = "REJECTED"
                print(f"{input:<5} | {action:<6}")
                break
        else:
            action = "REJECTED"
            print(f"{input:<5} | {action:<6}")
            break
        no += 1


def splitLL_input(input, terminals):  # Splits the elements in input string
    # and returns them as a list

    tokens = []
    buffer = ""
    index = 0

    # Iterate through each character in the input string
    while index < len(input):
        char = input[index]
        if char in terminals:
            # If the character is a terminal symbol, add it to the tokens list
            if buffer:
                tokens.append(buffer)
                buffer = ""
            tokens.append(char)
            index += 1
        else:
            # If the character is not a terminal symbol, append it to the buffer
            buffer += char
            index += 1

    # Add any remaining characters in the buffer to the tokens list
    if buffer:
        tokens.append(buffer)
    return tokens


def main():
    global ll_table
    global lr_table
    ll_exists = True
    lr_exists = True

    try:
        ll_table = readTable(FILE_LL)  # Read tables from input.txt
    except FileNotFoundError:
        print(f"{FILE_LL} not found! The program might not work as expected!")
        ll_exists = False
    else:
        print(f"\nRead LL(1) parsing table from file {FILE_LL}.", end="\n")

    try:
        lr_table = readTable(FILE_LR)
    except FileNotFoundError:
        print(f"{FILE_LR} not found! The program might not work as expected!")
        lr_exists = False
    else:
        print(f"\nRead LR(1) parsing table from file {FILE_LR}.", end="\n")

    inputList = read_input_file(FILE_INPUT)  # Read input string

    for line in inputList:
        try:
            # Read line by line and split the elements by ;
            tableType = line.split(';')[0].strip()  # If the table is LL or LR
            inputString = line.split(';')[1]  # The remaining part of the string
            if (tableType == "LL" and ll_exists):
                if (check_ll_input(splitLL_input(inputString, ll_table[0][1:]),
                                   ll_table[0][1:])):  # Check the input if it is
                    # relevant to the table or not

                    print(
                        f"\nProcessing input string {inputString} for LL(1) parsing table.",
                        end="\n\n")
                    LL_table(ll_table, inputString)  # Main function for LL parsing
                else:
                    print(
                        f"\n*Provided input string {inputString} for LL(1) parsing is not valid.")
            elif (tableType == "LR" and lr_exists):
                if (check_lr_input(inputString, lr_table[1][1:])):  # Check if
                    # input is relevant

                    print(
                        f"\nProcessing input string {inputString} for LR(1) parsing table.",
                        end="\n\n")
                    LR_table(lr_table, inputString)  # Main function for LR parsing
                else:
                    print(
                        f"\n*Provided input string {inputString} for LR(1) parsing is not valid.")
            else:
                print(f"\nInvalid input file format.")
        except IndexError:
            print(f"\nInvalid input file format for "
                  f"{inputList.index(line) + 2}. line.")
        print("=" * 70)        


if __name__ == "__main__":
    main()
