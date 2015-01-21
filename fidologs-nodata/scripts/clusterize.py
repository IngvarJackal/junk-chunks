import pickle
from sklearn.cluster import AgglomerativeClustering, MiniBatchKMeans
from sklearn import metrics
from collections import Counter


FILE_IN_MSG = "../data/2001-lemmproc.pickle"
FILE_IN_VEC = "../data/2001-vector_space-uni.pickle"
FILE_OUT_RESULTS = "../results/clusters-2001-uni.txt"
FILE_OUT_VERBOSE = "../results/clusters-2001-uni-verbose.txt"
FILE_OUT_PICKLE_RESULTS = "../data/2001-clusters-uni.pickle"

REDUCING_NUMBER = 80 # reduce number of clusters by this value

print "Loading data..."
data = pickle.load(open(FILE_IN_VEC))
messages = pickle.load(open(FILE_IN_MSG))

vect = data["vectors"]
nams = data["names"]
n_clust = len(nams)/REDUCING_NUMBER

print "Hierarchical clustering..."
c_comp_cos = AgglomerativeClustering(n_clusters=n_clust, affinity="cosine", linkage="complete").fit(vect)
c_comp_cos_labels = c_comp_cos.labels_
clusters_hierarchical = {}
for name, cluster in zip(nams, c_comp_cos_labels):
    clusters_hierarchical[cluster] = clusters_hierarchical.get(cluster, []) + [name]

print "k-mean clustering..."
c_kmean_b = MiniBatchKMeans(n_clusters=n_clust).fit(vect)
c_kmean_b_labels = c_kmean_b.labels_
clusters_kmean = {}
for name, cluster in zip(nams, c_kmean_b_labels):
    clusters_kmean[cluster] = clusters_kmean.get(cluster, []) + [name]

print "Writing output..."
with open(FILE_OUT_RESULTS, "w") as file_out:
    file_out.write(" H I E R A R C H I C A L   C L U S T E R S\n")
    for cluster, names in clusters_hierarchical.iteritems():
        file_out.write(str(cluster))
        file_out.write(":")
        file_out.write(",".join([str(x) for x in names]))
        file_out.write("\n")
    file_out.write("SILHOUETTE SCORE (euclidean): " + str(metrics.silhouette_score(vect, c_comp_cos_labels, metric='euclidean')))
    file_out.write("\n")
    file_out.write("SILHOUETTE SCORE (cosine): " + str(metrics.silhouette_score(vect, c_comp_cos_labels, metric='cosine')))
    file_out.write("\n" + "-"*79 + "\n K - M E A N   C L U S T E R S\n")
    for cluster, names in clusters_kmean.iteritems():
        file_out.write(str(cluster))
        file_out.write(":")
        file_out.write(",".join([str(x) for x in names]))
        file_out.write("\n")
    file_out.write("SILHOUETTE SCORE (euclidean): " + str(metrics.silhouette_score(vect, c_kmean_b_labels, metric='euclidean')))
    file_out.write("\n")
    file_out.write("SILHOUETTE SCORE (cosine): " + str(metrics.silhouette_score(vect, c_kmean_b_labels, metric='cosine')))

pickle.dump({"h_clusters":clusters_hierarchical,
             "h_labels":c_comp_cos_labels,
             "k_clusters":clusters_kmean,
             "k_labels":c_kmean_b_labels}, open(FILE_OUT_PICKLE_RESULTS, "wb"))