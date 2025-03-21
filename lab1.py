import math
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

def GetText(name, index):
    return texts[headers.index(name)][index]

def GetTextJson(index):
    row = texts[index]
    json = {}
    for i in range(len(row)):
        json[row[i]] = i
    return json

def CalculateTotal(where=[]):
    answer = 0
    w = ""
    if(len(where) != 0):
        w = "where " + " and ".join(where)
    cur.execute(f"select {headers[-1]}, count(*) / sum(count(*)) over() from {tableName} {w} group by {headers[-1]};")
    res = cur.fetchall()
    # sets = result.value_counts(normalize=True)
    sets = [0]*len(texts[-1])
    for i in res:
        sets[texts[-1].index(i[0])] = float(i[1])
    for i in sets:
        if(i == 0):
            continue
        answer += -i * math.log2(i)
    return answer

totalEntropy = CalculateTotal()

def GetLength(where):
    w = ""
    if(len(where) != 0):
        w = "where " + " and ".join(where)
    cur.execute(f"select count(*) from {tableName} {w}")
    return cur.fetchall()[0][0]


def CalculateGain(name, where=[]):
    result = 0
    w = ""
    if(len(where) != 0):
        w = "where " + " and ".join(where)
    
    totalLength = GetLength(where)
    cur.execute(f"select distinct {name} from {tableName} {w}")
    maxValue = len(cur.fetchall())
    for i in range(maxValue):
        newWhere = where.copy()
        newWhere.append(f'{name} = "{texts[headers.index(name)][i]}"')

        currentLength = GetLength(newWhere)
        entro = CalculateTotal(newWhere)
        result +=  entro * (currentLength / totalLength)
    tE = CalculateTotal(where)
    return tE - result
        
def GetValues(where):
    w = ""
    if(len(where) >0):
        w = "where " + " and ".join(where)
    cur.execute(f"select {headers[-1]} from {tableName} {w} group by {headers[-1]} ORDER BY count({headers[-1]}) desc")
    a = cur.fetchall()
    return a[0][0]

def GetMaxGain(head,where=[]):
    newHeaders = head.copy()
    newHeaders.remove("result")
    entropies = []
    
    for i in newHeaders:
        entropies.append(CalculateGain(i,where))
    maxValue = max(entropies)
    index = entropies.index(maxValue)
    return newHeaders[index]

def StartCalculate(head,where=[], dropped=0):
    maxGain = GetMaxGain(head,where)
    results = []
    w = ""
    if(len(where) != 0):
        w = "where " + " and ".join(where)
    cur.execute(f"select distinct {maxGain} from {tableName}")
    size = cur.fetchall()
    size = len(size)
    # print(range(size), maxGain)
    for i in range(size):
        if i < len(texts[headers.index(maxGain)]):
            # newTable = table.loc[table[maxGain] == i].drop([maxGain], axis=1)
            h = head.copy()
            # print(h, head)
            h.remove(maxGain)
            dropped+=1
            newWhere = where.copy()
            newWhere.append(f'{maxGain} = "{GetText(maxGain,i)}"')
            cur.execute(f"select count(distinct result) from {tableName} where {' and '.join(newWhere)}")
            r = cur.fetchall()[0][0]
            if(r == 1):
                cur.execute(f"select result from {tableName} where {' and '.join(newWhere)}")
                res = cur.fetchall()[0][0]
                results.append({GetText(maxGain,i):res})
            else:
                if(len(headers)==1):
                    results.append({GetText(maxGain,i):GetValues(newWhere)})
                else:
                    results.append({GetText(maxGain,i):StartCalculate(h,newWhere, dropped)})
    return {maxGain:results}

answer = StartCalculate(headers)
def Start(findDatas):
    def Check(json, headers):
        headers = headers.copy()
        c = (list(json.keys()))[0]
        value = findDatas[headers.index(c)]
        d = json[c]
        data = []
        for i in d:
            data.append((list(i.keys()))[0])
        headers.remove(c)
        findDatas.remove(value)
        if(value not in data):
            return "Error"
        nextData = d[data.index(value)][value]
        if(nextData in texts[-1]):
            return nextData
        return Check(nextData, headers)
    def PrintJSON(data, prefix=""):
        result = []
        keys = list(data.keys())
        for idx, key in enumerate(keys):
            is_last = (idx == len(keys) - 1)
            connector = "└── " if is_last else "├── "
            result.append(prefix + connector + key)
            next_prefix = prefix + ("    " if is_last else "│   ")
            for j_idx, j in enumerate(data[key]):
                j_key = list(j.keys())[0]
                is_last_j = (j_idx == len(data[key]) - 1)
                sub_connector = "└── " if is_last_j else "├── "
                result.append(next_prefix + sub_connector + j_key)
                if j[j_key] in texts[-1]:
                    result.append(next_prefix + "    " + "└── " + j[j_key])
                else:
                    result.append(PrintJSON(j[j_key], next_prefix + ("    " if is_last_j else "│   ")))
        return "\n".join(result)

    result = Check(answer, headers)
    return result, PrintJSON(answer)

# if __name__ == "__main__":

#     print("total entropy = ", totalEntropy)
#     answer = StartCalculate(data)
#     file = open("file.json", "w",encoding="utf-8")
#     file.write(str(json.dumps(answer, ensure_ascii=False)))

#     def PrintJSON(data, prefix=""):
#         keys = list(data.keys())
#         for idx, key in enumerate(keys):
#             is_last = (idx == len(keys) - 1)
#             connector = "└── " if is_last else "├── "
#             print(prefix + connector + key)
#             next_prefix = prefix + ("    " if is_last else "│   ")
#             for j_idx, j in enumerate(data[key]):
#                 j_key = list(j.keys())[0]
#                 is_last_j = (j_idx == len(data[key]) - 1)
#                 sub_connector = "└── " if is_last_j else "├── "
#                 print(next_prefix + sub_connector + (j_key))
#                 if j[j_key] in texts[-1]:
#                     print(next_prefix  + "    " + "└── " + j[j_key]) 
#                 else:
#                     PrintJSON(j[j_key], next_prefix + ("    " if is_last_j else "│   "))
    
#     PrintJSON(answer, "")