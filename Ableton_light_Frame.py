import os
import time
import tkinter as tk
from tkinter import messagebox, ttk
from mido import Message, MidiFile, MidiTrack, MetaMessage

#
BG_COLOR = "#343541"
BTN_COLOR = "#2D3241"
FOCUS_COLOR = "#B0C4DE"
BTN_L_COLOR = "#60616F"
DLG_COLOR = "#40414F"
MIDIPATH = "D:\live\my project\galactic warzone\灯光"

root = tk.Tk()
root.configure(bg=BG_COLOR)
BPM = 174
INITIALIZING = False
frequent_color = {}

class Color:
    def __init__(self, vel, name, hex_value):
        self.vel = vel
        self.name = name
        self.hex = hex_value


class FunctionExecution:
    def __init__(self):
        self.stored_function = None

    def execute_and_store(self, func, *args, **kwargs):
        result = func(*args, **kwargs)
        self.stored_function = (func, args, kwargs)
        return result

    def re_execute(self):
        if self.stored_function:
            func, args, kwargs = self.stored_function
            func(*args, **kwargs)
        else:
            print("No function to execute.")


colors = [
    Color(0, "Black", "#000000"),
    Color(121, "Dark Red 7", "#340100"),
    Color(1, "Dark Gray", "#1c1c1c"),
    Color(6, "Dark Red 2", "#5a0000"),
    Color(71, "Dark Gray 2", "#202020"),
    Color(120, "Dark Red 6", "#a20401"),
    Color(106, "Red", "#ac0401"),
    Color(117, "Dark Purple 3", "#404040"),
    Color(118, "Dark Gray 3", "#747474"),
    Color(2, "Gray", "#7c7c7c"),
    Color(70, "Gray 2", "#7c7c7c"),
    Color(3, "Light Gray", "#fcfcfc"),
    Color(127, "Dark Brown 6", "#4c1300"),
    Color(10, "Dark Orange", "#5a1d00"),
    Color(105, "Dark Brown 4", "#6a3c18"),
    Color(61, "Dark Vermilion", "#9a3500"),
    Color(5, "Dark Red", "#fe0a00"),
    Color(72, "Bright Red 2", "#ff0a00"),
    Color(60, "Vermilion", "#ff1901"),
    Color(108, "Dark Orange 4", "#dc6900"),
    Color(84, "Bright Orange", "#ff4a01"),
    Color(9, "Orange", "#ff5700"),
    Color(107, "Bright Red 4", "#e15136"),
    Color(4, "Deep Red", "#ff4e48"),
    Color(11, "Dark Orange 2", "#241802"),
    Color(83, "Dark Brown 3", "#412000"),
    Color(100, "Dark Orange 3", "#3a2802"),
    Color(125, "Dark Brown 5", "#3c3000"),
    Color(62, "Brown", "#7a5101"),
    Color(99, "Golden Yellow", "#815d00"),
    Color(126, "Dark Orange 5", "#b45d00"),
    Color(97, "Dark Yellow 3", "#b8b100"),
    Color(124, "Dark Yellow 4", "#b8b100"),
    Color(96, "Bright Orange 2", "#ff7d01"),
    Color(109, "Bright Yellow 3", "#fee100"),
    Color(8, "Pale Orange", "#ffbc63"),
    Color(15, "Dark Yellow 2", "#181800"),
    Color(63, "Dark Brown", "#3e6500"),
    Color(14, "Dark Yellow", "#585800"),
    Color(111, "Bright Green 7", "#60b500"),
    Color(85, "Lime Yellow", "#82e100"),
    Color(110, "Bright Yellow 4", "#99e101"),
    Color(98, "Bright Yellow 2", "#8afd00"),
    Color(74, "Bright Yellow", "#acec00"),
    Color(73, "Pale Yellow", "#bafd00"),
    Color(13, "Yellow 2", "#fdfd00"),
    Color(12, "Yellow", "#fdfd21"),
    Color(113, "Pale Yellow 2", "#dcfd54"),
    Color(23, "Dark Green 4", "#001800"),
    Color(64, "Dark Brown 2", "#013800"),
    Color(19, "Dark Green 2", "#132801"),
    Color(101, "Dark Green 10", "#0d4c05"),
    Color(18, "Dark Green", "#165800"),
    Color(21, "Bright Green", "#00fe00"),
    Color(25, "Bright Green 2", "#00fe00"),
    Color(17, "Green", "#40fd01"),
    Color(75, "Lime Green", "#56fd00"),
    Color(20, "Light Green 2", "#35fd2b"),
    Color(86, "Lime Green 2", "#66fd00"),
    Color(16, "Light Green", "#81fd2b"),
    Color(27, "Dark Green 6", "#001800"),
    Color(123, "Dark Green 13", "#004101"),
    Color(22, "Dark Green 3", "#005801"),
    Color(26, "Dark Green 5", "#005801"),
    Color(30, "Dark Green 7", "#015814"),
    Color(76, "Dark Green 9", "#008800"),
    Color(122, "Bright Green 8", "#00d201"),
    Color(87, "Bright Green 5", "#00fe00"),
    Color(88, "Bright Green 6", "#00fe00"),
    Color(29, "Green 2", "#00fd3a"),
    Color(24, "Pale Green", "#35fc47"),
    Color(89, "Green 3", "#45fd61"),
    Color(35, "Dark Cyan 2", "#011810"),
    Color(31, "Dark Green 8", "#001c0e"),
    Color(65, "Dark Olive", "#005432"),
    Color(102, "Dark Green 11", "#005037"),
    Color(34, "Dark Cyan", "#015732"),
    Color(77, "Bright Green 4", "#01fc7b"),
    Color(33, "Bright Cyan", "#00fb91"),
    Color(28, "Bright Green 3", "#32fd7f"),
    Color(90, "Bright Teal 2", "#01fbcb"),
    Color(32, "Turquoise", "#2ffcb1"),
    Color(114, "Pale Cyan", "#76fbb9"),
    Color(119, "Pale Cyan 2", "#defcfc"),
    Color(39, "Dark Blue 2", "#001018"),
    Color(42, "Dark Blue 3", "#011a5a"),
    Color(68, "Teal", "#01444d"),
    Color(38, "Dark Blue", "#014051"),
    Color(66, "Bright Teal", "#00537f"),
    Color(92, "Dark Blue 7", "#274dc8"),
    Color(41, "Bright Blue 2", "#0050ff"),
    Color(37, "Bright Blue", "#00a7ff"),
    Color(78, "Bright Cyan 2", "#00a7ff"),
    Color(40, "Light Blue", "#4186ff"),
    Color(91, "Bright Blue 6", "#5086ff"),
    Color(36, "Sky Blue", "#39beff"),
    Color(47, "Dark Blue 6", "#000018"),
    Color(43, "Dark Blue 4", "#010619"),
    Color(103, "Dark Green 12", "#131429"),
    Color(46, "Dark Blue 5", "#00005a"),
    Color(112, "Dark Blue 8", "#1b1c31"),
    Color(104, "Bright Blue 7", "#101f5a"),
    Color(45, "Bright Blue 3", "#0000fe"),
    Color(67, "Dark Teal", "#0000fe"),
    Color(79, "Blue 3", "#021aff"),
    Color(44, "Royal Blue", "#4747ff"),
    Color(93, "Light Purple", "#847aed"),
    Color(115, "Pale Blue", "#9698ff"),
    Color(55, "Dark Magenta 2", "#180018"),
    Color(51, "Dark Purple 2", "#0a0032"),
    Color(50, "Dark Purple", "#160067"),
    Color(54, "Dark Magenta", "#5a005a"),
    Color(69, "Indigo", "#1a00d1"),
    Color(80, "Bright Blue 4", "#3500ff"),
    Color(49, "Purple", "#5000ff"),
    Color(81, "Bright Blue 5", "#7800ff"),
    Color(48, "Lavender", "#8347ff"),
    Color(94, "Bright Magenta", "#d30cff"),
    Color(116, "Bright Purple 2", "#8b62ff"),
    Color(53, "Magenta", "#ff00fe"),
    Color(0, "Black", "#000000"),
    Color(7, "Dark Red 3", "#180002"),
    Color(59, "Dark Red 5", "#210110"),
    Color(1, "Dark Gray", "#1c1c1c"),
    Color(58, "Dark Red 4", "#5a021b"),
    Color(82, "Bright Purple", "#b4177e"),
    Color(57, "Bright Red", "#ff0753"),
    Color(95, "Bright Red 3", "#ff065a"),
    Color(2, "Gray", "#7c7c7c"),
    Color(56, "Salmon Pink", "#fb4e83"),
    Color(52, "Pink", "#ff48fe"),
    Color(3, "Light Gray", "#fcfcfc"),
    Color(121, "Dark Red 7", "#340100"),
    Color(6, "Dark Red 2", "#5a0000"),
    Color(71, "Dark Gray 2", "#202020"),
    Color(120, "Dark Red 6", "#a20401"),
    Color(106, "Red", "#ac0401"),
    Color(117, "Dark Purple 3", "#404040"),
    Color(5, "Dark Red", "#fe0a00"),
    Color(72, "Bright Red 2", "#ff0a00"),
    Color(60, "Vermilion", "#ff1901"),
    Color(118, "Dark Gray 3", "#747474"),
    Color(70, "Gray 2", "#7c7c7c"),
    Color(4, "Deep Red", "#ff4e48")
]
now_template = ""
saved_texts = []
saved_palettes = []
saved_templates = []
original_output = [[]]
output = [[]]
transform_text = [[]]

