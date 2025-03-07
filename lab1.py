import pandas
import math
import json

# data = pandas.read_csv("data.csv").astype(str)
nData = pandas.read_csv("dataC.csv").astype(str)
data = nData[["Зориулалт","Үйлдвэрлэсэн он", "Тээврийн хэрэгслийн төрөл", "Үйлдвэрлэсэн улс"]]
data['result'] = nData['Марк']
texts = []
for i in data:
    texts.append(data[i].unique().tolist())

# print(texts)

headers = list(data.columns.values)
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
    

def CalculateTotal(table):
    result = table["result"]
    answer = 0
    sets = result.value_counts(normalize=True)
    for i in sets:
        answer += -i * math.log2(i)
    return answer

totalEntropy = CalculateTotal(data)

def CalculateGain(table, name):
    result = 0
    totalLength = len(table)
    for i in range(table[name].max()+1):
        newData = table.loc[table[name] == i]
        currentLength = len(newData)
        entro = CalculateTotal(newData)
        result +=  entro * (currentLength / totalLength)
    tE = CalculateTotal(table)
    return tE - result
        
def GetValues(table):
    value = table.value_counts(normalize=True).idxmax()[0]

    return texts[-1][value]

def GetMaxGain(table):
    headers = list(table.columns.values)
    headers.remove("result")
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
        if i in table[maxGain].values:
            newTable = table.loc[table[maxGain] == i].drop([maxGain], axis=1)
            if(newTable["result"].nunique() == 1):
                results.append({GetText(maxGain,i):texts[-1][newTable["result"].iloc[0]]})
            else:
                if(len(list(newTable.keys())) == 1):
                    results.append({GetText(maxGain,i):GetValues(newTable)})
                    # print(newTable.value_counts(normalize=True))
                else:
                    results.append({GetText(maxGain,i):StartCalculate(newTable)})
    return {maxGain:results}



def Start(findDatas):
    answer = StartCalculate(data)
    def Check(json, headers):
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

    result = Check(answer, list(data.columns.values))
    return result, PrintJSON(answer)

if __name__ == "__main__":

    print("total entropy = ", totalEntropy)
    answer = StartCalculate(data)
    file = open("file.json", "w",encoding="utf-8")
    file.write(str(json.dumps(answer, ensure_ascii=False)))

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
                print(next_prefix + sub_connector + (j_key))
                if j[j_key] in texts[-1]:
                    print(next_prefix  + "    " + "└── " + j[j_key]) 
                else:
                    PrintJSON(j[j_key], next_prefix + ("    " if is_last_j else "│   "))
    
    PrintJSON(answer, "")