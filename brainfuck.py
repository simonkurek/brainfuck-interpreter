import sys
from typing import List

class FileContentHandler:

    def load(self):

        try:
            filename = sys.argv[1]
            file = open(filename, 'r')
        except FileNotFoundError:
            print("\nError: Invalid filename")
            print("Please check filename and try again.\n")
            exit(1)
        except IndexError:
            print("\nError: Filename not given.")
            print("Please try: python3 brainfuck.py [filename]\n")
            exit(1)

        self.code = []

        for line in file:
            for char in line:
                self.code.append(char)


class Interpreter:

    def __init__(self, code: List[str]):
        self.code = code
        self.instructions_len = len(self.code)
        self.pointer = 0
        self.memory = [0]
        self.actual_line = 1
        self.instruction_pointer = 0
        self.loop_start_index_stack = []
        self.loop_end_index = 0
        self.instruction_map = {
            '+':self.increment,
            '-':self.decrement,
            '>':self.pointer_right,
            '<':self.pointer_left,
            '\n':self.next_line,
            '.':self.display,
            ',':self.get_char,
            '[':self.loop_start,
            ']':self.loop_end,
        }
        if len(self.code) > 0: self.executor()

    def executor(self):
        while self.instructions_len > self.instruction_pointer:
            self.load_next_instruction()
        #print('\n')

    def load_next_instruction(self):
        print(f'Instruction number: {self.instruction_pointer}') #loop checker
        print(self.memory)
        instruction = self.code[self.instruction_pointer]
        if instruction in self.instruction_map:
            self.instruction_map[instruction]()
        self.instruction_pointer += 1

    def loop_start(self):
        self.loop_start_index_stack.append(self.instruction_pointer)
        if self.memory[self.pointer] == 0:
            #jump to ]
            if self.loop_end_index == 0:
                while self.code[self.instruction_pointer] != ']':
                    self.instruction_pointer += 1
                self.loop_end_index = self.instruction_pointer
            else:
                self.instruction_pointer = self.loop_end_index            

    def loop_end(self):
        self.loop_end_index = self.instruction_pointer
        if self.memory[self.pointer] != 0:
            self.instruction_pointer = self.loop_start_index_stack[-1]
        else:
            self.loop_end_index = 0
            self.loop_start_index_stack.pop()
        
    def increment(self):
        self.memory[self.pointer] += 1

    def decrement(self):
        self.memory[self.pointer] -= 1

    def pointer_right(self):
        if len(self.memory)-1 == self.pointer:
            self.memory.append(0)
        self.pointer += 1

    def pointer_left(self):
        self.pointer -= 1

    def next_line(self):
        self.actual_line += 1

    def display(self):
        #print(self.memory[self.pointer])
        print(chr(self.memory[self.pointer]), end="")

    def get_char(self):
        char = input()
        x = ord(char)
        self.memory[self.pointer] = x

if __name__ == '__main__':
    fch = FileContentHandler()
    fch.load()
    # temp debug mode
    #print(fch.code[90:96])
    interpreter = Interpreter(fch.code)
    print(interpreter.memory)


# TODO
# int range 0-255!!!!!!

# DONE
#interpreter locker nested loops mechanism

#future todo

# handle all exceptions
# dubug mode:
#  - step by step memory dump (pointer position, memory dump, instruction pointer,)

# all functions
# reading code from file
# instrucion couter
# memory dump (manualy)
# actual line (debug)
# instruction pointer (what interpreter is doing in any moment)
# dynamic memory usage 