execution = FunctionExecution()
# ----------AREA CLASSIFICATION------------


# region FRAME


main_area = tk.Frame(root)
main_area.configure(bg=BG_COLOR)
main_area.grid(row=0, column=0)

text_area = tk.Frame(main_area)
text_area.configure(bg=BG_COLOR)
text_area.grid(row=0, column=0)

control_area = tk.Frame(main_area)
control_area.configure(bg=BG_COLOR)
control_area.grid(row=1, column=0)

color_area = tk.Frame(root)
color_area.configure(bg=BG_COLOR)
color_area.grid(row=0, column=1)

button_area = tk.Frame(control_area)
button_area.configure(bg=BG_COLOR)
button_area.grid(row=0, column=0)

break_btn = tk.Frame(control_area, width=30, height=10)
break_btn.configure(bg=BG_COLOR)
break_btn.grid(row=0, column=1)

console_sum_area = tk.Frame(control_area)
console_sum_area.configure(bg=BG_COLOR)
console_sum_area.grid(row=0, column=2, sticky="n")

console_area = tk.Frame(console_sum_area)
console_area.configure(bg=BG_COLOR)
console_area.grid(row=0, column=0, sticky="n")

frame_area = tk.Frame(console_sum_area)
frame_area.configure(bg=BG_COLOR)
frame_area.grid(row=1, column=0, sticky="s")

check_area = tk.Frame(control_area)
check_area.configure(bg=BG_COLOR)
check_area.grid(row=0, column=3)

save_area = tk.Frame(control_area)
save_area.configure(bg=BG_COLOR)
save_area.grid(row=0, column=4)


# endregion


# ----------FUNCTION------------

# !!!!!!!!!!COMBINATION MODE!!!!!!!!!!!!
def get_vel_value(name):
    for color in colors:
        if color.name == name:
            return color.vel
    return None


def get_hex_value(vel):
    for color in colors:
        if color.vel == vel:
            return color.hex
    return None

def get_vel_by_hex(hex_value):
    for color in colors:
        if color.hex == hex_value:
            return color.vel
    return None

def transform_name_to_vel(colorlist):
    new_list = []
    for i in colorlist:
        print("trans", i)
        new_list.append(get_vel_value(i))
        print(new_list)
    return new_list


def initializing(ticks_per_beat=96):
    global mid
    global track

    mid = MidiFile(type=0, ticks_per_beat=ticks_per_beat)
    track = MidiTrack()

    mid.tracks.append(track)
    track.append(MetaMessage('track_name', name='', time=0))
    track.append(
        MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=36, notated_32nd_notes_per_beat=8,
                    time=0))


def trigger_on(Places=None, Color=None):
    for every_block in Places:
        track.append(Message('note_on', note=every_block, velocity=Color, time=0))


def trigger_off(Places=None, Interval=None, Color=None):
    TempInterval = Interval
    for every_block in Places:
        track.append(Message('note_off', note=every_block, velocity=Color, time=TempInterval))
        if TempInterval != 0:
            TempInterval = 0


def show_buttons_color(Places=None, Color=None):
    # print(Color)
    Color = get_hex_value(Color)
    # print(Color)
    for every_block in Places:
        # print(every_block)
        row, col = get_index(every_block)
        # print(every_block,row,col)
        # print(row,col)

        row, col = col, row
        # print(type(row),row,type(col),col)
        showcanvas.create_rectangle(row * grid_size, col * grid_size, row * grid_size + grid_size,
                                    col * grid_size + grid_size, fill=Color)


def hide_buttons_color(Places=None, Interval=None, Color=None):
    beat = 60 / BPM
    tick = beat / 96
    TempInterval = Interval * tick
    # print(TempInterval)
    for every_block in Places:
        row, col = get_index(every_block)

        row, col = col, row
        showcanvas.create_rectangle(row * grid_size, col * grid_size, row * grid_size + grid_size,
                                    col * grid_size + grid_size, fill=BTN_L_COLOR)
        time.sleep(TempInterval)
        if TempInterval != 0:
            TempInterval = 0


# some same length colorful line/only one color
def color_trigger(colorlist=None, triggerlist=None, Interval=None, Circulation=False, Show=False, wait=None):
    if type(colorlist) != list:
        colorlist = eval(colorlist)
    if type(triggerlist) != list:
        triggerlist = eval(triggerlist)
    colorlist = transform_name_to_vel(colorlist)
    Interval = int(Interval)
    total_num = len(colorlist) + len(triggerlist)
    # print(type(colorlist))
    # print(colorlist)
    # print(type(triggerlist))
    # print(triggerlist)
    if Circulation:
        while len(colorlist) < len(triggerlist):
            colorlist = colorlist + colorlist
    
    for both_sum in range(2, total_num + 1):
        TempInterval = Interval
        left_side = max(1, both_sum - len(colorlist))
        right_side = min(both_sum - 1, len(triggerlist))
        for Triggerlist_rank in range(left_side, right_side + 1):
            Colorlist_rank = both_sum - Triggerlist_rank
            blocks = triggerlist[Triggerlist_rank - 1]
            if Show:

                show_buttons_color(blocks, colorlist[Colorlist_rank - 1])
            else:
                trigger_on(blocks, colorlist[Colorlist_rank - 1])
        showcanvas.update()
        for Triggerlist_rank in range(left_side, right_side + 1):
            Colorlist_rank = both_sum - Triggerlist_rank
            blocks = triggerlist[Triggerlist_rank - 1]
            if Show:
                hide_buttons_color(blocks, TempInterval, colorlist[Colorlist_rank - 1])
            else:
                trigger_off(blocks, TempInterval, colorlist[Colorlist_rank - 1])
            if TempInterval != 0:
                TempInterval = 0
        showcanvas.update()


