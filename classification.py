from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

def classifySVM(x,y,ts,r):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=ts, random_state=42)
    clf = svm.SVC(C=r)
    clf.fit(X_train, y_train.values.ravel())
    return clf.score(X_test,y_test)

def classifyKNN(x,y,ts,n):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=ts, random_state=42)
    neigh = KNeighborsClassifier(n_neighbors=n)
    neigh.fit(X_train, y_train.values.ravel())
    return neigh.score(X_test,y_test)

def classifyLR(x,y,ts,p):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=ts, random_state=42)
    clf = LogisticRegression(random_state=0,penalty=p)
    clf.fit(X_train, y_train.values.ravel())
    return clf.score(X_test,y_test)


def classify(x,y,args):
    match args.model:
        case 'svm':
            return "Not found"
        case 'knn':
            return "Not found"
        case 'lr':
            return "Not found"
        case _:
            raise Exception('invalid classification method')