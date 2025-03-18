import pandas


data = pandas.read_csv("data.csv").astype(str)
# nData = pandas.read_csv("dataC.csv").astype(str)
# data = nData[["Зориулалт","Үйлдвэрлэсэн он", "Тээврийн хэрэгслийн төрөл", "Үйлдвэрлэсэн улс"]]
# data['result'] = nData['Марк']
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

def IsSame(row, line):
    for i in range(len(line)):

        if row[i] != line[i]:
            return False
    return True

def CalculateSupport(line):
    countTotal = 0
    resultCount = len(data["result"].unique().tolist())
    count = [0] * resultCount
    for _, row in data.iterrows():
        if(IsSame(row, line)):
            count[row["result"]]+=1
            countTotal+=1
    # print(count)
    return (count, countTotal+0.0001)
        

def Start(findDatas):
    count, countTotal = CalculateSupport(findDatas)
    answer = []
    for i in range(len(count)):
        # print(count[i]/countTotal, count[i], countTotal)
        answer.append((GetText("result", i), count[i]/countTotal))
    answer = sorted(answer, key=lambda x: x[1], reverse=True)
    return answer
    
if __name__ == "__main__":
    print(Start([0, 0, 0, 0]))