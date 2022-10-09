DATABASE = 'UserData.sqlite'


def restart():
    global close_notifier
    close_notifier = 1
    app.quit()
    app.destroy()
    os.system("Stalker.exe")
    sys.exit()


import os, sys
import threading
import tkinter
import customtkinter
import sqlite3

from tkinter import BOTTOM, DISABLED, font
from cv2 import COLOR_HLS2RGB_FULL
from UserStats import UserStats
from UserActivityNotifier import UserActivityNotifier

app = customtkinter.CTk()
check_codeforces = 1
check_codechef = 1

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS User_Handles (
    user_id INT,
    user_name TEXT,
    handle_codeforces TEXT,
    handle_codechef TEXT,
    PRIMARY KEY(handle_codeforces)
);''')
conn.commit()
cur.execute('SELECT * FROM User_Handles;')
data = cur.fetchall()
conn.close()
# print(data)
conn.close()


class Buttons:
    button_id = dict()
    details = []

    def __init__(self, data) -> None:
        pass

    def event_submit(self, top: customtkinter.CTk,
                     name: customtkinter.CTkEntry, cf: customtkinter.CTkEntry,
                     cc: customtkinter.CTkEntry):
        self.details = [name.get(), cf.get(), cc.get()]
        top.quit()
        top.destroy()

    def event_add(self, add_button):
        print('button event_add')
        user_id = int()
        for i in range(1, 13):
            if i not in self.button_id.values():
                user_id = i
                break

        top = customtkinter.CTkToplevel()
        top.title("User Entry")
        top.geometry("400x300")
        top.iconbitmap("logo.ico")
        name_entry = customtkinter.CTkEntry(master=top,
                                            placeholder_text="Name",
                                            width=250,
                                            height=30,
                                            border_width=2,
                                            corner_radius=4)
        name_entry.place(x=75, y=50)
        cf_entry = customtkinter.CTkEntry(
            master=top,
            placeholder_text="Codeforces Profile",
            width=250,
            height=30,
            border_width=2,
            corner_radius=4)
        cf_entry.place(x=75, y=95)
        cc_entry = customtkinter.CTkEntry(master=top,
                                          placeholder_text="Codechef Profile",
                                          width=250,
                                          height=30,
                                          border_width=2,
                                          corner_radius=4)
        cc_entry.place(x=75, y=140)

        submit = customtkinter.CTkButton(
            master=top,
            width=150,
            height=30,
            border_width=0,
            corner_radius=8,
            text="Submit",
            command=lambda: self.event_submit(top, name_entry, cf_entry,
                                              cc_entry),
            text_font=('@Batang', 13, 'bold'))
        submit.pack(padx=30, pady=30, side=BOTTOM)
        top.mainloop()

        try:
            name, cf, cc = self.details[0], self.details[1], self.details[2]
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('INSERT INTO User_Handles VALUES ( ?, ?, ?, ? );',
                        (user_id, name, cf, cc))
            conn.commit()
            conn.close()
        except:
            pass
        restart()

    def event_delete(self, del_button: customtkinter.CTkButton):
        print('button event_del')
        user_id = self.button_id[del_button]

        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('DELETE FROM User_Handles WHERE user_id = ? ;',
                        (user_id, ))
            conn.commit()
            conn.close()
        except:
            pass
        restart()

    def event_stats(self, name_button: customtkinter.CTkButton):
        data = self.button_id[name_button]
        stats = UserStats(data[1], data[2], data[3])

    def event_toggle_codeforces(self, toggle_cf: customtkinter.CTkButton):
        print('button toggle cf')
        global check_codeforces
        if check_codeforces == 1:
            check_codeforces = 0
            toggle_cf.configure(fg_color='#444C58',
                                text_font=('@Batang', 23),
                                text_color='grey')
        else:
            check_codeforces = 1
            toggle_cf.configure(fg_color='#217FF9',
                                text_font=('@Batang', 23, 'bold'),
                                text_color='white')

    def event_toggle_codechef(self, toggle_cc: customtkinter.CTkButton):
        print('button toggle cc')
        global check_codechef
        if check_codechef == 1:
            check_codechef = 0
            toggle_cc.configure(fg_color='#444C58',
                                text_font=('@Batang', 23),
                                text_color='grey')
        else:
            check_codechef = 1
            toggle_cc.configure(fg_color='#217FF9',
                                text_font=('@Batang', 23, 'bold'),
                                text_color='white')


class Display(Buttons):

    def __init__(self, data) -> None:
        super().__init__(data)
        user_cnt = len(data)

        # add button
        add_button = customtkinter.CTkButton(
            master=app,
            width=40,
            height=40,
            border_width=0,
            corner_radius=4,
            text="+",
            command=lambda: self.event_add(add_button),
            text_font=('Courier', 23, 'bold'))
        add_button.place(rely=1.0, relx=1.0, x=-10, y=-10, anchor=tkinter.SE)
        add_button.configure(
            fg_color='grey',
            hover_color='#04D81C',  # green
            text_color='white')

        if user_cnt >= 12:
            add_button.configure(state=tkinter.DISABLED)
        self.toggle_buttons(app)

    def toggle_buttons(self, app: customtkinter.CTk):
        toggle_cf = customtkinter.CTkButton(
            master=app,
            width=385,
            height=70,
            border_width=0,
            corner_radius=4,
            text="Codeforces",
            command=lambda: self.event_toggle_codeforces(toggle_cf),
            text_font=('@Batang', 23, 'bold'),
            hover='False')
        toggle_cf.place(x=10, y=10)
        toggle_cf.configure(fg_color='#217FF9', text_color='white')

        toggle_cc = customtkinter.CTkButton(
            master=app,
            width=385,
            height=70,
            border_width=0,
            corner_radius=4,
            text="Codechef",
            command=lambda: self.event_toggle_codechef(toggle_cc),
            text_font=('@Batang', 23, 'bold'),
            hover='False')
        toggle_cc.place(x=405, y=10)
        toggle_cc.configure(fg_color='#217FF9', text_color='white')

    def display_user(self, app: customtkinter.CTk, cnt, data) -> None:
        color = ["#494D59", '#373943']
        y_pos = 40 * (cnt - 1) + 100
        name, cf, cc = data[1], data[2], data[3]

        # × delete button
        del_button = customtkinter.CTkButton(
            master=app,
            width=30,
            height=30,
            border_width=0,
            corner_radius=4,
            text="×",
            command=lambda: self.event_delete(del_button),
            text_font=('Courier', 13, 'bold'))
        del_button.place(x=10, y=y_pos)
        del_button.configure(fg_color=color[cnt % 2],
                             hover_color='red',
                             text_color='white')
        self.button_id[del_button] = data[0]

        # name button
        name_button = customtkinter.CTkButton(
            master=app,
            width=305,
            height=30,
            border_width=0,
            corner_radius=4,
            text=name,
            command=lambda: self.event_stats(name_button),
            text_font=('@Batang', 13, 'bold'))
        name_button.place(x=45, y=y_pos)
        name_button.configure(
            fg_color=color[cnt % 2],
            hover_color='#AAC7FB',  # light blue
            text_color='white')
        self.button_id[name_button] = data

        # cf label
        cf = tkinter.StringVar(value=cf)
        label = customtkinter.CTkLabel(
            master=app,
            textvariable=cf,
            width=215,
            height=30,
            fg_color=("white", color[cnt % 2]),
            corner_radius=4,
        )
        label.configure(font=("@Batang", 13))
        label.place(x=355, y=y_pos)

        # cc label
        cc = tkinter.StringVar(value=cc)
        label = customtkinter.CTkLabel(
            master=app,
            textvariable=cc,
            width=215,
            height=30,
            fg_color=("white", color[cnt % 2]),
            corner_radius=4,
        )
        label.configure(font=("@Batang", 13))
        label.place(x=575, y=y_pos)

        pass


def stalker_window():
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("green")
    app.title("Stalker")
    app.geometry("800x640")
    app.iconbitmap("logo.ico")
    app.resizable(False, False)

    display = Display(data)
    for i in range(len(data)):
        display.display_user(app, i + 1, data[i])

    app.mainloop()


def scrape_friends(friend_list):
    global check_codechef
    global check_codeforces
    while True:
        if close_notifier:
            sys.exit()
        for friend in friend_list:
            if check_codeforces: friend.check_new_codeforces()
            if check_codechef: friend.check_new_codechef()


def notifier():
    friends = [[], [], [], []]
    for i in range(len(data)):
        frnd = UserActivityNotifier(data[i][1], data[i][2], data[i][3])
        friends[i % 4].append(frnd)

    for frnd_lst in friends:
        if len(frnd_lst) > 0:
            thread = threading.Thread(target=scrape_friends, args=(frnd_lst, ))
            thread.start()


close_notifier = 0
notifier_thread = threading.Thread(target=notifier)
notifier_thread.start()

stalker_window()

close_notifier = 1
print('done')