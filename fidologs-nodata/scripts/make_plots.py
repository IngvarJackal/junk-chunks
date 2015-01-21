import pickle
import pylab
import numpy as np
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.decomposition import RandomizedPCA

FILE_IN_PICKLE_2D_SPACE = "../data/2001-2d-uni.pickle"
FILE_IN_LABELS = "../data/2001-clusters-uni.pickle"
FILE_IN_PICKLE_VECTOR_SPACE = "../data/2001-vector_space-uni.pickle"
FILE_CLUSTER_PCA_PLOTS_OUT = "../results/clusters-pca.png"
FILE_CLUSTER_LDA_PLOTS_OUT = "../results/clusters-lda.png"
FILE_CLUSTER_LDA_NORM_PLOTS_OUT1 = "../results/clusters-norm-left_part-lda.png"

OUT_DIR = "../results"

print "Loading labels..."
data = pickle.load(open(FILE_IN_LABELS, "rb"))
labels = data["h_labels"]
clusters = data["h_clusters"]

print "Loading vector data"
red_vectors = pickle.load(open(FILE_IN_PICKLE_VECTOR_SPACE, "rb"))["vectors"]

print "Performing PCA 2D..."
pca = RandomizedPCA(n_components=2)
matrix = pca.fit_transform(red_vectors) + 10

print "Creating PCA clusters log-log plot..."
pylab.figure(figsize=(24, 18))
pylab.scatter(np.log(matrix[:,0]), np.log(matrix[:,1]), s=400, c=labels, alpha=0.5, marker="o", lw = 0)
for i, txt in enumerate(labels):
    pylab.annotate(txt, (np.log(matrix[i,0])-0.01, np.log(matrix[i,1])-0.03))

print "Saving data..."
pylab.savefig(FILE_CLUSTER_PCA_PLOTS_OUT, dpi=150)

print "Performing 2D LDA..."
pca = LDA(n_components=2)
matrix = pca.fit_transform(red_vectors, labels) + 10

print "Creating LDA clusters log-log plot..."
pylab.figure(figsize=(24, 18))
pylab.scatter(np.log(matrix[:,0])/np.log(1.01),
              np.log(matrix[:,1])/np.log(1.01),
              s=400, c=labels, alpha=0.34, marker="o", lw = 0)
for i, txt in enumerate(labels):
    pylab.annotate(txt, (np.log(matrix[i,0])/np.log(1.01)-2.5,
                         np.log(matrix[i,1])/np.log(1.01)-2))

print "Saving data..."
pylab.savefig(FILE_CLUSTER_LDA_PLOTS_OUT, dpi=150)

matrix -= 10

print "Creating the left part of LDA clusters plot..."
pylab.figure(figsize=(120, 90))
pylab.scatter(matrix[:,0], matrix[:,1], s=400, c=labels, alpha=0.5, marker="o", lw = 0)
for i, txt in enumerate(labels):
    pylab.annotate(txt, (matrix[i,0]-20e-3, matrix[i,1]-27e-3))
x1,x2,y1,y2 = pylab.axis()
pylab.axis((-10, 10, y1, y2))

print "Saving data..."
pylab.savefig(FILE_CLUSTER_LDA_NORM_PLOTS_OUT1, dpi=60)


import codecs, random
def get_random_sample(cluster, messages, maxnum=8):
    result = []
    shuffled = cluster[::]
    random.shuffle(shuffled)
    randomN = shuffled[:maxnum]
    for msg in randomN:
        result.append(messages[msg].raw_text)
    return unicode("\n\n".join(result).decode("utf-8"))
FILE_OUT_VERBOSE = "../results/clusters-2001-uni-verbose.txt"
FILE_IN_MSG = "../data/2001-lemmproc.pickle"
clusters_hierarchical = clusters
messages = pickle.load(open(FILE_IN_MSG))
with codecs.open(FILE_OUT_VERBOSE, "w", encoding="utf-8") as file_out:
    file_out.write(" H I E R A R C H I C A L   C L U S T E R S")
    for cluster, names in clusters_hierarchical.iteritems():
        file_out.write(u"\n==== " + str(cluster) + " | " + str(len(names)) + u" ====\n")
        file_out.write(u"".join([x for x in get_random_sample(names, messages)]))
        file_out.write("\n")