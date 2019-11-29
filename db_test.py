import csv
from pymysql.err import *
import pymysql
from dbconfig import db_config

# csv fields: 0 = article_id; 1 = title; 2 = authors; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
connection = pymysql.connect(**db_config)
with connection.cursor() as cursor:
    query = """
    SELECT * FROM articles
    LIMIT 10
    ;
    """
    try:
        ret = cursor.execute(query)
        data = cursor.fetchall()
    except MySQLError as err:
        if err.args[0] != 1062:
            print(err)
            print(row[0])
        else:
            print('empty abstract', i)

print(data)

connection.commit()
connection.close()
