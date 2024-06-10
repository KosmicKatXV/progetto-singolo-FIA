from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.metrics import confusion_matrix as cm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

def classify(x,y,args):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=args.testsize, random_state=42)
    match args.model:
        case 'svm':
            clf = svm.SVC(C=args.regularisation)
        case 'knn':
            clf = KNeighborsClassifier(n_neighbors=args.neighbours)
        case 'lr':
            clf = LogisticRegression(random_state=0,penalty=args.penalty)
        case _:
            raise Exception('invalid classification method')
    clf.fit(X_train, y_train.values.ravel())
    y_pred = clf.predict(X_test)
    #confusionMatrix = cm(y_test, y_pred)
    #return clf.score(X_test,y_test),confusionMatrix
    return y_test,y_pred