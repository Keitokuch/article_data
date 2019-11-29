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

with open('ai_ids.csv') as f:
    #journal_list = [int(s) for s in f.read().splitlines()]
    journal_list = f.read().splitlines()
    print(journal_list)

dd = {}

# csv fields: 0 = article_id; 1 = title; 2 = authors; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
with open("1.csv") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    cnt = 0
    for row in reader:
        #  if row[13] in journal_list:
            #  cnt += 1
            #  print(cnt)
        if row[13] in dd:
            dd[row[13]] += 1
        else:
            dd[row[13]] = 1

print(dd)

