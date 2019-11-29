import sys
import csv
import difflib

def later(a, b):
    ya = int(a[:4])
    yb = int(b[:4])
    ma = int(a[5:7])
    mb = int(b[5:7])
    da = int(a[8:10])
    db = int(b[8:10])
    if da < db:
        return False
    elif da == db:
        if ma < mb:
            return False
        elif ma == mb:
            if da < db:
                return False
    return True

# csv fields: 0 = article_id; 1 = title; 2 = authors; 5 = entry_id; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
with open("0.csv") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    prev = ['-1'] * 6
    d = difflib.Differ()
    tl = 0
#    for i in range(1100000):
    #  for i in range(500000):
    for i in range(1000):
        try:
            t = next(reader)
        except StopIteration:
            print(i)
            sys.exit(0)

        assert prev[5] != t[5]
        """
        if prev[0] == t[0]:
            #print(prev[0], prev[1], prev[2], prev[9], prev[13])
            #print(t[0], t[1], t[2], t[9],t[13])
            #print(prev[0], prev[1])
            #print(t[0], t[1])
            #assert prev[2] == t[2]
#           assert prev[9] != t[9]
#           assert prev[5] != t[5]
#           print(prev[15], t[15])

            if (prev[10] != t[10]):
                if later(t[11], prev[11]):
                    if len(prev[10]) <= len(t[10]):
                        print("True")
                    else:
                        print("False")
                        print(prev[10])
                        print(t[10])
                else:
                    if len(prev[10]) > len(t[1]):
                        print("True")
                    else:
                        print("False")
#           if (prev[11] != t[11]):
#               print(later(prev[11], t[11]), prev[11], t[11])

            if prev[10] != t[10]:
                print(len(prev[10]))
                print(prev[10])
                print(len(t[10]))
                print(t[10])

            if prev[11] != t[11]:
                print(prev[11], t[11])

            diff = []
            for j in range(1, 17):
                if prev[j] != t[j]:
                    diff.append(j)
            print(diff)
            """
        prev = t

        #if i in [6, 7]:
        #    print(t[0], t[10])
