from dateutil.parser import parse
import pymorphy2
import nltk
import pickle
from message import Message
from nltk import decorators
morph = pymorphy2.MorphAnalyzer()

PATH_IN = "../data/pre-2001-proc.txt"
PATH_OUT_PLAIN = "../data/2001-lemmproc.txt"
PATH_OUT = "../data/2001-lemmproc.pickle"

SEPARATOR = "vbcnbzxclvjhzxcbhvjbzxcjvbjhzxcbvjhzxvbjhzxcbv<UNIQUE_STRING>vbcnbzxclvjhzxcbhvjbzxcjvbjhzxcbvjhzxvbjhzxcbv>"

def russianTokenizer(text):
    result = text
    result = result.replace('.', ' . ')
    result = result.replace(' .  .  . ', ' ... ')
    result = result.replace(',', ' , ')
    result = result.replace(':', ' : ')
    result = result.replace(';', ' ; ')
    result = result.replace('!', ' ! ')
    result = result.replace('?', ' ? ')
    result = result.replace('\"', ' \" ')
    result = result.replace('\'', ' \' ')
    result = result.replace('(', ' ( ')
    result = result.replace(')', ' ) ')
    result = result.replace('  ', ' ')
    result = result.replace('  ', ' ')
    result = result.replace('  ', ' ')
    result = result.replace('  ', ' ')
    result = result.strip()
    result = result.split(' ')
    return result

@decorators.memoize
def tokenize(word):
    return russianTokenizer(word)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

f_in = file(PATH_IN, "r")
messages = {}

fulltext = f_in.read().split(SEPARATOR)[:-1]
current = 0.0
maximum = len(fulltext)
for item in fulltext:
    current += 1
    print "\b" * 50, "{0}% processed".format(round(current / maximum * 100, 2)),

    msg = Message()

    items = item.split("\n")
    if items[0] == "":
      del items[0]
    msg.msg_id = int(items[0][len("ID: "):])
    msg.user = items[1][len("USER: "):]
    msg.date = parse(items[2][len("DATE: "):])
    msg.subject = items[3][len("SUBJECT: "):]
    msg.recipient = items[4][len("RECIPIENT: "):]
    raw_text = items[5][len("TEXT: "):]
    text = [w for w in (unicode(w.decode("utf-8")) for w in tokenize(raw_text)) if w.isalpha() and not (is_ascii(w) and len(w)<3)]
    lemm_text = [morph.parse(word)[0].normal_form for word in text]
    msg.uni = lemm_text
    msg.bi = nltk.bigrams(text)
    msg.bi_lemm = nltk.bigrams(lemm_text)
    msg.raw_text = raw_text

    messages[int(msg.msg_id)] = msg
f_in.close()

print "\nWriting data..."

with file(PATH_OUT_PLAIN, "w") as f_out_plain:
  f_out_plain.write(("\n" + SEPARATOR + "\n").join((str(text) for text in messages.values())))
  f_out_plain.write("\n")

pickle.dump(messages, open(PATH_OUT, "wb"))
