from dateutil.parser import parse
from time import mktime
from datetime import datetime
import re

PATH_IN = "../data/raw-2001.txt"
PATH_OUT = "../data/pre-2001-proc.txt"

FROM = "From - "
X_COMMENT_TO = "X-Comment-To: "
FROM_FIELD = "From: "
DATE = "Date: "
SUBJECT = "Subject: "
TEXT_START = "X-Mozilla-Status2: 00000000"

SEPARATOR = "vbcnbzxclvjhzxcbhvjbzxcjvbjhzxcbvjhzxvbjhzxcbv<UNIQUE_STRING>vbcnbzxclvjhzxcbhvjbzxcjvbjhzxcbvjhzxvbjhzxcbv>"

f_in = file(PATH_IN, "r")
f_out = file(PATH_OUT, "w")

class Message(object):
    def __init__(self):
        self.msg_id = None
        self.date = None
        self.user = None
        self.subject = None
        self.recipient = None
        self.text = None
        self.processed = False

    def process(self):
        self.processed = True

        self.date = str(datetime.fromtimestamp(mktime(parse(self.date).utctimetuple())).strftime("%d %b %Y %H:%M:%S"))

        self.text = "".join([t for t in self.text if t.find(">") == -1 and t.find("wrote") == -1]) # remove citations
        if self.text.find(".UUE") != -1 or self.text.find("section") != -1: # remove UUE-texts
            self.text = "<UUE_CONTAINER_REMOVED>"
        self.text = str(re.sub(r"\s+", " ", self.text)).strip()

        self.user = self.user[:self.user.find("<") - 1]

        self.subject = self.subject.strip().replace("Re: ", "").replace("Re^2: ", "").replace("Re : ", "").replace("Re^2 : ", "")

        if self.recipient:
            self.recipient = self.recipient.strip()

    def __str__(self):
        if not self.processed:
            self.process()
        return "".join(["ID: {msg_id}\nUSER: {user}\nDATE: {date}\nSUBJECT: {subject}\nRECIPIENT: {recipient}\nTEXT: {text}\n"
                                         .format(msg_id = self.msg_id, user=self.user, date=self.date, subject=self.subject, recipient=self.recipient, text=self.text),
                                     SEPARATOR,
                                     "\n"])

msg = Message()
textmode = False
text = []
msg_id = 0
number = 0
for line in f_in.readlines():
    number += 1
    if number % 1000 == 0:
        print "\b" * 50, "{0}k lines processed".format(number / 1000),
    if line.startswith(FROM):
        textmode = False
        msg.text = text
        text = []
        if msg.date:
            msg.msg_id = msg_id
            msg_id += 1
            f_out.write(str(msg))
        msg = Message()
    if not textmode:
        if line.startswith(TEXT_START):
            textmode = True
        if line.startswith(X_COMMENT_TO):
            msg.recipient = line[len(X_COMMENT_TO):]
        elif line.startswith(FROM_FIELD):
            msg.user = line[len(FROM_FIELD):]
        elif line.startswith(DATE):
            msg.date = line[len(DATE):]
        elif line.startswith(SUBJECT):
            msg.subject = line[len(SUBJECT):]
    else:
        text.append(line)
        
f_in.close()
f_out.close()