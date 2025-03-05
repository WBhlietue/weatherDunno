import pandas

data = pandas.read_csv("data.csv")


texts = [
    ["sunny", "cloudy", "rain"],
    ["hot", "medium", "cold"],
    ["high", "normal"],
    ["weak", "force"],
    ["no", "yes"]
]

findDatas = ["rain", "hot", "high", "weak"]
findDatas = ["sunny", "cold", "high", "force"]

findDatas = [texts[0].index(findDatas[0]),texts[1].index(findDatas[1]),texts[2].index(findDatas[2]),texts[3].index(findDatas[3])]

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
    newTable = table.loc[table["play"] == result]
    newTable2 = newTable.loc[newTable[heads[row]] == num]
    return len(newTable2) / len(newTable)

def GetResultRate(res):
    newTable = data.loc[data["play"] == res]
    return len(newTable) / len(data)

yesRate = GetResultRate(1)
noRate = GetResultRate(0)

for i in range(len(findDatas)):
    yesRate *= GetRate(data, i, findDatas[i], 1)
    noRate *= GetRate(data, i, findDatas[i], 0)

print("yes:", yesRate)
print(" no:", noRate)

if(yesRate > noRate):
    print("YES")
else:
    print("NO")