# some same length different area
def same_pace_color(colorlist=None, triggerlist=None, Interval=None, Circulation=False, Show=False, wait=None):
    if type(colorlist) != list:
        colorlist = eval(colorlist)
    if type(triggerlist) != list:
        triggerlist = eval(triggerlist)
    new_colorlist = []
    print(colorlist, "000")
    for i in colorlist:
        print(i)
        new_colorlist.append(transform_name_to_vel(i))
    print(new_colorlist, "NEW")
    colorlist = new_colorlist
    print(colorlist)
    Interval = int(Interval)
    for every_step in range(len(triggerlist[0])):
        TempInterval = Interval
        try:
            for every_area in range(len(colorlist)):
                trigger_on(triggerlist[every_area][every_step], colorlist[every_area][0])
        except:
            pass
        try:
            for every_area in range(len(colorlist)):
                trigger_off(triggerlist[every_area][every_step], TempInterval, colorlist[every_area][0])
                if TempInterval != 0:
                    TempInterval = 0
        except:
            pass


def footstep(colorlist=None, triggerlist=None, Interval=None, Circulation=False, Show=False, wait=None):
    full_trigger = []
    if type(colorlist) != list:
        colorlist = eval(colorlist)
    if type(triggerlist) != list:
        triggerlist = eval(triggerlist)
    colorlist = transform_name_to_vel(colorlist)
    Interval = int(Interval)
    total_num = len(colorlist) + len(triggerlist)
    # print(total_num)
    # print(colorlist,triggerlist)
    for both_sum in range(2, total_num + 1):
        TempInterval = Interval
        left_side = max(1, both_sum - len(colorlist))
        right_side = min(both_sum - 1, len(triggerlist))
        if both_sum > len(colorlist):
            # print(both_sum)
            # print(full_trigger)
            full_trigger = full_trigger + triggerlist[both_sum - len(colorlist) - 1]
            if Show:
                # print(full_trigger, colorlist)
                show_buttons_color(full_trigger, colorlist[-1])
            else:
                trigger_on(full_trigger, colorlist[-1])
        for Triggerlist_rank in range(left_side, right_side + 1):
            Colorlist_rank = both_sum - Triggerlist_rank
            blocks = triggerlist[Triggerlist_rank - 1]
            if Show:
                # print(blocks, colorlist)
                show_buttons_color(blocks, colorlist[Colorlist_rank - 1])
            else:
                trigger_on(blocks, colorlist[Colorlist_rank - 1])
        showcanvas.update()
        for Triggerlist_rank in range(left_side, right_side + 1):
            Colorlist_rank = both_sum - Triggerlist_rank
            blocks = triggerlist[Triggerlist_rank - 1]
            if Show:
                hide_buttons_color(blocks, TempInterval, colorlist[Colorlist_rank - 1])
            else:
                trigger_off(blocks, TempInterval, colorlist[Colorlist_rank - 1])
            if TempInterval != 0:
                TempInterval = 0
        showcanvas.update()
    # print(full_trigger)
    if Show:
        show_buttons_color(full_trigger, colorlist[-1])
    else:
        trigger_on(full_trigger, colorlist[-1])
    showcanvas.update()
    if wait is None or wait == "":
        wait = 0
    else:
        wait = int(wait)

    if Show:
        hide_buttons_color(full_trigger, wait, colorlist[-1])
    else:
        trigger_off(full_trigger, wait, colorlist[-1])
    showcanvas.update()


def frame_lights(framefile = None,intervalfile = None):
    for i in range(len(framefile)):
        everyframe = framefile[i]
        everyinterval = intervalfile[i]
        track.append(Message('note_on', note=0, velocity=0, time=0))
        if everyinterval == 0 :
            messagebox.showerror(f"invalid interval in Frame {i+1}")
            break
        if everyframe == {}:
            track.append(Message('note_off', note=0, velocity=0, time=0))
            continue
        for everyblock in everyframe:
            print(everyblock)
            hex_color = everyframe[everyblock][1]
            vel = int(get_vel_by_hex(hex_color))
            track.append(Message('note_on', note=int(everyblock), velocity=vel, time=0))
        track.append(Message('note_off', note=0, velocity=0, time=int(everyinterval)))
        for everyblock in everyframe:
            hex_color = everyframe[everyblock][1]
            vel = int(get_vel_by_hex(hex_color))
            track.append(Message('note_off', note=int(everyblock), velocity=vel, time=0))

def save_midi(name):
    mid.save(f"{MIDIPATH}\\{name}.mid")


# END!!!!!!!!!!COMBINATION MODE!!!!!!!!!!!!

# ===========BUTTON AREA===========


def update_output():
    input_text = input_entry.get()
    output_text.delete('1.0', 'end')
    original_output_text.delete('1.0', 'end')

    to_join = [f'[{",".join(map(str, x))}]' for x in output]
    output_text.insert('end', f'[{",".join(to_join)}]')
    to_join = [f'[{",".join(map(str, x))}]' for x in original_output]
    original_output_text.insert('end', f'[{",".join(to_join)}]')


Buttonname = ""


def on_button_click(button, text):
    if Framemode == True:
        global Buttonname
        global Nowbutton
        if Nowbutton != "":
            if Buttonname in Framefile[Nowframe - 1]:
                Nowbutton.configure(bg=Framefile[Nowframe - 1][Buttonname][1])
            else:
                Nowbutton.configure(bg=BTN_L_COLOR)
        Buttonname = text
        Nowbutton = button
        Nowbutton.configure(bg="white")
        print(text)
        return
    if text in output[-1]:
        original_output[-1].remove(str(int(text) - 35))
        output[-1].remove(text)

        button.config(bg=BTN_L_COLOR)
        # print(root.cget('bg'))
    else:
        original_output[-1].append(str(int(text) - 35))
        output[-1].append(text)
        button.config(bg="#006400")
    update_output()


