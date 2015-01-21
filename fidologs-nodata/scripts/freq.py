import pickle
from message import Message
import codecs
import operator

FILE_IN = "../data/2001-lemmproc.pickle"
FILE_OUT = "../results/freq-2001-uni.txt"
FILE_OUT_PICKLE = "../data/2001-freq-uni.pickle"

users = {}
users_weighted = {}

print "Loading data..."
messages = pickle.load(open(FILE_IN, "rb"))

total = len(messages)
current = 0.0
for msg in messages.values():
    current += 1
    print "\b" * 50, "{0}% processed".format(round(current / total * 100, 2)),
    users[msg.user] = users.get(msg.user, 0) + 1
    users_weighted[msg.user] = users_weighted.get(msg.user, 0) + len(msg.bi)/2 + 1

top_flooders = sorted(users.items(), key=operator.itemgetter(1), reverse=True)[:5]
top_flooders_weighted = sorted(users_weighted.items(), key=operator.itemgetter(1), reverse=True)[:5]

sorted_users = {}
for user in users.keys():
    sorted_users[user] = users[user] * users_weighted[user]
sorted_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)

with codecs.open(FILE_OUT, "w", encoding="utf-8") as out:
    for user in sorted_users:
        user = user[0]
        out.write(unicode(user.decode("utf-8") if user != "" else "<EMPTY_NICK>").ljust(30))
        out.write("messages: ")
        out.write(str(users[user]).ljust(5))
        out.write("amount of text: ")
        out.write(str(users_weighted[user]).ljust(10))
        out.write("average length of message: ")
        out.write(str(round(1.0*users_weighted[user]/users[user], 2)).ljust(10))
        out.write("\n")
    out.write("\nTOP FLOODERS: ")
    out.write(unicode(", ".join([x[0] for x in top_flooders]).decode("utf-8")))
    out.write("\nTOP WEIGHTED FLOODERS: ")
    out.write(unicode(", ".join([x[0] for x in top_flooders_weighted]).decode("utf-8")))
    out.write("\n")

pickle.dump({"sorted_users":sorted_users, "data":users, "weighted_data": users_weighted}, open(FILE_OUT_PICKLE, "wb"))