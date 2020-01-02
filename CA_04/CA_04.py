# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split  # Import train_test_split function
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation
from sklearn.datasets import load_iris
from sklearn import tree
import matplotlib

# load dataset
data = pd.read_csv("data.csv")
data.head()

# split dataset in features and target variable
X = data.drop(columns=['target'])  # Features
y = data.target  # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)  # 80% training and 20% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))


def print_tree(clf):
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(150, 100)
    tree.plot_tree(clf, filled=True, rounded=True, class_names=True)

# print_tree(clf)


# -------------PART 2-----------------
# load dataset
data = pd.read_csv("data.csv")
samples = list()
for i in range(5):
    samples.append(data.sample(n=150, replace=True))
    print(samples[i].head())