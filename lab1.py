import pandas
import math

data = pandas.read_csv("data.csv")

texts = [
    ["sunny", "cloudy", "rain"],
    ["hot", "medium", "cold"],
    ["high", "normal"],
    ["weak", "force"],
    ["no", "yes"]
]

findDatas = ["sunny", "medium", "high", "force"]

def GetText(name, index):
    return texts[list(data.columns.values).index(name)][index]

def GetTextJson(index):
    row = texts[index]
    json = {}
    for i in range(len(row)):
        json[row[i]] = i
    return json

index = 0
for i in data:
    data[i] = data[i].map(GetTextJson(index))
    index+=1
def CalculateEntropy(p, n):
    total = p + n
    if(p == 0 or n == 0):
        return 0
    return (-p / total * math.log2(p/total)) - (n/total * math.log2(n/total)) 

def CalculateTotal(table):
    result = table["play"]
    total = len(result)
    p = result.sum()
    n = total - p
    return CalculateEntropy(p, n)

totalEntropy = CalculateTotal(data)

def CalculateGain(table, name):
    result = 0
    totalLength = len(table)
    for i in range(table[name].max()+1):
        newData = table.loc[table[name] == i]
        currentLength = len(newData)
        p = newData["play"].sum()
        n = currentLength - p
        entro = CalculateEntropy(p, n)
        #print(name, entro)
        result +=  entro * (currentLength / totalLength)
    tE = CalculateTotal(table)
    #print(result, tE - result, tE)
    return tE - result
        
def GetMaxGain(table):
    headers = list(table.columns.values)
    headers.remove("play")

    entropies = []
    for i in headers:
        entropies.append(CalculateGain(table, i))
    maxValue = max(entropies)
    index = entropies.index(maxValue)
    return headers[index]

def StartCalculate(table):
    maxGain = GetMaxGain(table)
    results = []
    for i in range(table[maxGain].max()+1):
        newTable = table.loc[table[maxGain] == i].drop([maxGain], axis=1)
        if(newTable["play"].sum() == len(newTable)):
            results.append({GetText(maxGain,i):"YES"})
        elif(newTable["play"].sum() == 0):
            results.append({GetText(maxGain,i):"NO"})
        else:
            results.append({GetText(maxGain,i):StartCalculate(newTable)})
    return {maxGain:results}

print("total entropy = ", totalEntropy)

answer = StartCalculate(data)

# file = open("file.json", "w")
# file.write(str(answer))

def PrintJSON(data, prefix=""):
    keys = list(data.keys())
    for idx, key in enumerate(keys):
        is_last = (idx == len(keys) - 1)
        connector = "└── " if is_last else "├── "

        print(prefix + connector + key)

        next_prefix = prefix + ("    " if is_last else "│   ")
        for j_idx, j in enumerate(data[key]):
            j_key = list(j.keys())[0]
            is_last_j = (j_idx == len(data[key]) - 1)
            sub_connector = "└── " if is_last_j else "├── "
            print(next_prefix + sub_connector + j_key)
            if j[j_key] == "YES" or j[j_key] == "NO":
                print(next_prefix  + "    " + "└── " + j[j_key]) 
            else:
                PrintJSON(j[j_key], next_prefix + ("    " if is_last_j else "│   "))
PrintJSON(answer, "")



def Check(json, headers):
    c = (list(json.keys()))[0]
    value = findDatas[headers.index(c)]
    d = json[c]
    data = []
    for i in d:
        data.append((list(i.keys()))[0])
    headers.remove(c)
    findDatas.remove(value)
    nextData = d[data.index(value)][value]
    if(nextData == "YES" or nextData == "NO"):
        return nextData
    return Check(nextData, headers)

print("find =", findDatas)
result = Check(answer, list(data.columns.values))
print(result)
