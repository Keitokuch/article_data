import csv
from pymysql.err import *
import pymysql
from dbconfig import db_config


with open('ai_ids.csv') as f:
    journal_list = f.read().splitlines()

# csv fields: 0 = article_id; 1 = title; 2 = authors; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
connection = pymysql.connect(**db_config)
with open("0.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    with connection.cursor() as cursor:
        query = """
        INSERT INTO articles
        VALUE (%(id)s, LEFT(%(title)s, 2047), LEFT(%(authors)s, 1023), %(abstract)s)
        ;
        """
        i, ii = 0, 0
        for row in reader:
            if row[10] != '' and int(row[0]) < 800000:
                try:
                    ret = cursor.execute(query, {'id': row[0],
                                                 'title': row[1],
                                                 'authors': row[2],
                                                 'abstract': row[10]
                                                 }
                                         )
                    i += 1
                except MySQLError as err:
                    if err.args[0] != 1062:
                        print(err)
                        print(row[0])
            else:
                print('empty abstract', i)

print(i)


connection.commit()
connection.close()
