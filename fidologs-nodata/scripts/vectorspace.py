import numpy

def vectorspace(msg, all_words):
    components = [word for word in msg]
    return numpy.array([components.count(word) for word in all_words], numpy.short)