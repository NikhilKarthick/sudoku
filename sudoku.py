import random
import tkinter as tk
from tkinter import END, Button, Entry, font


global_state = {}

SELECTED_COLOR = "skyblue"
BACKGROUND = "background"
BACKGROUND_COLOR = "#26242f"
SELECTED_CELL = "selected_cell"


def get_contents():
    rows = []

    for row in entryVars:
        cells = []
        for cell in row:
            if cell.get():
                cells.append(int(cell.get()))
            else:
                cells.append(0)
        rows.append(cells)

    return rows


def on_solve_game(e):

    input = get_contents()
    solved_output = solve(input)

    for r in range(9):
        for c in range(9):
            all_entries[r][c]["state"] = "normal"
            all_entries[r][c].delete(0, END)
            all_entries[r][c].insert(0, str(solved_output[r][c]))
            all_entries[r][c]["state"] = "disabled"

    global_state = {SELECTED_CELL: None}


def on_new_game(e):

    input = generate_input()

    for r, row in enumerate(entryVars):
        for (c, cell) in enumerate(row):
            all_entries[r][c][
                "state"
            ] = "normal"  # This cell could have been disabled in the previous game. So, enable it.
            if input[r][c] != 0:
                cell.set(str(input[r][c]))
                all_entries[r][c][
                    "state"
                ] = "disabled"  # Disabled disabled the user from editing
            else:
                cell.set("")

    global_state = {SELECTED_CELL: None}


def is_solved(output):

    for r in range(9):
        rowNums = {output[r][c] for c in range(9) if output[r][c]}
        if len(rowNums) < 9:
            return False

    for c in range(9):
        colNums = {output[r][c] for r in range(9) if output[r][c]}
        if len(colNums) < 9:
            return False

    boxNums = set()

    for r in range(3):
        for c in range(3):
            if output[r][c] != 0:
                boxNums = set()

                for br in range(r * 3, (r + 1) * 3):
                    for bc in range(c * 3, (c + 1) * 3):
                        if output[br][bc]:
                            boxNums.add(output[br][bc])

                if len(boxNums) < 9:
                    return False

    return True


def on_focus_in(e):
    bgcolor = e.widget[BACKGROUND]

    if bgcolor != "red":
        e.widget.configure({BACKGROUND: SELECTED_COLOR})

    global_state[SELECTED_CELL] = e.widget
    global_state["selectedCellPos"] = e.widget._name


def on_focus_out(e):

    bgcolor = e.widget[BACKGROUND]
    if bgcolor != "red":
        e.widget.configure({BACKGROUND: BACKGROUND_COLOR})

    if global_state[SELECTED_CELL]:
        [r, c] = map(int, e.widget._name.split())

        if entryVars[r][c].get() == "":
            e.widget.configure({BACKGROUND: BACKGROUND_COLOR})
            return

        if not is_valid(r, c, int(entryVars[r][c].get())):
            e.widget.configure({BACKGROUND: "red"})
        else:
            e.widget.configure({BACKGROUND: BACKGROUND_COLOR})

        output = get_contents()
        if is_solved(output):
            message_label["foreground"] = "green"
            print("Congratulations, You solved it!")


def on_key_press(e):

    if e.char != "" or e.keysym != "Tab":
        e.widget.delete(0, END)

    v = e.char
    try:
        v = int(v)
        if v == 0:
            return "break"
    except ValueError:
        if v != "\x08" and v != "":
            return "break"


def is_valid(r, c, num):
    dict = {i: False for i in range(9)}

    for r1, row in enumerate(entryVars):
        if r1 != r:
            continue

        for cell in row:
            if cell.get():
                num = int(cell.get())
                if num in dict and dict[num]:
                    return False

                dict[int(cell.get())] = True

    dict = {i: False for i in range(9)}

    for row in entryVars:
        cell = row[c]
        if cell.get():
            num = int(cell.get())
            if num in dict and dict[num]:
                return False

            dict[int(cell.get())] = True

    boxr = r // 3
    boxc = c // 3

    dict = {i: False for i in range(9)}

    for br in range(boxr * 3, (boxr + 1) * 3):
        for bc in range(boxc * 3, (boxc + 1) * 3):
            cell = entryVars[br][bc]
            if cell.get():
                num = int(cell.get())
                if num in dict and dict[num]:
                    return False

                dict[int(cell.get())] = True

    return True


