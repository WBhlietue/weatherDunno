import pandas

# data = pandas.read_csv("data.csv").astype(str)
nData = pandas.read_csv("dataC.csv").astype(str)
data = nData[["Зориулалт","Үйлдвэрлэсэн он", "Тээврийн хэрэгслийн төрөл", "Үйлдвэрлэсэн улс"]]
data['result'] = nData['Марк']
texts = []
for i in data:
    texts.append(data[i].unique().tolist())

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

heads = list(data.columns.values)

def GetRate(table, row, num, result):
    newTable = table.loc[table["result"] == result]
    newTable2 = newTable.loc[newTable[heads[row]] == num]
    return len(newTable2) / len(newTable)

def GetResultRate(res):
    newTable = data.loc[data["result"] == res]
    return len(newTable) / len(data)

def Start(findDatas):
    findDatas = [texts[0].index(findDatas[0]),texts[1].index(findDatas[1]),texts[2].index(findDatas[2]),texts[3].index(findDatas[3])]
    result = data["result"].unique()
    rates = []
    for i in result:
        rates.append((texts[-1][i], GetResultRate(i)))

    for i in range(len(findDatas)):
        for j in range(len(rates)):
            rates[j] = (rates[j][0], rates[j][1] * GetRate(data, i, findDatas[i], j))

    dataFrame = pandas.DataFrame(rates, columns=["result", "rate"])
    max_rate_row = dataFrame.loc[dataFrame['rate'].idxmax()]
    max_result = max_rate_row['result']
    strs = []
    sum = 0
    for i in rates:
        sum += i[1]
    if(sum == 0):
        return "Error", ""
    for i in rates:
        strs.append(f"{i[0]:<22}:{i[1]/sum:<15.10}")
    return max_result, "\n".join(strs)
if __name__ == "__main__":
    Start(["Суудал", "1994", "Туулах чадвар сайтай", "Япон"])