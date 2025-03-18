import pandas
import server
data = pandas.read_csv("dataC.csv")

db = server.db
cursor = db.cursor()
cursor.execute("drop table if exists cars;")
cursor.execute(f"create table if not exists cars(id int, mark varchar(50), model varchar(50), color varchar(20), class char(1), motor int, forWhat varchar(50), type varchar(60), position varchar(12), madeDate char(4), enterDate char(11), country varchar(50));")

data_to_insert = []
for _, i in data.iterrows():
    data_to_insert.append((
        i["ТХ id"],
        i["Марк"],
        i["Модель"],
        i["Өнгө"],
        i["Ангилал"],
        i["Хөдөлгүүрийн багтаамж"],
        i["Зориулалт"],
        i["Тээврийн хэрэгслийн төрөл"],
        i["Хүрдний байрлал"],
        i["Үйлдвэрлэсэн он"],
        i["Орж ирсэн огноо"],
        i["Үйлдвэрлэсэн улс"]
    ))

# for _, i in data.iterrows():
#     print(len(i["Орж ирсэн огноо"]), i["Орж ирсэн огноо"])
#     cursor.execute(f'insert into cars (id, mark, model, color, class, motor, forWhat, type, position, madeDate, enterDate, country) values ({i["ТХ id"]},"{i["Марк"]}","{i["Модель"]}","{i["Өнгө"]}","{i["Ангилал"]}",{i["Хөдөлгүүрийн багтаамж"]},"{i["Зориулалт"]}","{i["Тээврийн хэрэгслийн төрөл"]}","{i["Хүрдний байрлал"]}","{i["Үйлдвэрлэсэн он"]}","{i["Орж ирсэн огноо"]}","{i["Үйлдвэрлэсэн улс"]}")')
print("start Insert")
sql = """
    INSERT INTO cars (id, mark, model, color, class, motor, forWhat, type, position, madeDate, enterDate, country)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(sql, data_to_insert)
db.commit()
cursor.execute("select * from cars;")
d = cursor.fetchall()

print(d)