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

totalLength = GetLength([])

def GetText(name, index):
    return texts[headers.index(name)][index]

def GetTextJson(index):
    row = texts[index]
    json = {}
    for i in range(len(row)):
        json[row[i]] = i
    return json

def GetRate(row, num, result):
    cur.execute(f'select count(*) from {tableName} where {headers[-1]} = "{texts[-1][result]}"')
    newTable = cur.fetchall()[0][0]
    cur.execute(f'select count(*) from {tableName} where {headers[row]} = "{texts[row][num]}" and {headers[-1]} = "{texts[-1][result]}"')
    newTable2 = cur.fetchall()[0][0]
    return newTable2 / newTable

def GetResultRate(res):
    cur.execute(f'select count(*) from {tableName} where {headers[-1]} = "{texts[-1][res]}"')
    newTable = cur.fetchall()[0][0]
    return newTable / totalLength

def Start(findDatas):
    findDatas = [texts[0].index(findDatas[0]),texts[1].index(findDatas[1]),texts[2].index(findDatas[2]),texts[3].index(findDatas[3])]
    cur.execute(f'select distinct {headers[-1]} from {tableName}')
    result = [texts[-1].index(i[0]) for i in cur.fetchall()]
    rates = []
    for i in result:
        rates.append((texts[-1][i], GetResultRate(i)))

    for i in range(len(findDatas)):
        for j in range(len(rates)):
            rates[j] = (rates[j][0], rates[j][1] * GetRate(i, findDatas[i], j))
    print(rates)
    rates = sorted(rates, key=lambda x: x[1], reverse=True)
    max_result = rates[0][0]
    strs = []
    sum = 0
    for i in rates:
        sum += i[1]
    if(sum == 0):
        return "Error", ""
    for i in rates:
        strs.append(f"{i[0]:<22}:{i[1]/sum:<15.10}")
    return max_result, "\n".join(strs)

print(Start(["sunny", "hot","high", "force"]))