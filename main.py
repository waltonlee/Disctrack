from collections import namedtuple
from tkinter import *
from tkinter import ttk

Catch = namedtuple('Catch', 'x y')
possession = []

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
        
        self.objects=[]
        self.bind("<Button-1>", self.click_handler)
        
    def click_handler(self, event):
        new_catch = Catch(event.x, event.y)
        if possession:
            self.create_line(possession[-1].x, possession[-1].y, new_catch.x, new_catch.y, fill='blue')
        possession.append(Catch(event.x, event.y)) # TODO: receiver class
        self.objects.append(self.create_circle(event.x, event.y, 5, fill='blue'))

root = Tk()

game = Field(root)
game.grid(column=0, row=0, sticky=(N, W, E, S))



root.mainloop()
