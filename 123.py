import sqlite3
import functools
import operator

line = ['', '', '']

db = sqlite3.connect("//192.168.0.122/base2/ofd_db.db")
cur = db.cursor()
what = 'Глу'
what = (what+'%',)
print(what)

#try:
cur.execute('''SELECT * FROM ofd''')
i = cur.fetchall()
print(i)
#except sqlite3.ProgrammingError:


def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    str = '\n'.join(str)
    return str


#cur.execute('SELECT * FROM ofd WHERE org LIKE ?',what)
#row = cur.fetchall()
#print(row)
#try:
 #   row = convertTuple(row)
#except TypeError:
#    print('error')
#print(row)
#except sqlite3.DatabaseError as err:
 #   print("Error: ", err)

