#!/usr/local/bin/python3.3
# Requires python >= 3.3

import mysql.connector
from mysql.connector import errorcode

m = {
	'user': 'ba73e3e4f35e25',
	'pass': 'c3965805',
	'host': 'us-cdbr-iron-east-02.cleardb.net',
	'db': 'heroku_2e0ebcf7ba84509'
}


try:
	cnx = mysql.connector.connect(user=m['user'], password=m['pass'], host=m['host'], database=m['db'])

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)

DROP_TABLE_CMD = 'DROP TABLE numbers'

MAKE_TABLE_CMD = (
    "CREATE TABLE `numbers` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `num` BIGINT UNSIGNED NOT NULL,"
    "  `json`  TEXT NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE(`num`)"
    ") ENGINE=InnoDB")

cursor = cnx.cursor()

try:
	#cursor.execute( DROP_TABLE_CMD  )
	cursor.execute( MAKE_TABLE_CMD  )

except mysql.connector.Error as err:

	if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
		print("Table already exists.")
	else:
		print("Error: " + err.msg)
else:
	print("Created Table with command: %s" % MAKE_TABLE_CMD )


cnx.close()



#cur = db.cursor() 

# Use all the SQL you like
#cur.execute("SHOW TABLES")

# print all the first cell of all the rows
#for row in cur.fetchall() :
#    print row[0]


