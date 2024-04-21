from sklearn import svm
from sklearn.datasets import load_iris, load_wine
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


def classifyData(name, dataset):
    X = dataset.data
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)
    print(name)
    accuracy, precision, recall = runAlgo("Decision Tree", DecisionTreeClassifier(), X_train, X_test, y_train, y_test)
    accuracy, precision, recall = runAlgo("Naive Bayes", GaussianNB(), X_train, X_test, y_train, y_test)
    accuracy, precision, recall = runAlgo("SVM", svm.SVC(kernel="linear", C=0.01), X_train, X_test, y_train, y_test)


def runAlgo(name, algo, X_train, X_test, y_train, y_test):
    y_pred = algo.fit(X_train, y_train).predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    print("%13s, Accuracy %.2f,  Precision %.2f,  Recall %.2f" %
          (name, accuracy, precision, recall))
    
    return accuracy, precision, recall


classifyData("Iris Classification", load_iris())
print()
classifyData("Wine Classification", load_wine())