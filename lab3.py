import server
# data = pandas.read_csv("data.csv").astype(str)
# nData = pandas.read_csv("dataC.csv").astype(str)
# data = nData[["Зориулалт","Үйлдвэрлэсэн он", "Тээврийн хэрэгслийн төрөл", "Үйлдвэрлэсэн улс"]]
# data['result'] = nData['Марк']

db = server.db
cur = db.cursor()
headers = server.headers
tableName = server.tableName
texts = []

for i in headers:
    cur.execute(f"select distinct {i} from weather;")
    a = cur.fetchall()
    p = []
    for j in a:
        p.append(j[0])
    texts.append(p)
def GetLength(where):
    w = ""
    if(len(where) != 0):
        w = "where " + " and ".join(where)
    cur.execute(f"select count(*) from {tableName} {w}")
    return cur.fetchall()[0][0]

def IsSame(row, line):
    for i in range(len(line)):

        if row[i] != line[i]:
            return False
    return True

def GetText(name, index):
    return texts[headers.index(name)][index]

def CalculateSupport(line):
    countTotal = 0
    cur.execute(f'select distinct {headers[-1]} from {tableName}')
    resultCount = len(cur.fetchall())
    count = [0] * resultCount
    cur.execute(f'select {", ".join(headers)} from {tableName}')
    for row in cur.fetchall():
        if(IsSame(row, line)):
            count[row["result"]]+=1
            countTotal+=1
    # print(count)
    return (count, countTotal+0.0001)
        

def Start(findDatas):
    count, countTotal = CalculateSupport(findDatas)
    answer = []
    for i in range(len(count)):
        answer.append((GetText("result", i), count[i]/countTotal))
    answer = sorted(answer, key=lambda x: x[1], reverse=True)
    return answer
    
if __name__ == "__main__":
    print(Start(["sunny","medium","normal","force"]))
    # print(data)