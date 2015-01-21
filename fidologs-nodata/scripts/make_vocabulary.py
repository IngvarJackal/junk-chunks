import codecs
import pickle
import operator
from message import Message
import numpy
from sklearn.feature_extraction.text import TfidfTransformer
from vectorspace import vectorspace

FILE_IN = "../data/2001-lemmproc.pickle"
FILE_OUT = "../data/2001-vocab.txt"
FILE_OUT_RESULTS = "../results/diverg-2001.txt"
FILE_OUT_PICKLE = "../data/2001-vocabs.pickle"
FILE_OUT_PICKLE_TFIDF = "../data/2001-tfidf-uni.pickle"
FILE_OUT_WORD_COUNTS = "../results/words-2001.txt"

print "Loading data..."
messages = pickle.load(open(FILE_IN, "rb"))

print "Creating user vocabularies"
users = {}
total = len(messages)
current = 0.0

words_count = {}
total_words = 0.0
words_per_user = {}
total_words_per_user = {}
for msg in messages.values():
    current += 1
    print "\b" * 50, "{0}% processed".format(round(current / total * 100, 2)),
    users[msg.user] = users.get(msg.user, set()).union(set(msg.uni))

    d = words_per_user.get(msg.user, {})
    for word in msg.uni:
        words_count[word] = words_count.get(word, 0) + 1
        total_words += 1
        d[word] = d.get(word, 0) + 1
        total_words_per_user[msg.user] = total_words_per_user.get(msg.user, 0.0) + 1
    words_per_user[msg.user] = d

global_set = set()
print "\nCreating global vocabulary..."
for s in users.values():
    global_set = global_set.union(s)

print "Creating vector space"
vectors = []
current = 0.0
for msg in messages.values():
    current += 1
    print "\b" * 50, "{0}% processed".format(round(current / total * 100, 2)),
    vectors.append(vectorspace(msg.uni, global_set))

print "\nCreating tf-idf terms..."
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectors)
weights = {}
for word, weight  in zip(global_set, transformer.idf_):
    weights[word] = weight

print "Writing data..."
with codecs.open(FILE_OUT, "w", encoding="utf-8") as out:
    for user, words in users.iteritems():
        out.write(unicode(user.decode("utf-8")))
        out.write(":")
        out.write(",".join(words))
        out.write("\n")
    out.write("TOTAL:")
    out.write(":")
    out.write(",".join(global_set))

total = len(global_set)
sorted_users_diverg = {}
for user, words in users.iteritems():
    sorted_users_diverg[user] = round(float(len(words))/total * 100, 4)
sorted_users = sorted(sorted_users_diverg.items(), key=operator.itemgetter(1), reverse=True)

with codecs.open(FILE_OUT_RESULTS, "w", encoding="utf-8") as out:
    for user in sorted_users:
        user = user[0]
        out.write(unicode(user.decode("utf-8") if user != "" else "<EMPTY_NICK>").ljust(30))
        out.write(": ")
        out.write(str(sorted_users_diverg[user]))
        out.write("%\n")

sorted_words = sorted(words_count.items(), key=operator.itemgetter(1), reverse=True)
with codecs.open(FILE_OUT_WORD_COUNTS, "w", encoding="utf-8") as out:
    for word in sorted_words:
        out.write(unicode(word[0] + ": " + str(word[1]) + " ({0:.2}%\t{1})\n".format(word[1]*100/total_words, weights[word[0]])))
    out.write("\n\n")

    # for user, words in words_per_user.iteritems():
    #     out.write(user.decode("utf-8") + u": ")
    #     for word, count in words.iteritems():
    #         s = word.encode("utf-8") + ": " + str(count) + " ({0:.2f}%), ".format(total_words_per_user[user]*100/total_words)
    #         print s, type(s)
    #         out.write(s.encode("utf-8"))
    #     out.write("'\n")

pickle.dump({"sorted_users":sorted_users, "data":users}, open(FILE_OUT_PICKLE, "wb"))
pickle.dump(weights, open(FILE_OUT_PICKLE_TFIDF, "wb"))
