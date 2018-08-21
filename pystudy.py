import tkinter as tk
from os import listdir, getcwd
from os.path import isfile, join

LARGE_FONT = ("Verdana", 12)
study_questions = {}
question_keys = []
question_values = []

def get_study_sets():
    path = getcwd() + "\studysets"
    sets = [f for f in listdir(path) if isfile(join(path, f))]
    return sets


def create_dict(file):
    study_questions.clear()
    with open(getcwd() + "\studysets\\" + file, 'r') as f:
        for line in f:
            line = line.strip("\n")
            key, value = line.split(':')
            study_questions[key] = value
    global question_keys
    global question_values
    for key in study_questions:
        question_keys.append(key)
        question_values.append(study_questions[key])


class Pystudy(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        if cont == PageTwo:
            assert len(study_questions) > 1, "User has not selected a study set"
        frame = self.frames[cont]
        frame.tkraise()


# Introduction page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#535863")
        label = tk.Label(self, text="Study Smarter With Pystudy", font=LARGE_FONT, bg="#535863", fg="#fdfdfe")
        label.pack(pady=50, padx=10)
        start_btn = tk.Button(self, text="Start Studying", bg="#979AA1",
                              activebackground="#5a5c60", fg="#fdfdfe", activeforeground="#fdfdfe",
                              relief=tk.FLAT, command=lambda: controller.show_frame(PageOne))
        start_btn.pack()


# Page to prompt the user to pick studyset(s) to be used
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#535863")
        label = tk.Label(self, text="Please choose a study set!", font=LARGE_FONT, bg="#535863", fg="#fdfdfe")
        label.pack(pady=50, padx=10)

        # Creates a checklist menu using get_study_sets
        menu_btn = tk.Menubutton(self, text="Choose a study set...", relief=tk.FLAT,  bg="#979AA1", fg="#fdfdfe")
        menu_btn.pack()
        menu_btn.menu = tk.Menu(menu_btn, tearoff=0)
        menu_btn["menu"] = menu_btn.menu
        for f in get_study_sets():
            menu_btn.menu.add_command(label=f, command=lambda: create_dict(f))
        start_btn = tk.Button(self, text="Next", bg="#979AA1",
                              activebackground="#5a5c60", fg="#fdfdfe", activeforeground="#fdfdfe",
                              relief=tk.FLAT, command=lambda: controller.show_frame(PageTwo))
        start_btn.pack(pady=10, padx=10)


# Catch all study page
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        self.counter = 0
        tk.Frame.__init__(self, parent, bg="#535863")
        self.label = tk.Label(self, text="Are you ready?", font=LARGE_FONT, bg="#535863", fg="#fdfdfe")
        self.label.pack(pady=50, padx=10)
        start_btn = tk.Button(self, text="Begin", bg="#979AA1",
                              activebackground="#5a5c60", fg="#fdfdfe", activeforeground="#fdfdfe",
                              relief=tk.FLAT, command=lambda: self.start(start_btn))
        start_btn.pack(pady=10, padx=10)

    def start(self, cont):
        cont.destroy()
        self.next_question()
        show_value = tk.Button(self, text="Show Answer", bg="#979AA1",
                              activebackground="#5a5c60", fg="#fdfdfe", activeforeground="#fdfdfe",
                              relief=tk.FLAT, command=lambda: self.show_answer())
        show_value.pack()
        next_question = tk.Button(self, text="Next", bg="#979AA1",
                               activebackground="#5a5c60", fg="#fdfdfe", activeforeground="#fdfdfe",
                               relief=tk.FLAT, command=lambda: self.next_question())
        next_question.pack()

    def next_question(self):
        try:
            self.label.config(text=question_keys[self.counter])
        except IndexError:
            self.counter = 0
            self.label.config(text=question_keys[self.counter])

        self.counter += 1

    def show_answer(self):
        try:
            self.label.config(text=question_values[self.counter - 1])
        except IndexError:
            self.counter = 0
            self.label.config(text=question_values[self.counter - 1])


app = Pystudy()
app.geometry("550x300")
app.resizable(width=False, height=False)
app.mainloop()
