from collections import namedtuple
from dis import dis
from select import select
from tkinter import *
from tkinter import ttk

Catch = namedtuple('Catch', 'x y receiver')
global current_team, teams
current_team = 'light'
teams = {'light': [], 'dark': []}
possession = []

MMP = ['Bobby', 'Lucas', 'Walton', 'Kevin', 'Varun', 'Adam', 'Rob', 'Aaron',
       'Pudge', 'Bryan', 'Rye', 'Jared', 'Greg', 'Dalton', 'Brian', 'Devin', 'JP', 'Liam']
FMP = ['Karina', 'Fernanda', 'Gina', 'Clare', 'Kelly', 'Stella', 'Eva',
       'Molly', 'Liz', 'Rogie', 'Sleav', 'Sofia', 'Sajani', 'Olive', 'Helen']


class Player:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Selector(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            **kwargs
        )

        self.l = Label(self, text=f'Who is on light?',
                       bg='#7CFC00', fg='black')
        self.l.grid(row=0, column=0)

        self.buttons = {}
        self.select_dict = {}
        for p in MMP + FMP:
            self.select_dict[p] = IntVar()

        for i, p in enumerate(MMP):
            select_button = PlayerSelect(
                self, p, self.select_dict, variable=self.select_dict[p])
            self.buttons[p] = select_button
            select_button.grid(
                row=i//2 + 1, column=i % 2, sticky=W)
        for i, p in enumerate(FMP):
            select_button = PlayerSelect(
                self, p, self.select_dict, variable=self.select_dict[p])
            self.buttons[p] = select_button
            select_button.grid(
                row=i//2 + 1, column=i % 2 + 2, sticky=W)

        confirmButton = PlayerConfirm(
            self, self.select_dict, command=self.confirm)
        confirmButton.grid(row=0, column=2)

    def confirm(self):
        global current_team
        global teams
        if current_team == 'light':
            current_team = 'dark'
            teams['light'] = [k for k, v in self.select_dict.items()
                              if v.get() == 1]
            self.l.config(text='Who is on dark?')
            for v in teams['light']:
                self.select_dict[v].set(-1)
                self.buttons[v].config(state=['disabled'])
        else:
            teams['dark'] = [k for k, v in self.select_dict.items()
                             if v.get() == 1]
            self.lower()
        print(teams)


class PlayerSelect(Checkbutton):
    def __init__(self, parent, name, select_dict, **kwargs):
        super().__init__(parent, text=name,
                         bg='#7CFC00', fg='black', **kwargs)
        self.name = name
        self.select_dict = select_dict


class PlayerConfirm(Button):
    def __init__(self, parent, select_dict, **kwargs):
        super().__init__(parent, text='Done',
                         highlightbackground='#7CFC00', fg='black', **kwargs)
        self.select_dict = select_dict


class ReceivingTeam(Frame):
    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            **kwargs
        )

        Label(self, text=f'Who is receiving the pull?',
              bg='#7CFC00', fg='black').grid(row=0, column=0)

        def lightcb():
            global current_team
            current_team = 'light'
            self.lower()

        def darkcb():
            global current_team
            current_team = 'dark'
            self.lower()

        Button(self, text='light', bg='#7CFC00', fg='black',
               command=lightcb).grid(row=1, column=0)
        Button(self, text='dark', bg='#7CFC00', fg='black',
               command=darkcb).grid(row=2, column=0)


class Field(Canvas):
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            highlightthickness=5,
            highlightbackground='white',
            **kwargs
        )
        self.create_line(200, 0, 200, 400, fill='white', width=5)
        self.create_line(900, 0, 900, 400, fill='white', width=5)

        self.objects = []
        self.buttons = []
        self.pass_mode = True
        self.possession = []
        self.bind('<Button-1>', self.click_handler)

    def enable(self):
        self.possession.append(Catch(self.x, self.y))  # TODO: receiver class
        print(self.possession)
        self.pass_mode = True

    def disable(self):
        self.unbind('<Button-1>')

    def click_handler(self, event):
        global current_team
        global teams
        # show buttons
        if self.pass_mode:
            if self.possession:
                self.create_line(
                    self.possession[-1].x, self.possession[-1].y, event.x, event.y, fill='blue')
            self.objects.append(self.create_circle(
                event.x, event.y, 5, fill='blue'))
            self.x, self.y = event.x, event.y
            # show buttons/disable clicking then hide buttons/enable clicking
            for i, p in enumerate(teams[current_team]):
                flip = 1 if event.y < 200 else -1
                button = ReceiverSelect(self, p, command=self.enable)
                self.buttons.append(button)
                button.place(x=event.x, y=event.y +
                             (i * flip * 30) + ((flip - 1) * 15))

            self.pass_mode = False


class ReceiverSelect(Button):
    def __init__(self, parent, name, **kwargs):
        super().__init__(parent, text=name,
                         bg='#7CFC00', fg='black', **kwargs)
        self.name = name


root = Tk()

game = Field(root)
game.grid(column=0, row=0, sticky=(N, W, E, S))

team_page = ReceivingTeam(root)
team_page.grid(column=0, row=0, sticky=(N, W, E, S))
team_page.grid_propagate(0)

player_choice = Selector(root)
player_choice.grid(column=0, row=0, sticky=(N, W, E, S))
player_choice.grid_propagate(0)

root.mainloop()
