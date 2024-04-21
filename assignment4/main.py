from sklearn import svm
from sklearn.datasets import load_iris, load_wine
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


def classifyData(name, dataset):
    X = dataset.data
    y = dataset.target
    metrics = [[0 for iterations in range(10)] for algo in range(3)]

    print(name)
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

    for i in range(3):
        min_, max_, avg_ = getMinMaxAvg(metrics[i], 0)
        print("Accuracy   Min %.2f,  Avg %.2f,  Max %.2f" %
              (min_, max_, avg_))
        min_, max_, avg_ = getMinMaxAvg(metrics[i], 1)
        print("Precision  Min %.2f,  Avg %.2f,  Max %.2f" %
              (min_, max_, avg_))
        min_, max_, avg_ = getMinMaxAvg(metrics[i], 2)
        print("Recall     Min %.2f,  Avg %.2f,  Max %.2f" %
              (min_, max_, avg_))


def getMinMaxAvg(data, index):
    min_ = min(data, key = lambda a: a[index])[index]
    max_ = max(data, key = lambda a: a[index])[index]
    avg_ = (min_ + max_) / 2

    return min_, max_, avg_


def runAlgo(name, algo, X_train, X_test, y_train, y_test):
    y_pred = algo.fit(X_train, y_train).predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    
    return accuracy, precision, recall


classifyData("Iris Classification", load_iris())
print()
classifyData("Wine Classification", load_wine())