import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.datasets import load_iris, load_wine
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


def classifyData(name, dataset, row):
    X = dataset.data
    y = dataset.target
    metrics = [[0 for iterations in range(10)] for algo in range(3)]

    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        metrics[0][i] = runAlgo("Decision Tree",
                                DecisionTreeClassifier(),
                                X_train, X_test, y_train, y_test)
        metrics[1][i] = runAlgo("Naive Bayes",
                                GaussianNB(),
                                X_train, X_test, y_train, y_test)
        metrics[2][i] = runAlgo("SVM",
                                svm.SVC(kernel="linear", C=0.01),
                                X_train, X_test, y_train, y_test)

    for i, metric in enumerate(["Accuracy", "Precision", "Recall"]):
        ax = plt.subplot(2, 3, i + row)
        ax.set_title(name + " Dataset " + metric)
        plt.xticks([0,1,2], ["Decision Tree","Naive Bayes","SVM"])
        plotBar(metrics[0], i, 0)
        plotBar(metrics[1], i, 1)
        plotBar(metrics[2], i, 2)


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
    avg_ = sum(a[index] for a in data) / 10

    return min_, max_, avg_


def runAlgo(name, algo, X_train, X_test, y_train, y_test):
    y_pred = algo.fit(X_train, y_train).predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    
    return accuracy, precision, recall

plt.subplots(nrows=2, ncols=3, figsize=(11, 7))
classifyData("Iris", load_iris(), 1)
print()
classifyData("Wine", load_wine(), 4)
plt.figlegend(["avg", "min", "max"], loc = 'lower center', ncol=5, labelspacing=0.)
plt.tight_layout(pad=3)
plt.show()
