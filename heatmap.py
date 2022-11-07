import json
import seaborn
import matplotlib.pyplot as plt

f = open('data1.json')
data = json.load(f)

xlist = []
ylist = []

# for point in data:
#     for possession in point:
#         catches = possession['catches'][:-1]
#         for catch in catches:
#             x, y = catch[0], catch[1]
#             if possession['direction'] == 'left':
#                 x, y =  x * -1 + 1100, y * -1 + 400
#             x, y = y, x
#             xlist.append(x)
#             ylist.append(y)

for point in data:
    possession = point[-1]
    catches = possession['catches'][:-1]
    for catch in catches:
        x, y = catch[0], catch[1]
        if possession['direction'] == 'left':
            x, y = x * -1 + 1100, y * -1 + 400
        x, y = y, x
        xlist.append(x)
        ylist.append(y)

plot = seaborn.kdeplot(xlist, ylist, shade=True)
plt.axis([0, 400, 0, 1100])
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
