
import pickle
import numpy


red_vectors = pickle.load(open(FILE_IN_PICKLE_VECTOR_SPACE, "rb"))["vectors"]

print red_vectors



print "Wrinig 2D data..."
pickle.dump({"vectors":red_vectors_2d}, open(FILE_OUT_PICKLE_2D_PCA_SPACE, "wb"))

