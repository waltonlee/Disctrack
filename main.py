from collections import namedtuple
import json
from tkinter import *

Catch = namedtuple('Catch', 'x y receiver')
global current_team, teams, direction, canvas, arrow, points, select_dict, select_buttons
select_dict = {}
points = []
current_team = 'light'
teams = {'light': [], 'dark': []}

MMP = ['Bobby', 'Lucas', 'Walton', 'Kevin', 'Varun', 'Adam', 'Rob', 'Aaron',
       'Pudge', 'Bryan', 'Rye', 'Jared', 'Greg', 'Dalton', 'Brian', 'Devin', 'JP', 'Liam']
FMP = ['Karina', 'Fernanda', 'Gina', 'Clare', 'Kelly', 'Stella', 'Eva',
       'Molly', 'Liz', 'Rogie', 'Sleav', 'Sofia', 'Sajani', 'Olive', 'Helen']


class Player:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Possession:
    def __init__(self, direction='', players=''):
        self.direction = direction
        self.players = players
        self.catches = []


class Selector(Frame):
    def __init__(self, parent, **kwargs):
        global select_dict, select_buttons
        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            **kwargs
        )

        self.l = Label(self, text='Who is on light?',
                       bg='#7CFC00', fg='black')
        self.l.grid(row=0, column=0)

        select_buttons = {}
        for p in MMP + FMP:
            select_dict[p] = IntVar()

        for i, p in enumerate(MMP):
            select_button = PlayerSelect(
                self, p, variable=select_dict[p])
            select_buttons[p] = select_button
            select_button.grid(
                row=i//2 + 1, column=i % 2, sticky=W)
        for i, p in enumerate(FMP):
            select_button = PlayerSelect(
                self, p, variable=select_dict[p])
            select_buttons[p] = select_button
            select_button.grid(
                row=i//2 + 1, column=i % 2 + 2, sticky=W)

        confirmButton = PlayerConfirm(
            self, command=self.confirm)
        confirmButton.grid(row=0, column=2)

    def confirm(self):
        global current_team, teams
        if current_team == 'light':
            current_team = 'dark'
            teams['light'] = [k for k, v in select_dict.items()
                              if v.get() == 1]
            self.l.config(text='Who is on dark?')
            for v in teams['light']:
                select_dict[v].set(-1)
                select_buttons[v].config(state=['disabled'])
        else:
            teams['dark'] = [k for k, v in select_dict.items()
                             if v.get() == 1]
            self.l.config(text='Who is on light?')
            self.lower()
        print(teams)


class PlayerSelect(Checkbutton):
    def __init__(self, parent, name, **kwargs):
        super().__init__(parent, text=name,
                         bg='#7CFC00', fg='black', **kwargs)
        self.name = name


class PlayerConfirm(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text='Done',
                         highlightbackground='#7CFC00', fg='black', **kwargs)


class ReceivingTeam(Frame):
    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            **kwargs
        )

        Label(self, text='Who is receiving the pull?',
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


class StartingDirection(Frame):
    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            width=1100,
            height=400,
            bg='#7CFC00',
            **kwargs
        )

        Label(self, text='Which direction is the starting team going?',
              bg='#7CFC00', fg='black').grid(row=0, column=0)

        def leftcb():
            global direction, canvas, arrow
            direction = 'left'
            arrow = canvas.create_line(20, 380, 60, 380, arrow=FIRST)
            self.lower()

        def rightcb():
            global direction, canvas, arrow
            direction = 'right'
            arrow = canvas.create_line(20, 380, 60, 380, arrow=LAST)
            self.lower()

        Button(self, text='left', bg='#7CFC00', fg='black',
               command=leftcb).grid(row=1, column=0)
        Button(self, text='right', bg='#7CFC00', fg='black',
               command=rightcb).grid(row=2, column=0)


class Game(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            width=1100,
            height=400,
            **kwargs
        )
        global canvas
        canvas = Field(self)
        canvas.place(x=0, y=0)


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

        self.parent = parent
        self.objects = []
        self.buttons = []
        self.point = []  # list of possessions
        self.possession = Possession()
        self.pass_mode = True
        self.bind('<Button-1>', self.click_handler)
        end_button = EndButton(self)
        end_button.place(x=1050, y=370)

    def turnover(self):
        global current_team, direction, arrow
        current_team = 'dark' if current_team == 'light' else 'light'
        direction = 'left' if direction == 'right' else 'right'
        if direction == 'left':
            self.itemconfig(arrow, arrow=FIRST)
        if direction == 'right':
            self.itemconfig(arrow, arrow=LAST)

        self.point.append(self.possession)

        self.possession = Possession(direction, teams[current_team])
        for x in self.objects:
            self.delete(x)
        self.turnover_button.destroy()
        if self.score_button:
            self.score_button.destroy()
        # change line colors?

    def score(self):
        global points, select_dict, select_buttons, current_team, arrow

        self.point.append(self.possession)
        self.possession = Possession()
        points.append(self.point)
        self.point = []
        self.parent.lower()
        current_team = 'light'

        for p in select_dict:
            select_dict[p].set(0)
        for b in select_buttons:
            select_buttons[b].config(state=['normal'])
        for x in self.objects:
            self.delete(x)
        self.delete(arrow)
        self.turnover_button.destroy()
        self.score_button.destroy()

    def receiver_cb(self, name):
        global direction
        self.possession.catches.append(Catch(self.x, self.y, name))
        for button in self.buttons:
            button.destroy()
        # print(self.possession)

        self.turnover_button = TurnoverButton(self, command=self.turnover)
        self.turnover_button.place(x=0, y=0)

        if (direction == 'right' and self.x > 900) or (direction == 'left' and self.x < 200):
            self.score_button = ScoreButton(self, command=self.score)
            self.score_button.place(x=0, y=30)
            # TODO: No more passes until new teams

        self.pass_mode = True

    def click_handler(self, event):
        global current_team, teams, direction
        # show buttons
        if self.pass_mode:
            if self.possession.catches:
                self.turnover_button.destroy()
                self.objects.append(self.create_line(
                    self.possession.catches[-1].x, self.possession.catches[-1].y, event.x, event.y, fill='blue'))
            else:
                self.possession = Possession(direction, teams[current_team])
            self.objects.append(self.create_circle(
                event.x, event.y, 5, fill='blue'))
            self.x, self.y = event.x, event.y
            # show buttons/disable clicking then hide buttons/enable clicking
            for i, p in enumerate(teams[current_team]):
                flip = 1 if event.y < 200 else -1
                button = ReceiverSelect(self, p)
                self.buttons.append(button)
                button.place(x=event.x, y=event.y +
                             (i * flip * 30) + ((flip - 1) * 15))

            self.pass_mode = False


class ReceiverSelect(Button):
    def __init__(self, parent, name, **kwargs):
        def callback():
            parent.receiver_cb(name)
        super().__init__(parent, text=name,
                         bg='#7CFC00', fg='black', command=callback, **kwargs)


class TurnoverButton(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text='turnover',
                         bg='#7CFC00', fg='black', **kwargs)


class ScoreButton(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text='score',
                         bg='#7CFC00', fg='black', **kwargs)


def obj_dict(obj):
    return obj.__dict__


def end():
    global points
    print(json.dumps(points, default=obj_dict))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(points, f, ensure_ascii=False, indent=4, default=obj_dict)


class EndButton(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text='end',
                         bg='#7CFC00', fg='black', command=end, **kwargs)


root = Tk()

game = Game(root)
game.grid(column=0, row=0, sticky=(N, W, E, S))
game.grid_propagate(0)

direction_page = StartingDirection(root)
direction_page.grid(column=0, row=0, sticky=(N, W, E, S))
direction_page.grid_propagate(0)

team_page = ReceivingTeam(root)
team_page.grid(column=0, row=0, sticky=(N, W, E, S))
team_page.grid_propagate(0)

player_choice = Selector(root)
player_choice.grid(column=0, row=0, sticky=(N, W, E, S))
player_choice.grid_propagate(0)

root.mainloop()
