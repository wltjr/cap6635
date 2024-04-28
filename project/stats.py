
import csv
import matplotlib.pyplot as plt


def plotBar(data, index, x):
    min_, max_, avg_ = getMinMaxAvg(data, index)
    plt.errorbar(x, avg_, fmt='ob', lw=3)
    plt.text(x + 0.1, avg_, round(avg_, 2))
    plt.errorbar(x, min_, fmt='_r', lw=3)
    plt.text(x + 0.1, min_, round(min_, 2))
    plt.errorbar(x, max_, fmt='_g', lw=3)
    plt.text(x + 0.1, max_, round(max_, 2))
    plt.errorbar(x, avg_, max_ - min_, fmt='.k', lw=1)


def getMinMaxAvg(data, index):
    min_ = min(data, key = lambda a: a[index])[index]
    max_ = max(data, key = lambda a: a[index])[index]
    avg_ = sum(a[index] for a in data) / len(data)

    return min_, max_, avg_


with open("data.csv") as csvfile:
    data = csv.reader(csvfile)
    stats = []
    for line in data:
        stats.append([int(i) for i in line])
    csvfile.close()

plt.subplots(nrows=1, ncols=2, figsize=(8, 4))

for i, metric in enumerate(["Nodes", "Cost"]):
    plt.suptitle("Statistics from %s Simulations" % (len(stats)))
    ax = plt.subplot(1, 2, i+1)
    ax.set_title("IRRT* + Bug 2 " + metric)
    plt.xticks([0,1], ["Online","Offline"])
    plotBar(stats, i, 0)
    plotBar(stats, i+2, 1)

plt.figlegend(["avg", "min", "max"], loc = 'lower center', ncol=5, labelspacing=0.)
plt.tight_layout(pad=3)
plt.subplots_adjust(top=0.86)
plt.show()