def on_click(e):
    button: Button = e.widget

    if global_state[SELECTED_CELL]:
        [r, c] = map(int, global_state["selectedCellPos"].split())
        global_state[SELECTED_CELL].delete(0, END)
        global_state[SELECTED_CELL].insert(0, button["text"])
        if not is_valid(r, c, int(button["text"])):
            global_state[SELECTED_CELL].configure({BACKGROUND: "red"})
        else:
            global_state[SELECTED_CELL].configure({BACKGROUND: SELECTED_COLOR})

        output = get_contents()
        if is_solved(output):
            message_label["foreground"] = "green"
            print("Congratulations, You solved it!")


def on_erase(e):
    button: Button = e.widget

    if global_state[SELECTED_CELL]:
        global_state[SELECTED_CELL].delete(0, END)
        global_state[SELECTED_CELL].configure({BACKGROUND: SELECTED_COLOR})


window = tk.Tk()

window.title("Sudoku")

all_nums = [x for x in range(1, 10)]
all_nums_set = set(all_nums)


def is_solved(output):

    for r in range(9):
        rowNums = {output[r][c] for c in range(9) if output[r][c]}
        if len(rowNums) < 9:
            return False

    for c in range(9):
        colNums = {output[r][c] for r in range(9) if output[r][c]}
        if len(colNums) < 9:
            return False

    return True


def solve(input):

    output = [[cell for cell in row] for row in input]

    for r in range(9):

        row_nums = {output[r][c] for c in range(9) if output[r][c] != 0}

        if len(row_nums) == 9:
            continue

        for c in range(9):

            if output[r][c] == 0:

                col_nums = {output[r][c] for r in range(9) if output[r][c] != 0}
                boxr = r // 3
                boxc = c // 3

                box_nums = set()

                for br in range(boxr * 3, (boxr + 1) * 3):
                    for bc in range(boxc * 3, (boxc + 1) * 3):
                        if output[br][bc] != 0:
                            box_nums.add(output[br][bc])

                filledNums = row_nums | col_nums | box_nums
                potentialNums = all_nums_set - filledNums

                if len(potentialNums) == 0:
                    return None

                elif len(potentialNums) > 0:
                    for num in potentialNums:
                        input_copy = [[cell for cell in row] for row in output]
                        input_copy[r][c] = num
                        output_copy = solve(input_copy)
                        if output_copy != None:
                            return output_copy

                    return None
                else:
                    return None

    return output if is_solved(output) else None


def generate_input():

    middle_input = generate_middle_input()

    solved_input = solve(middle_input)

    input = remove_some_numbers_from_random_positions(solved_input)

    return input


def generate_middle_input():

    input = [[0 for _ in range(9)] for _ in range(9)]

    def fill_middle_table():

        nums = []

        r = 3

        while r < 6:

            c = 3

            while c < 6:

                if len(nums) < 9:
                    num = random.choice(all_nums)
                    if num not in nums:
                        nums.append(num)
                        input[r][c] = num
                        c += 1

            r += 1

        return nums

    def fill_middle_row():
        nums = [input[4][x] for x in range(3, 6)]

        c = 0
        while c < 9:
            num = random.choice(all_nums)
            if num not in nums:
                nums.append(num)
                input[4][c] = num
                c += 1
                if c == 3:
                    c = 6

        return num

    def fill_middle_column():
        nums = [input[x][4] for x in range(3, 6)]

        c = 0
        while c < 9:
            num = random.choice(all_nums)
            if num not in nums:
                nums.append(num)
                input[c][4] = num
                c += 1
                if c == 3:
                    c = 6

        return num

    fill_middle_table()
    fill_middle_row()
    fill_middle_column()

    return input


def remove_some_numbers_from_random_positions(solved_input):
    count_dict = {(r, c): 5 for r in range(3) for c in range(3)}

    row_dict = {r: 5 for r in range(9)}
    col_dict = {c: 5 for c in range(9)}

    cell_indices = [x for x in range(81)]

    while len(row_dict) > 0 and len(col_dict) > 0 and len(cell_indices) > 0:
        index = random.choice(cell_indices)

        row = index // 9
        col = index % 9

        tr = row // 3
        tc = col // 3

        cell_indices.remove(index)

        if (tr, tc) in count_dict and row in row_dict and col in col_dict:
            solved_input[row][col] = 0

            if count_dict[(tr, tc)] == 1:
                del count_dict[(tr, tc)]
            else:
                count_dict[(tr, tc)] -= 1

            if row_dict[row] == 1:
                del row_dict[row]
            else:
                row_dict[row] -= 1

            if col_dict[col] == 1:
                del col_dict[col]
            else:
                col_dict[col] -= 1

    return solved_input


