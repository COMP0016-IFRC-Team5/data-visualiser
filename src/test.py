import matplotlib.pyplot as plt


x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 4, 6]
plt.scatter(x, y)

for i in range(len(x)):
    plt.text(x[i], y[i], f'({x[i]}, {y[i]})', ha='center', va='bottom')


plt.show()