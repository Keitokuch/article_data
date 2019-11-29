import csv
from pymysql.err import *
import pymysql
from dbconfig import db_config

# csv fields: 0 = article_id; 1 = title; 2 = authors; 5 = entry_id; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
connection = pymysql.connect(**db_config)
with open("0.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    with connection.cursor() as cursor:
        query = """
        INSERT INTO article_entries
        VALUE (%(eid)s, %(aid)s, %(link)s, %(jid)s)
        ;
        """
        i = 0
        for row in reader:
            aid = int(row[0])
            print(aid)
            if aid > 800000 and aid != 1778082:
                break
            try:
                ret = cursor.execute(query, {'eid': row[5],
                                             'aid': row[0],
                                             'link': row[9],
                                             'jid': row[13]
                                             }
                                     )
                i += 1
            except MySQLError as err:
                print(err)
                print(row[0])

print(i)

connection.commit()
connection.close()
