import json
import math
from tkinter import *

f = open('data1.json')
data = json.load(f)

root = Tk()
canvas = Canvas(root, width=400,
                height=1100,
                bg='#7CFC00',
                highlightthickness=5,
                highlightbackground='white')
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.create_line(0, 200, 400, 200, fill='white', width=5)
canvas.create_line(0, 900, 400, 900, fill='white', width=5)

# for point in data:
#     for possession in point[:-1]:
#         x1, y1 = possession['catches'][-2][0], possession['catches'][-2][1]
#         x2, y2 = possession['catches'][-1][0], possession['catches'][-1][1]
#         if possession['direction'] == 'left':
#             y1, y2 = y1 * -1 + 400, y2 * -1 + 400
#             x1, x2 = x1 * -1 + 1100, x2 * -1 + 1100
#         canvas.create_line(x1, y1, x2, y2, fill='blue', width=3, arrow=LAST)

for point in data:
    for possession in point[:-1]:
        x1, y1 = possession['catches'][-2][0], possession['catches'][-2][1]
        x2, y2 = possession['catches'][-1][0], possession['catches'][-1][1]
        if possession['direction'] == 'left':
            y1, y2 = y1 * -1 + 400, y2 * -1 + 400
            x1, x2 = x1 * -1 + 1100, x2 * -1 + 1100
        nx, ny = x2 - x1, y2 - y1
        k = math.sqrt((nx ** 2) + (ny ** 2))
        nx, ny = round(nx * 200/k), round(ny * 200/k)
        rx, ry = ny, -1 * nx
        canvas.create_line(200, 550, rx + 200, ry + 550,
                           fill='red', width=1, arrow=LAST)

root.mainloop()
