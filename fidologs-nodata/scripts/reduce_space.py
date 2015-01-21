import pickle
import numpy
from sklearn.decomposition import RandomizedPCA
from vectorspace import vectorspace
import random

FILE_IN_MSG = "../data/2001-lemmproc.pickle"
FILE_IN_WEIGHTS = "../data/2001-tfidf-uni.pickle"
FILE_OUT_PICKLE_VECTOR_SPACE = "../data/2001-vector_space-uni.pickle"

LOW_THRESHOLD = 4 # too common
HIGH_THRESHOLD = 8.1 # too rare

PERCENT_OF_EXPLAINED = 0.9

SAMPLING_RATIO = 1.0/4 # every fourth message

print "Loading data..."
messages = pickle.load(open(FILE_IN_MSG, "rb"))
messages_keys = messages.keys()
random.shuffle(messages_keys)
messages_keys = messages_keys[:int(len(messages_keys)*SAMPLING_RATIO)]
weights = pickle.load(open(FILE_IN_WEIGHTS, "rb"))
print "Subsetting data..."
global_set = []

for word, number in weights.iteritems():
    if LOW_THRESHOLD < number < HIGH_THRESHOLD:
        global_set.append(word)

print "Creating vector space"
vectors = []
names = []
total = len(messages_keys)
current = 0.0
for index in messages_keys:
    current += 1
    print "\b" * 50, "{0}% processed".format(round(current / total * 100, 2)),
    names.append(index)
    vectors.append(vectorspace(messages[index].uni, global_set))
vectors = numpy.array(vectors, numpy.short)

print "\nPerforming PCA..."
pca = RandomizedPCA()
pca.fit(vectors)
i = 0
c = 0.0
for component in pca.explained_variance_ratio_:
    if PERCENT_OF_EXPLAINED <= c:
        break
    i += 1
    c += component
components = i
print components, "dimensions remained from", len(global_set)
pca = RandomizedPCA(n_components=i)
red_vectors = pca.fit_transform(vectors)

print "Wrinig data..."
pickle.dump({"vectors":red_vectors, "names":names}, open(FILE_OUT_PICKLE_VECTOR_SPACE, "wb"))