def load_from_file():
    try:
        with open("template.txt", "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                text = lines[i + 1].strip()
                saved_texts.append((name, text))
                create_text_button(name)
    except FileNotFoundError:
        pass
    try:
        with open("palette.txt", "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                palette = lines[i + 1].strip()
                saved_palettes.append((name, palette))
                create_palette_button(name)
    except FileNotFoundError:
        pass
    try:
        with open(f"{MIDIPATH}\\templateorig.txt", "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                template = lines[i + 1].strip()
                saved_templates.append((name, template))
                create_template_button(name, place=len(saved_templates))
    except FileNotFoundError:
        pass


# END===========BUTTON AREA===========

# ===========DRAW AREA===========

Framebuttons = []
Frameintervals = []


def on_new_click():
    if Framemode == True:
        global Framecount
        global Framefile
        global Nowframe
        Framecount += 1
        Framefile.append({})
        Intervalfile.append(0)
        buttona = tk.Button(framesavearea, text=str(Framecount),
                            width=3, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR,
                            font=("Tahoma", 10))
        buttona.config(command=lambda button=buttona: on_frame_button_click(button))
        buttona.grid(row=0, column=Framecount, sticky="W")
        Framebuttons.append(buttona)
        buttonb = tk.Button(framesavearea, text=0,
                            width=3, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR,
                            font=("Tahoma", 10))
        buttonb.config(command=lambda button=buttonb,text = Framecount: on_frame_interval_click(button,text))
        buttonb.grid(row=1, column=Framecount, sticky="N")
        Frameintervals.append(buttonb)
        if Nowframe == "":
            Nowframe = 1
            Framebuttons[Nowframe - 1].configure(bg="white", fg=BTN_COLOR)
        return
    if inherit_var.get():
        output.append(output[-1][:])
    else:
        output.append([])
        for button in buttons:
            if button.cget('bg') == "#006400":
                button.config(bg="#32CD32")
            elif button.cget('bg') == "#32CD32":
                button.config(bg=BTN_L_COLOR)
    update_output()


def on_new_press(event):
    if event.name == 'n':
        on_new_click()
    if event.name == "a":
        on_color_add_click()


def on_reset_click():
    global output
    global original_output
    original_output = [[]]
    output = [[]]
    for button in buttons:
        button.config(bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    output_text.delete('1.0', 'end')
    original_output_text.delete('1.0', 'end')


def on_copy_click():
    root.clipboard_clear()
    root.clipboard_append(output_text.get('1.0', 'end-1c'))
    # messagebox.showinfo('Copied', 'Output copied to clipboard')


def on_save_click():
    text = input_entry.get()
    if text != "":
        name = text
    elif text == "":
        name = "Trigger " + str(len(saved_texts) + 1)
    text = output_text.get('1.0', 'end-1c')
    saved_texts.append((name, text))
    create_text_button(name)
    # messagebox.showinfo("Success", "Text saved successfully.")


def copy_text(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    # messagebox.showinfo('Copied', 'Output copied to clipboard')


def save_to_file():
    with open("template.txt", "w") as file:
        for saved_text in saved_texts:
            file.write(saved_text[0] + "\n")
            file.write(saved_text[1] + "\n")


def update_text_positions():
    for i, (saved_name, _) in enumerate(saved_texts):
        button = tk.Button(testsavearea, text=saved_name, command=lambda: copy_text(get_text_by_name(saved_name)),
                           width=10, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        button.grid(row=i, column=0)

        delete_button = tk.Button(testsavearea, text="Delete", command=lambda name=saved_name: delete_text(name),
                                  bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        delete_button.grid(row=i, column=1)


def delete_text(name):
    # 删除文本按钮和文本
    for i, (saved_name, _) in enumerate(saved_texts):
        if saved_name == name:
            saved_texts.pop(i)
            break
    for widget in testsavearea.winfo_children():
        widget.destroy()
    # 更新后续按钮的位置
    update_text_positions()


def create_text_button(name):
    # 创建文本按钮
    button = tk.Button(testsavearea, text=name, command=lambda: copy_text(get_text_by_name(name)),
                       width=9, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    button.grid(row=len(saved_texts), column=0)

    # 创建删除按钮
    delete_button = tk.Button(testsavearea, text="Delete", command=lambda: delete_text(name),
                              bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    delete_button.grid(row=len(saved_texts), column=1)


# END===========DRAW AREA===========

# ===========TRANSFORM AREA===========


def get_index(num):
    # print(num)
    if 1 + 35 <= num <= 32 + 35:
        row = 8 - (num - 35 - 1) // 4
        col = (num - 35 - 1) % 4 + 1
    elif 33 + 35 <= num <= 64 + 35:
        row = 8 - (num - 35 - 33) // 4
        col = (num - 35 - 33) % 4 + 4 + 1
    elif 65 + 35 <= num <= 72 + 35:
        row = num - 64 - 35
        col = 9
    elif 73 + 35 <= num <= 80 + 35:
        row = num - 72 - 35
        col = 0
    elif 81 + 35 <= num <= 88 + 35:
        row = 9
        col = num - 80 - 35
    elif -7 + 35 <= num <= 35:
        row = 0
        col = num + 8 - 35
    # print(row,col)
    return row, col


def get_num(row, col):
    if row == 0:
        return col - 8 + 35
    elif 1 <= row <= 8:
        if col == 0:
            return row + 72 + 35
        elif 1 <= col <= 4:
            return (8 - row) * 4 + col + 35
        elif 5 <= col <= 8:
            return ((8 - row) * 4 + col - 4) + 32 + 35
        elif col == 9:
            return row + 64 + 35
    elif row == 9:
        return col + 80 + 35


def transform(matrix, direction):
    result = []
    for every_row in matrix:
        new_row = []
        for num in every_row:
            i, j = get_index(num)
            if direction == 'cw':
                new_i, new_j = 9 - j, i
            elif direction == 'ccw':
                new_i, new_j = j, 9 - i
            elif direction == '180':
                new_i, new_j = 9 - i, 9 - j
                print(new_i, new_j)
            elif direction == 'flipy':
                new_i, new_j = 9 - i, j
            elif direction == 'flipx':
                new_i, new_j = i, 9 - j
            new_num = get_num(new_i, new_j)
            print(new_num)
            new_row.append(new_num)
        result.append(new_row)
    return result


def on_transform_click(direction):
    try:
        matrix = eval(transform_text.get('1.0', 'end-1c'))
        result = transform(matrix, direction)
        transform_text.delete("1.0", "end")
        transform_text.insert("end", str(result))
    except:
        messagebox.showerror('Error', 'Invalid input')


def on_reverse_click():
    try:
        matrix = eval(transform_text.get('1.0', 'end-1c'))
        result = matrix[::-1]
        transform_text.delete(0, tk.END)
        transform_text.insert(0, str(result))
    except:
        messagebox.showerror('Error', 'Invalid input')


# END===========TRANSFORM AREA===========

# ===========TEMPLATE AREA===========


def on_template_flow_click():
    global templatename
    global INITIALIZING
    name = flow_entry.get()
    interval = interval_entry.get()
    triggerlist = output_text.get("1.0", "end-1c")
    colorlist = color_text.get("1.0", "end-1c")
    if not INITIALIZING:
        INITIALIZING = True
        initializing()
    color_trigger(colorlist=colorlist, triggerlist=triggerlist, Interval=interval)
    if add_var.get():
        templatename.append(save_template("color_trigger"))
        print(templatename)
        return
    print(templatename)
    save_template("color_trigger")
    save_midi(name=name)
    INITIALIZING = False
    templatename = []


def on_template_bunch_click():
    global templatename
    global INITIALIZING
    name = flow_entry.get()
    interval = interval_entry.get()
    triggerlist = output_text.get("1.0", "end-1c")
    colorlist = color_text.get("1.0", "end-1c")
    if not INITIALIZING:
        INITIALIZING = True
        initializing()
    same_pace_color(colorlist=colorlist, triggerlist=triggerlist, Interval=interval)
    if add_var.get():
        templatename.append(save_template("color_trigger"))
        print(templatename)
        return
    save_template("same_pace_color")
    save_midi(name=name)
    INITIALIZING = False
    templatename = []


def on_template_snake_click():
    name = flow_entry.get()
    interval = interval_entry.get()
    triggerlist = output_text.get("1.0", "end-1c")
    colorlist = color_text.get("1.0", "end-1c")
    wait = wait_entry.get()
    initializing()
    footstep(colorlist=colorlist, triggerlist=triggerlist, Interval=interval, wait=wait)
    save_template("footstep")
    save_midi(name=name)


def on_template_show_click():
    # print(now_template)
    list_template = eval(now_template)
    for every_template in list_template:
        print(list_template)
        print(every_template)
        eval(every_template)


def save_frame_to_file():
    global templatename
    global INITIALIZING
    name = flow_entry.get()
    if not INITIALIZING:
        INITIALIZING = True
        initializing()
    frame_lights(framefile = Framefile,intervalfile = Intervalfile)
    if add_var.get():
        templatename.append(save_template("frame_lights"))
        print(templatename)
        return
    print(templatename)
    save_template("frame_lights")
    save_midi(name=name)
    INITIALIZING = False
    templatename = []
Framemode = False
Framefile = []
Framecount = 0
Nowbutton = ""
Nowframe = ""
Intervalfile = []

def on_template_frame_click():
    global Framemode
    global Framecount
    global Framefile
    global Nowbutton
    global Nowframe
    global Framebuttons
    if Framemode == True:
        save_frame_to_file()
        i = 0
        for k in range(8):
            for j in range(8):
                if j < 4:
                    text = str(k * 4 + j + 1)
                else:
                    text = str(32 + k * 4 + j - 4 + 1)
                buttons[i].configure(text=text)
                i += 1
        for button in buttons:
            button.configure(bg = BTN_L_COLOR)
        frame_button.configure(background=BTN_COLOR, fg="white")
        Framemode = False
        for widget in framesavearea.winfo_children():
            widget.destroy()
        return
    for i in range(64):
        buttons[i].configure(text="")
    for button in buttons:
        button.configure(bg=BTN_L_COLOR)
    frame_button.configure(background="white", fg=BTN_COLOR)
    Framemode = True
    Framecount = 0
    Framefile = []
    Nowbutton = ""
    Nowframe = ""
    Intervalfile = []
    Framebuttons = []
    labela = tk.Label(framesavearea, text="Interval:",
                      width=8, height=1, bg=DLG_COLOR, fg="white", activebackground=FOCUS_COLOR,
                      font=("Tahoma", 10))
    labela.grid(row=1, column=0, sticky="N")
    labelb = tk.Label(framesavearea, text="Frame:",
                      width=8, height=1, bg=DLG_COLOR, fg="white", activebackground=FOCUS_COLOR,
                      font=("Tahoma", 10))
    labelb.grid(row=0, column=0, sticky="N")
    on_new_click()


def on_frame_button_click(button):
    global Nowframe
    global Framebuttons
    global Nowbutton
    Framebuttons[Nowframe - 1].configure(bg=BTN_COLOR, fg="white")
    for livebutton in buttons:
        livebutton.config(bg=BTN_L_COLOR)
    Nowframe = int(button.cget("text"))
    Framebuttons[Nowframe - 1].configure(fg=BTN_COLOR, bg="white")
    print("Nowframe:", Nowframe)
    Nowbutton.configure(bg="white")
    if Framefile[Nowframe - 1] == {}:
        return
    for Buttonname in Framefile[Nowframe - 1]:
        Framefile[Nowframe - 1][Buttonname][0].configure(bg=Framefile[Nowframe - 1][Buttonname][1])


def on_frame_interval_click(button,text):
    global Intervalfile
    interval = interval_entry.get()
    Intervalfile[text-1] = interval
    if interval == "":
        return
    button.configure(text=interval)


def save_template(funcname):
    global templatename
    name = flow_entry.get()
    # print(name)
    interval = interval_entry.get()
    triggerlist = output_text.get("1.0", "end-1c")
    colorlist = color_text.get("1.0", "end-1c")
    text = f"{funcname}(colorlist={colorlist},triggerlist={triggerlist},Interval={interval},Show=True)"
    if add_var.get():
        return text
    if text:
        print(text)
        print(templatename, 1)
        print(type(templatename))
        templatename.append(text)
        text = templatename
        print("text", text, "template", templatename)
        for i, (saved_name, _) in enumerate(saved_templates):
            if saved_name == name:
                # 名字已存在，弹出对话框询问用户选择
                result = messagebox.askquestion("Name Conflict",
                                                "A template with the same name already exists. Do you want to overwrite it?")
                if result == "yes":
                    # 覆盖已存在的模板
                    saved_templates[i] = (name, str(text))
                    # 更新模板按钮
                    create_template_button(name, place=i + 1)
                    # messagebox.showinfo("Success", "Template overwritten successfully.")
                else:

                    # 取消保存
                    # messagebox.showinfo("Cancelled", "Template not saved.")
                    pass
                return

        # 名字不存在，保存新模板
        saved_templates.append((name, str(text)))
        create_template_button(name, place=len(saved_templates))
        # messagebox.showinfo("Success", "Template saved successfully.")


def create_template_button(name, place):
    # 创建模板按钮
    button = tk.Button(templatesavearea, text=name, command=lambda: save_text(get_template_by_name(name)),
                       width=9, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    button.grid(row=place, column=0)

    # 创建删除按钮
    delete_button = tk.Button(templatesavearea, text="Delete", command=lambda: delete_template(name),
                              bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    delete_button.grid(row=place, column=1)


def delete_template(name):
    # 删除按钮和文本
    for i, (saved_name, _) in enumerate(saved_templates):
        if saved_name == name:
            saved_templates.pop(i)
            break

    # 删除 MIDI 文件
    delete_midi(name)

    # 删除所有按钮
    for widget in templatesavearea.winfo_children():
        widget.destroy()

    # 重新创建按钮
    update_button_positions()


def delete_midi(name):
    # 删除对应的 MIDI 文件
    midi_file_path = f"{MIDIPATH}\\{name}.mid"
    if os.path.exists(midi_file_path):
        os.remove(midi_file_path)


def update_button_positions():
    # 更新后续按钮的位置

    for i, (saved_name, _) in enumerate(saved_templates):
        button = tk.Button(templatesavearea, text=saved_name,
                           command=lambda: save_text(get_template_by_name(saved_name)),
                           width=9, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        button.grid(row=i, column=0)

        delete_button = tk.Button(templatesavearea, text="Delete",
                                  command=lambda name=saved_name: delete_template(name),
                                  bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        delete_button.grid(row=i, column=1)


def save_text(text):
    global now_template
    now_template = text


def save_template_to_file():
    with open(f"{MIDIPATH}\\templateorig.txt", "w") as file:
        for saved_template in saved_templates:
            file.write(saved_template[0] + "\n")
            file.write(saved_template[1] + "\n")


# END===========TEMPLATE AREA===========

# ===========SAVE AREA===========


def get_text_by_name(name):
    for saved_text in saved_texts:
        if saved_text[0] == name:
            return saved_text[1]
    return ""


def get_palette_by_name(name):
    for saved_text in saved_palettes:
        if saved_text[0] == name:
            return saved_text[1]
    return ""


def get_template_by_name(name):
    for saved_text in saved_templates:
        if saved_text[0] == name:
            return saved_text[1]
    return ""


# END===========SAVE AREA===========

# ===========COLOR AREA===========


def on_color_add_click():
    try:
        frequent_color[current_color] += 1
    except:
        frequent_color[current_color] = 1
    refresh_frequent_color()
    if Framemode == True:
        global Buttonname
        global Nowbutton

        if Nowbutton == "":
            return
        colorvel = transform_name_to_vel([current_color])
        color = get_hex_value(colorvel[0])
        Nowbutton.configure(bg=color)
        Framefile[Nowframe - 1][Buttonname] = [Nowbutton, color]
        print(Buttonname)
        return
    colortext.append(current_color)
    color_text.delete("1.0", "end")
    color_text.insert("end", str(colortext))

def refresh_frequent_color():
    print(frequent_color)
    top_colors = sorted(frequent_color, key=frequent_color.get, reverse=True)[:12]

    for i, color_name in enumerate(top_colors):
        color = next((c for c in colors if c.name == color_name), None)
        if color:
            color_frame = tk.Frame(frequent_color_frame, bg=color.hex, width=square_size, height=square_size)
            color_frame.grid(row=0, column=i)
            color_frame.bind("<Button-1>", lambda event, c=color: show_color_name(c.name, c.vel))

def on_color_reset_click():
    global colortext
    colortext = []
    color_text.delete('1.0', 'end')


def on_color_save_click():
    text = input_entry.get()
    if text != "":
        name = text
    elif text == "":
        name = "Palette" + str(len(saved_palettes) + 1)
    text = color_text.get("1.0", "end-1c")
    saved_palettes.append((name, text))
    # print(saved_palettes)
    create_palette_button(name)
    # messagebox.showinfo("Success", "Text saved successfully.")


def create_palette_button(name):
    # 创建调色板按钮
    button = tk.Button(palettearea, text=name, command=lambda: copy_text(get_palette_by_name(name)),
                       width=9, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    button.grid(row=len(saved_palettes), column=0)

    # 创建删除按钮
    delete_button = tk.Button(palettearea, text="Delete", command=lambda: delete_palette(name),
                              bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
    delete_button.grid(row=len(saved_palettes), column=1)


def delete_palette(name):
    # 删除调色板按钮和文本
    for i, (saved_name, _) in enumerate(saved_palettes):
        if saved_name == name:
            saved_palettes.pop(i)
            break
    for widget in palettearea.winfo_children():
        widget.destroy()
    # 更新后续按钮的位置
    update_palette_positions()


def update_palette_positions():
    for i, (saved_name, _) in enumerate(saved_palettes):
        button = tk.Button(palettearea, text=saved_name, command=lambda: copy_text(get_palette_by_name(saved_name)),
                           width=9, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        button.grid(row=i, column=0)

        delete_button = tk.Button(palettearea, text="Delete", command=lambda name=saved_name: delete_palette(name),
                                  bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR, font=("Tahoma", 10))
        delete_button.grid(row=i, column=1)


def save_palette_to_file():
    with open("palette.txt", "w") as file:
        for saved_palette in saved_palettes:
            file.write(saved_palette[0] + "\n")
            file.write(saved_palette[1] + "\n")


# ===========COLOR AREA===========

# END----------FUNCTION------------

# ----------TEXT AREA------------


# region CREATE TEXT


input_label = tk.Label(text_area, text='Name:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
input_label.grid(row=0, column=0)
input_entry = tk.Entry(text_area, bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
input_entry.grid(row=0, column=1, columnspan=7)

original_output_label = tk.Label(text_area, text='Original Output:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
original_output_label.grid(row=1, column=0)
original_output_text = tk.Text(text_area, height=4, wrap='none', bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
original_output_text.grid(row=1, column=1, columnspan=7)
original_output_scrollbar_x = ttk.Scrollbar(text_area, orient='horizontal', command=original_output_text.xview,
                                           style="TScrollbar")
original_output_scrollbar_y = ttk.Scrollbar(text_area, orient='vertical', command=original_output_text.yview,
                                           style="TScrollbar")
original_output_text.config(xscrollcommand=original_output_scrollbar_x.set, yscrollcommand=original_output_scrollbar_y.set)
original_output_scrollbar_x.grid(row=2, column=1, columnspan=7, sticky='ew')
original_output_scrollbar_y.grid(row=1, column=8, sticky='ns')

output_label = tk.Label(text_area, text='Output:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
output_label.grid(row=3, column=0)
output_text = tk.Text(text_area, height=4, wrap='none', bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
output_text.grid(row=3, column=1, columnspan=7)
output_scrollbar_x = ttk.Scrollbar(text_area, orient='horizontal', command=output_text.xview, style="TScrollbar")
output_scrollbar_y = ttk.Scrollbar(text_area, orient='vertical', command=output_text.yview, style="TScrollbar")
output_text.config(xscrollcommand=output_scrollbar_x.set, yscrollcommand=output_scrollbar_y.set)
output_scrollbar_x.grid(row=4, column=1, columnspan=7, sticky='ew')
output_scrollbar_y.grid(row=3, column=8, sticky='ns')

transform_label = tk.Label(text_area, text='Transform:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
transform_label.grid(row=5, column=0)
transform_text = tk.Text(text_area, height=4, wrap='none', bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
transform_text.grid(row=5, column=1, columnspan=7)
transform_scrollbar_x = ttk.Scrollbar(text_area, orient='horizontal', command=transform_text.xview, style="TScrollbar")
transform_scrollbar_y = ttk.Scrollbar(text_area, orient='vertical', command=transform_text.yview, style="TScrollbar")
transform_text.config(xscrollcommand=transform_scrollbar_x.set, yscrollcommand=transform_scrollbar_y.set)
transform_scrollbar_x.grid(row=6, column=1, columnspan=7, sticky='ew')
transform_scrollbar_y.grid(row=5, column=8, sticky='ns')

# endregion


# END----------TEXT AREA------------

# ----------BUTTON AREA------------


buttons = []
for i in range(8):
    for j in range(8):
        if j < 4:
            text = str(i * 4 + j + 1)
        else:
            text = str(32 + i * 4 + j - 4 + 1)
        button = tk.Button(button_area, text=text, width=2, height=1, bg=BTN_L_COLOR, fg="white",
                           activebackground=DLG_COLOR, font=("Tahoma", 10))
        text = str(int(text) + 35)
        button.config(command=lambda button=button, text=text: on_button_click(button, text))
        button.grid(row=8 - i, column=1 + j, padx=2, pady=2)
        buttons.append(button)
for i in range(28, 36):
    text = str(i)
    button = tk.Button(button_area, width=2, height=1, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR,
                       font=("Tahoma", 10))
    button.config(command=lambda button=button, text=text: on_button_click(button, text))
    button.grid(row=0, column=i - 28 + 1)
    buttons.append(button)
for i in range(100, 108):
    text = str(i)
    button = tk.Button(button_area, width=2, height=1, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR,
                       font=("Tahoma", 10))
    button.config(command=lambda button=button, text=text: on_button_click(button, text))
    button.grid(row=i - 99, column=9)
    buttons.append(button)
for i in range(108, 116):
    text = str(i)
    button = tk.Button(button_area, width=2, height=1, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR,
                       font=("Tahoma", 10))
    button.config(command=lambda button=button, text=text: on_button_click(button, text))
    button.grid(row=i - 107, column=0)
    buttons.append(button)
for i in range(116, 124):
    text = str(i)
    button = tk.Button(button_area, width=2, height=1, bg=BTN_L_COLOR, fg="white", activebackground=DLG_COLOR,
                       font=("Tahoma", 10))
    button.config(command=lambda button=button, text=text: on_button_click(button, text))
    button.grid(row=9, column=i - 116 + 1)
    buttons.append(button)
# print(grid_buttons)


# END----------BUTTON AREA------------

# ----------CONSOLE AREA------------


# region CONSOLE FRAMES


drawarea = tk.Frame(console_area)
drawarea.configure(bg=BG_COLOR)
drawarea.grid(row=0, column=0, sticky="n")

transformarea = tk.Frame(console_area)
transformarea.configure(bg=BG_COLOR)
transformarea.grid(row=0, column=1, sticky="n")

templatearea = tk.Frame(console_area)
templatearea.configure(bg=BG_COLOR)
templatearea.grid(row=0, column=2, sticky="n")

# endregion


# ===========DRAW AREA===========


# region DRAW BUTTONS


new_button = tk.Button(drawarea, text='New', command=on_new_click,
                       width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
new_button.grid(row=1, column=0)

reset_button = tk.Button(drawarea, text='Reset', command=on_reset_click,
                         width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
reset_button.grid(row=2, column=0)

copy_button = tk.Button(drawarea, text='Copy', command=on_copy_click,
                        width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
copy_button.grid(row=3, column=0)

save_button = tk.Button(drawarea, text="Save", command=on_save_click,
                        width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
save_button.grid(row=4, column=0)

# endregion


# END===========DRAW AREA===========

# ===========TRANSFORM AREA===========


# region TRANSFORM BUTTON


clockwise_button = tk.Button(transformarea, text='CW', command=lambda: on_transform_click('cw'),
                             width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white",
                             font=("Tahoma", 10))
clockwise_button.grid(row=1, column=9)

counterclockwise_button = tk.Button(transformarea, text='CCW', command=lambda: on_transform_click('ccw'),
                                    width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white",
                                    font=("Tahoma", 10))
counterclockwise_button.grid(row=2, column=9)

one_eighty_button = tk.Button(transformarea, text='180', command=lambda: on_transform_click('180'),
                              width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white",
                              font=("Tahoma", 10))
one_eighty_button.grid(row=3, column=9)

reverse_button = tk.Button(transformarea, text='Reverse', command=on_reverse_click,
                           width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white", font=("Tahoma", 10))
reverse_button.grid(row=4, column=9)

flipy_button = tk.Button(transformarea, text='FlipY', command=lambda: on_transform_click('flipy'),
                         width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white", font=("Tahoma", 10))
flipy_button.grid(row=5, column=9)

flipx_button = tk.Button(transformarea, text='FlipX', command=lambda: on_transform_click('flipx'),
                         width=8, height=1, bg=BTN_COLOR, activebackground=FOCUS_COLOR, fg="white", font=("Tahoma", 10))
flipx_button.grid(row=6, column=9)

# endregion


# END===========TRANSFORM AREA===========

# ===========TEMPLATE AREA===========


# region TEMPLATE BUTTON


flow_label = tk.Label(templatearea, text='Name:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
flow_label.grid(row=0, column=1)
flow_entry = tk.Entry(templatearea, bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
flow_entry.grid(row=0, column=2, columnspan=1)

interval_label = tk.Label(templatearea, text='Interval:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
interval_label.grid(row=1, column=1)
interval_entry = tk.Entry(templatearea, bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
interval_entry.grid(row=1, column=2, columnspan=1)

slidearea = tk.Frame(templatearea, bg=BG_COLOR)
slidearea.grid(row=2, column=1, columnspan=2)


def update_tick(value):
    ticklabel.config(text=ticktext[int(value)])


ticktext = ["1/6", "1/4", "1/3", "1/2", "1", "2", "3", "4", "5", "6", "7", "8"]
tickslider = tk.Scale(slidearea, from_=0, to=11, orient=tk.HORIZONTAL, length=100, showvalue=False, command=update_tick,
                      background=BG_COLOR, borderwidth=0, highlightbackground=BG_COLOR, troughcolor=DLG_COLOR,
                      highlightcolor=FOCUS_COLOR,
                      activebackground=FOCUS_COLOR)
tickslider.grid(row=0, column=0)

ticklabel = tk.Label(slidearea, text="0", width=2, bg=BG_COLOR, fg="white", font=("Tahoma", 12))
ticklabel.grid(row=0, column=1)


def handle_input():
    # 获取下拉列表的值
    scale_value = ticklabel.cget("text")

    # 将刻度值映射为对应的倍数
    scale_mapping = {
        '1/6': 1 / 6,
        '1/4': 1 / 4,

        '1/3': 1 / 3,
        '1/2': 1 / 2,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8
    }
    scale_factor = scale_mapping[scale_value]

    # 计算输入值
    input_value = 48 * scale_factor
    input_value = int(input_value)
    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, str(input_value))


input_button = tk.Button(slidearea, text="Input", command=handle_input,
                         bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
input_button.grid(row=0, column=2, padx=20)

wait_label = tk.Label(templatearea, text='Wait:', bg=BG_COLOR, fg="white", font=("Tahoma", 12))
wait_label.grid(row=3, column=1)
wait_entry = tk.Entry(templatearea, bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
wait_entry.grid(row=3, column=2, columnspan=1)
templatename = []
flow_button = tk.Button(templatearea, text='Flow', command=on_template_flow_click,
                        width=8, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
flow_button.grid(row=0, column=0, sticky="N")

bunch_button = tk.Button(templatearea, text='Bunch', command=on_template_bunch_click,
                         width=8, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
bunch_button.grid(row=1, column=0, sticky="N")

snake_button = tk.Button(templatearea, text='Snake', command=on_template_snake_click,
                         width=8, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
snake_button.grid(row=2, column=0, sticky="N")

show_button = tk.Button(templatearea, text='Show', command=on_template_show_click,
                        width=8, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
show_button.grid(row=3, column=0, sticky="N")

frame_button = tk.Button(templatearea, text='Frame', command=on_template_frame_click,
                         width=8, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
frame_button.grid(row=4, column=0, sticky="N")

# endregion


# END===========TEMPLATE AREA===========

# END----------CONSOLE AREA------------

# ----------CHECK AREA------------


# region CHECK BUTTON


inherit_var = tk.BooleanVar()
inherit_checkbutton = tk.Checkbutton(check_area, text='Inherit', variable=inherit_var,
                                     selectcolor=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR,
                                     activebackground=BG_COLOR, activeforeground=FOCUS_COLOR, bg=BG_COLOR, fg="white",
                                     font=("Tahoma", 12))
inherit_checkbutton.grid(row=0, column=0)

add_var = tk.BooleanVar()
add_checkbutton = tk.Checkbutton(check_area, text='Add', variable=add_var,
                                 selectcolor=BG_COLOR, highlightbackground=BG_COLOR, highlightcolor=BG_COLOR,
                                 activebackground=BG_COLOR, activeforeground=FOCUS_COLOR, bg=BG_COLOR, fg="white",
                                 font=("Tahoma", 12))
add_checkbutton.grid(row=1, column=0)

# endregion


# END----------CHECK AREA------------

# ----------SAVE AREA------------


# region SAVE BUTTON


savearea_canvas = tk.Canvas(save_area, borderwidth=0, highlightthickness=0, bg=DLG_COLOR)

style = ttk.Style()
style.theme_use('default')
style.configure("TScrollbar",
                gripcount=0,
                background=FOCUS_COLOR,
                darkcolor=BG_COLOR,
                lightcolor=DLG_COLOR,
                troughcolor=DLG_COLOR,
                )

savearea_scrollbar = ttk.Scrollbar(save_area, orient='vertical', command=savearea_canvas.yview, style="TScrollbar")
savearea_canvas.configure(yscrollcommand=savearea_scrollbar.set)

savearea_scroll = tk.Frame(savearea_canvas, bg=DLG_COLOR)
savearea_scroll.bind('<Configure>', lambda e: savearea_canvas.configure(scrollregion=savearea_canvas.bbox('all')))

savearea_canvas.create_window((0, 0), window=savearea_scroll, anchor='nw')
savearea_canvas.configure(yscrollcommand=savearea_scrollbar.set)
savearea_canvas.pack(side='left', fill='both', expand=True)
savearea_scrollbar.pack(side='right', fill='y')

testsavearea = tk.Frame(savearea_scroll, bg=DLG_COLOR)
testsavearea.grid(row=0, column=0, sticky="n")

palettearea = tk.Frame(savearea_scroll, bg=DLG_COLOR)
palettearea.grid(row=0, column=1, sticky="n")

templatesavearea = tk.Frame(savearea_scroll, bg=DLG_COLOR)
templatesavearea.grid(row=0, column=2, sticky="n")

# endregion


# END----------SAVE AREA------------

# ----------FRAME AREA------------


# region FRAME AREA!!!

framearea_canvas = tk.Canvas(frame_area, borderwidth=0, highlightthickness=0, bg=DLG_COLOR)

style = ttk.Style()
style.theme_use('default')
style.configure("TScrollbar",
                gripcount=0,
                background=FOCUS_COLOR,
                darkcolor=BG_COLOR,
                lightcolor=DLG_COLOR,
                troughcolor=DLG_COLOR,
                )

framearea_scrollbar = ttk.Scrollbar(frame_area, orient='horizontal', command=framearea_canvas.xview, style="TScrollbar")
framearea_canvas.configure(xscrollcommand=framearea_scrollbar.set, height=100)

framearea_scroll = tk.Frame(framearea_canvas, bg=DLG_COLOR)
framearea_scroll.bind('<Configure>', lambda e: framearea_canvas.configure(scrollregion=framearea_canvas.bbox('all')))

framearea_canvas.create_window((0, 0), window=framearea_scroll, anchor='nw')
framearea_canvas.configure(xscrollcommand=framearea_scrollbar.set, height=100)
framearea_canvas.pack(side='top', fill='both', expand=True)
framearea_scrollbar.pack(side='bottom', fill='x')

framesavearea = tk.Frame(framearea_scroll, bg=DLG_COLOR)
framesavearea.grid(row=0, column=0, sticky="n")


# endregion


# END----------FRAME AREA------------

# ----------COLOR AREA------------


# region COLOR AREA!!!

available_width = 240  # Leave some margin
square_size = 20  # Adjust this value to change the size of the color squares
num_columns = max(1, available_width // square_size)

def show_color_name(color_name, vel_name):
    global current_color
    current_color = color_name
    global current_vel
    current_vel = vel_name
    color_name_label.config(text=f"Name:{color_name},Vel:{vel_name}", font=("Tahoma", 12))

frequent_color_frame = tk.Frame(color_area)
frequent_color_frame.configure(bg=BG_COLOR,height=square_size)
frequent_color_frame.grid(row=0, column=0, pady=2)


color_table_frame = tk.Frame(color_area)
color_table_frame.configure(bg=BG_COLOR)
color_table_frame.grid(row=1, column=0)


current_color = ""
for i, color in enumerate(colors):
    row = i // num_columns
    col = i % num_columns

    color_frame = tk.Frame(color_table_frame, bg=color.hex, width=square_size, height=square_size)
    color_frame.grid(row=row, column=col)
    color_frame.bind("<Button-1>", lambda event, c=color: show_color_name(c.name, c.vel))

color_name_label = tk.Label(color_area, text="", font=("Arial", 10), bg=BG_COLOR, fg="white")
show_color_name("", "")
color_name_label.grid(row=2, column=0)

color_add = tk.Button(color_area, text='Add', command=on_color_add_click,
                      width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
color_add.grid(row=3, column=0)

colortext = []
color_label = tk.Label(text_area, text="Color:", bg=BG_COLOR, fg="white", font=("Tahoma", 12))
color_label.grid(row=9, column=0)
color_text = tk.Text(text_area, height=4, wrap='none', bg=DLG_COLOR, fg="white", font=("Tahoma", 12))
color_text.grid(row=9, column=1)
color_scrollbar_x = ttk.Scrollbar(text_area, orient='horizontal', command=color_text.xview, style="TScrollbar")
color_text.config(xscrollcommand=color_scrollbar_x.set)
color_scrollbar_x.grid(row=10, column=1, columnspan=1, sticky='ew')

color_reset = tk.Button(color_area, text='Reset', command=on_color_reset_click,
                        width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
color_reset.grid(row=4, column=0)

save_button = tk.Button(color_area, text="Save", command=on_color_save_click,
                        width=5, height=1, bg=BTN_COLOR, fg="white", activebackground=FOCUS_COLOR, font=("Tahoma", 10))
save_button.grid(row=5, column=0)

showarea = tk.Frame(color_area)
showarea.configure(bg=BG_COLOR, borderwidth=0)
showarea.grid(row=6, column=0)
grid_size = 20
showcanvas = tk.Canvas(showarea, width=10 * grid_size, height=10 * grid_size, bg=BG_COLOR, borderwidth=0,
                       highlightbackground=BG_COLOR)
showcanvas.pack()

grid = [[showcanvas.create_rectangle(x, y, x + grid_size, y + grid_size, fill=BTN_L_COLOR) for i, x in
         enumerate(range(0, 10 * grid_size, grid_size))] for y in range(0, 10 * grid_size, grid_size)]

# endregion


# END----------COLOR AREA------------
j = 0
for button in buttons:
    j += 1
    print(j, ":")
    print(button.cget("text"))


if __name__ == '__main__':
    load_from_file()
    root.title("画灯")
    root.mainloop()
    save_to_file()
    save_palette_to_file()
    save_template_to_file()
    # keyboard.on_press(on_new_press)
    # keyboard.wait('esc')
