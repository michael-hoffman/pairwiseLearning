from sklearn.manifold import *
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from dataUtils import *
import numpy as np

items_names_dir = "../../DATA/ml-20m/movies.csv"
data_dir = "../../GeneratedData/data1"


def OneVsOther(features, labels):
    array = np.arange(labels.shape[0])
    np.random.shuffle(array)
    ex = labels.shape[0] * 0.66
    classif = OneVsRestClassifier(estimator=SVC(random_state=0))
    #score = cross_val_score(classif, features, label, cv=5)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    classif.fit(features[array[:ex]], labels[array[:ex]])
    print(min(classif.predict(features[array[:ex]])), max(classif.predict(features[array[:ex]])))
    print(classif.score(features[array[ex:]], labels[array[ex:]]))
    print(sum(labels[array[ex:]]) / (labels.shape[0]-ex+1e-10), ex)
    #np.savetxt(classif.fit(FLAGS.checkpoint_dir + "/linear", features))

def tSNE_conv():
    items_names = GetItemsNames(items_names_dir)
    items_test = np.genfromtxt(data_dir + "/test_items.txt")
    print(items_test.shape[0])
    items_test  = items_test.astype(int)
    item_vecs, item_bias, user_vecs, user_bias, global_bias, user_vecs_train, user_bias_train = GetData(data_dir)

    model = SpectralEmbedding(n_components=2)

    Y = model.fit_transform(item_vecs)
    print(item_vecs.shape[0])
    colors = []
    colors_names = {}
    n_colors = 0
    items = []
    for i in range(items_test.shape[0]):
        try:
            ganr = items_names[items_test[items_test[i]] + 1][-1]
            ganr = ganr.split("|")
        except:
            continue
        #print(len(ganr))
        if (len(ganr) > 1):
            continue
        ganr = ganr[0]
        if (ganr not in colors_names):
            colors_names[ganr] = [n_colors, 0]
            n_colors += 1
        colors_names[ganr][-1] += 1
        if (ganr.find('Comedy') > -1 or ganr.find('Dram') > -1):
            if colors_names[ganr][-1] >= 500:
               continue
            if (ganr.find('Comedy') > -1):
                colors.append(0)
            else:
                colors.append(1)
            items.append(items_test[i])
    items = np.array(items, int)
    for c in colors_names:
        print(c, colors_names[c])
    OneVsOther(item_vecs[items], np.array(colors))

tSNE_conv()

