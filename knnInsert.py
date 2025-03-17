import pandas
import mysql.connector

db = mysql.connector.connect(
  host="",
  user="",
  password="",
  database = "dataTan"
)

cursor = db.cursor()
cursor.execute("drop table movie;")
cursor.execute("create table movie(name varchar(20), rating varchar(20), duration varchar(20), genre varchar(20));")
data = pandas.read_csv("knn.csv")

for _, i in data.iterrows():
    cursor.execute(f'insert into movie(name, duration, genre, rating) value("{i['name']}", "{i["duration"]}", "{i['genre']}", "{i["rating"]}");')
    print(i)
# print(data)
db.commit()
cursor.execute("select * from movie;")
d = cursor.fetchall()
print(d)