import json
from tkinter import *

f = open('data1.json')
data = json.load(f)

root = Tk()
canvas = Canvas(root, width=1100,
                height=400,
                bg='#7CFC00',
                highlightthickness=5,
                highlightbackground='white')
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.create_line(200, 0, 200, 400, fill='white', width=5)
canvas.create_line(900, 0, 900, 400, fill='white', width=5)

for point in data:
    for possession in point[:-1]:
        x1, y1 = possession['catches'][-2][0], possession['catches'][-2][1]
        x2, y2 = possession['catches'][-1][0], possession['catches'][-1][1]
        if possession['direction'] == 'left':
            y1, y2 = y1 * -1 + 400, y2 * -1 + 400
            x1, x2 = x1 * -1 + 1100, x2 * -1 + 1100
        canvas.create_line(x1, y1, x2, y2, fill='blue', width=3, arrow=LAST)

root.mainloop()
