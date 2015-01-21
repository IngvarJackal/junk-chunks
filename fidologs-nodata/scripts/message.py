class Message(object):
    def __init__(self):
        self.msg_id = None
        self.date = None
        self.user = None
        self.subject = None
        self.recipient = None
        self.uni = None
        self.bi = None
        self.bi_lemm = None
        self.raw_text = None

    def __str__(self):
        return ("ID: %i\nUSER: %s\nDATE: %s\nSUBJECT: %s\nRECIPIENT: %s\nUNIGRAMS: %s\nBIGRAMS: %s" %
                         (self.msg_id, self.user, self.date, self.subject, self.recipient,
                            "; ".join(self.uni).encode("utf-8"),
                            "; ".join([u" ".join(b) for b in self.bi]).encode("utf-8")))