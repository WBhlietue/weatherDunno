import pandas
import server
data = pandas.read_csv("data.csv")

db = server.db
cursor = db.cursor()
cursor.execute(f"drop table if exists weather;")
cursor.execute(f"create table if not exists weather(weather varchar(10), temperature varchar(10), water varchar(10), wind varchar(10), result varchar(10));")

for _, i in data.iterrows():
    cursor.execute(f'insert into weather(weather, temperature, water, wind, result) value("{i["weather"]}", "{i["temperature"]}", "{i["water"]}", "{i["wind"]}", "{i["result"]}");')

db.commit()
cursor.execute("select * from weather;")
d = cursor.fetchall()

print(d)