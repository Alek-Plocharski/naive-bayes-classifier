import numpy as np
import pandas as pd

df = pd.read_csv("tennis.csv")
train = df.iloc[:-2]
test = df.iloc[-2:-1]

size = train.shape[0]
decisions = train.iloc[:,-1].unique()
decision_counts = []
for decision in decisions:
    decision_sample = train.loc[train[train.columns[-1]] == decision]
    decision_counts.append(decision_sample.shape[0])
probability_tables = []
attributes = train.iloc[:,0:-1].columns
i=0
for attribute in attributes:
    classes = train.iloc[:,i].unique()
    d = pd.DataFrame(0.0, index=np.arange(len(decisions)), columns=classes)
    for j in range(len(decisions)):
        decision_sample = train.loc[train[train.columns[-1]] == decisions[j]]
        decision_count = decision_sample.shape[0]
        for c in classes:
            attribute_count = decision_sample.loc[decision_sample[attribute] == (c if attribute != 'windy' else bool(c))].shape[0]
            d[c][j] = attribute_count / decision_count
    probability_tables.append(d)
    i += 1

def predict(observation):
    global decisions
    global probability_tables
    global decision_counts
    global size
    decision_probabilities = []
    for i in range(len(decisions)):
        probability = 1.0
        for j in range(len(observation)):
            probability *= probability_tables[j][observation[j]][i]
        probability *= float(decision_counts[i]) / float(size)
        decision_probabilities.append(probability)
    max_value = max(decision_probabilities)
    index = decision_probabilities.index(max_value)
    print([float(i)/sum(decision_probabilities) for i in decision_probabilities])
    print(decisions)
    return decisions[index]

print(predict(['overcast', 'hot', 'normal', False]))

