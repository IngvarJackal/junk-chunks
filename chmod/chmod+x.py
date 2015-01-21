import os, stat, sys
if len(sys.argv) != 2:
    print "usage: python chmod+x <file1>"
else:
    st = os.stat(sys.argv[1])
    os.chmod(sys.argv[1], st.st_mode | stat.S_IEXEC)
