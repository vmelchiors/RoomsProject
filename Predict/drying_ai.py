from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pickle

def drying_predict(time, days_week):
    input_data = [[time, days_week]]
    prediction = tree_drying.predict(input_data)
    return prediction


with open('./ensalamento.pkl', 'rb') as f:
    x_drying_training, y_drying_training, x_drying_test, y_drying_test = pickle.load(f)

tree_drying = DecisionTreeClassifier(criterion='entropy', random_state=0)
tree_drying.fit(x_drying_training, y_drying_training)

predictionsAD = tree_drying.predict(x_drying_test)

print(predictionsAD)