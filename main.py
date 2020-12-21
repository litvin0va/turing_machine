PRINT_STEPS = True
STEP_BY_STEP = True

class Action:
    def __init__(self, current_symbol, new_symbol, direction, new_state):
        self.current_symbol = current_symbol #string
        self.new_symbol = new_symbol #string
        self.direction = direction #Direction
        self.new_state = new_state #string

class State:
    def __init__(self, state_name):
        self.name = state_name #string
        self.actions = [] #list of Actions

    def find_star(self):
        for action in self.actions:
            if action.current_symbol == "*":
                return action

    def find_action(self, current_symbol):
        for action in self.actions:
            if (action.current_symbol == current_symbol) or (action.current_symbol == "_" and current_symbol is None):
                return action
        action_with_any_symbol = self.find_star()
        if action_with_any_symbol is None:
            raise Exception("Action not found")
        return action_with_any_symbol


class Turing:
    def __init__(self):
        self.states = []

    def get_state_index_by_name(self, state_name):
        for index in range(len(self.states)):
            if self.states[index].name == state_name:
                return index
        raise Exception("Error! State", state_name, "Not Found!")

    def get_or_create_state_index_by_name(self, state_name):
        try:
            index = self.get_state_index_by_name(state_name)
        except:
            self.states.append(State(state_name))
            index = len(self.states) - 1
        return index

    def get_state(self, index):
        return self.states[index]

def print_tape(tape):
    current_tape = ""
    for key in sorted(tape.keys()):
        current_tape += tape[key]
    print(current_tape)

def pharse_file(filename):
    file = open(filename, "r")
    input_tape = file.readline()
    mashine = Turing()

    for line in file:
        if line[0] == ';' or line == "\n":
            continue
        words_list = line.split()
        if len(words_list) < 5 or (";" in words_list and words_list.index(";") < 5):
            raise Exception("Error! Incorrect Input!")
        current_state_index = mashine.get_or_create_state_index_by_name(words_list[0])
        current_state = mashine.get_state(current_state_index)
        action = Action(words_list[1], words_list[2], words_list[3], words_list[4])
        current_state.actions.append(action)
    return input_tape, mashine



input_tape, mashine = pharse_file("input.txt")
input_tape = input_tape.rstrip('\n') #to remove last symbol
input_tape = input_tape.replace(" ", "_")
print(input_tape)

tape = {}
for i in range(len(input_tape)):
    tape[i] = input_tape[i]

head = 0
current_state = mashine.get_state(mashine.get_state_index_by_name("0"))
step = 0

while True:
    step += 1
    try:
        current_tape_symbol = tape[head]
    except:
        tape[head] = "_"
        current_tape_symbol = None

    if STEP_BY_STEP:
        command = input()  # q = Quit , s = Step, i = Info

        while command == "i":
            print("----------------------------------------------")
            print("Current State:", current_state.name)
            current_tape = ""
            head_tape = ""
            for key in sorted(tape.keys()):
                current_tape += tape[key]
                if key == head:
                    head_tape += "+"
                else:
                    head_tape += "_"
            print(current_tape)
            print(head_tape)

            print("----------------------------------------------")
            command = input()  # q = Quit , s = Step, i = Info

        if command == "q":
            break
        elif command != "s":
            print("Wrong command!")
            break


    action = current_state.find_action(current_tape_symbol)
    if action.new_symbol != '*':
        tape[head] = action.new_symbol

    if action.direction == "l":
        head -= 1
    elif action.direction == "r":
        head += 1
    elif action.direction != "*":
        raise Exception("Error! Incorrect Direction!")

    if PRINT_STEPS == True:
        print_tape(tape)

    if action.new_state == "halt" or action.new_state == "halt-accept" or action.new_state == "halt-reject":
        print(action.new_state)
        break
    else:
        current_state = mashine.get_state(mashine.get_state_index_by_name(action.new_state))
#print("Total Steps:", step)