input = generate_input()

entryVars = [
    [tk.StringVar(value="" if cell == 0 else str(cell)) for cell in row]
    for row in input
]


sudoku_table_frame = tk.Frame(
    master=window,
    relief=tk.RIDGE,
    borderwidth=0,
    padx=25,
    pady=25,
)

sudoku_table_frame.grid(row=0, column=0)

sudoku_actions_frame = tk.Frame(
    master=window,
    relief=tk.RIDGE,
    borderwidth=0,
    padx=25,
    pady=25,
)

sudoku_actions_frame.grid(row=0, column=1)


all_entries = [[None for _ in range(9)] for _ in range(9)]


def populate_entries():
    for i in range(3):
        for j in range(3):
            frame = tk.Frame(
                master=sudoku_table_frame,
                relief=tk.RIDGE,
                borderwidth=0,
                padx=2,
                pady=2,
            )
            frame.grid(row=i, column=j, padx=1, pady=1)

            for r in range(3):
                for c in range(3):
                    child = tk.Frame(
                        master=frame,
                        relief=tk.RIDGE,
                        borderwidth=0,
                        padx=None,
                        pady=None,
                        border=1,
                    )
                    child.grid(row=r, column=c, padx=0.3, pady=0.3)

                    entry = tk.Entry(
                        master=child,
                        textvariable=entryVars[i * 3 + r][j * 3 + c],
                        name=f"{i * 3 + r} {j * 3 + c}",
                        foreground="yellow"
                        if input[i * 3 + r][j * 3 + c] != 0
                        else "yellow",
                        background=BACKGROUND_COLOR,
                        font=font.Font(weight="bold"),
                        width=3,
                        borderwidth=None,
                        relief=tk.SUNKEN,
                        state="disabled"
                        if input[i * 3 + r][j * 3 + c] != 0
                        else "normal",
                    )

                    entry.bind("<FocusIn>", func=on_focus_in)
                    entry.bind("<FocusOut>", func=on_focus_out)
                    entry.bind("<KeyPress>", func=on_key_press)

                    all_entries[i * 3 + r][j * 3 + c] = entry

                    entry.pack(padx=0, pady=0)


populate_entries()


def populate_actions_frame():
    button_actions_frame = tk.Frame(
        master=sudoku_actions_frame,
        relief=tk.RIDGE,
        borderwidth=0,
        padx=25,
        pady=25,
    )

    button_actions_frame.grid(row=0, column=0)

    button_actions_container = tk.Frame(
        master=button_actions_frame,
        relief=tk.RIDGE,
        borderwidth=0,
        padx=25,
        pady=25,
    )

    button_actions_container.grid(row=0, column=0, columnspan=3)

    button = tk.Button(master=button_actions_container, text="Erase")
    button.grid(row=0, column=0)
    button.bind("<Button-1>", on_erase)

    button = tk.Button(master=button_actions_frame, text="1")
    button.grid(row=1, column=0)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="2")
    button.grid(row=1, column=1)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="3")
    button.grid(row=1, column=2)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="4")
    button.grid(row=2, column=0)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="5")
    button.grid(row=2, column=1)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="6")
    button.grid(row=2, column=2)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="7")
    button.grid(row=3, column=0)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="8")
    button.grid(row=3, column=1)
    button.bind("<Button-1>", on_click)

    button = tk.Button(master=button_actions_frame, text="9")
    button.grid(row=3, column=2)
    button.bind("<Button-1>", on_click)

    new_game_button = tk.Button(master=button_actions_frame, text="New Game")
    new_game_button.grid(row=4, column=0, columnspan=3, pady=25)
    new_game_button.bind("<Button-1>", on_new_game)

    solve_game_button = tk.Button(master=button_actions_frame, text="Solve the board")
    solve_game_button.grid(row=5, column=0, columnspan=3, pady=25)
    solve_game_button.bind("<Button-1>", on_solve_game)


populate_actions_frame()


def add_message_frame():
    message_frame = tk.Frame(
        master=window,
        relief=tk.RIDGE,
        borderwidth=0,
        padx=25,
        pady=25,
    )
    message_frame.grid(row=2, column=0, columnspan=2)

    message_label = tk.Label(
        text="Congratulations, You have solved the sudoku!",
        master=message_frame,
        foreground=window[BACKGROUND],
        font=font.Font(size=20),
    )
    message_label.pack()

    return message_label


message_label = add_message_frame()


window.mainloop()