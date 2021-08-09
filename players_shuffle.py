from tkinter import Label, Button, Listbox, Tk, Frame, Entry, ANCHOR, END, RIGHT, LEFT
from random import shuffle

root = Tk()
root.title("Shuffle Teams")

lb1 = Label(root, text="Shuffle Teams")
lb1.pack(pady=10)

lb2 = Label(root, text="Add Players: ")
lb2.pack()

# List of players to be added
players_list = []


def add():
    add_pl = ent_players.get()  # Get Player Name
    lbox1.insert(END, (add_pl))  # Insert Player in the Listbox
    players_list.append(add_pl)  # Add Player to the List
    ent_players.delete(0, END)  # Clean the Entry
    # print(players_list) --> DEBUG List


def delete_player():
    if lbox1.curselection():  # If Player is Selected from Listbox1
        get_curse_t1 = lbox1.get(ANCHOR)  # Get Player Name to Listbox1
        lbox1.delete(ANCHOR)  # Delete Player from the Listbox1
        players_list.remove(get_curse_t1)  # Delete Player from the List
    if lbox2.curselection():  # If Player is Selected from Listbox2
        get_curse_t2 = lbox2.get(ANCHOR)  # Get Player Name to Listbox2
        lbox2.delete(ANCHOR)  # Delete Player from the Listbox2
        players_list.remove(get_curse_t2)  # Delete Player from the List


def shuffle_team():
    list_shuffle = shuffle(players_list)  # Shuffle the list
    lbox1.delete(0, 'end')  # Clean the listbox1
    lbox2.delete(0, 'end')  # Clean the listbox2
    cant = len(players_list)  # Count the players
    half = cant // 2  # Split in 2

    # Insert half of the shuffled players into the listbox1
    for i in players_list[0:half]:
        lbox1.insert(END, (i))
    # Insert half of the shuffled players into the listbox2
    for i in players_list[half:]:
        lbox2.insert(END, (i))


# Entry and Button ADD PLAYERS
frame0 = Frame(root)
frame0.pack()
ent_players = Entry(frame0)
ent_players.pack()
bt_add = Button(frame0, text="Add", command=add, padx=50)
bt_add.pack(pady=3)

# Label TEAM 1 and TEAM 2
frame1 = Frame(root)
frame1.pack(pady=5)
lb_t1 = Label(frame1, text="Team 1")
lb_t1.pack(side=LEFT, padx=35)
lb_t2 = Label(frame1, text="Team 2")
lb_t2.pack(side=RIGHT, padx=35)

# ListBox
frame2 = Frame(root)
frame2.pack()
lbox1 = Listbox(frame2)
lbox1.pack(side=LEFT)
lbox2 = Listbox(frame2)
lbox2.pack(side=RIGHT)

# Buttons
bt2 = Button(root, text="Shuffle Teams", command=shuffle_team)
bt2.pack(side=LEFT, padx=20, pady=5)
bt3 = Button(root, text="Delete player", command=delete_player)
bt3.pack(side=RIGHT, padx=20, pady=5)

root.mainloop()

# Gaston Paez
# https://github.com/GastonPaez
# paez.gastonm@gmail.com
