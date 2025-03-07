import pandas 
df = pandas.read_csv('ori.csv')
df = df[df['Үйлдвэрлэсэн он'] >= 1950]
df = df[df['Үйлдвэрлэсэн он'] <= 2024]
df.to_csv('dataC.csv', index=False)