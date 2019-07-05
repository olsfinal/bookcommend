import chardet
f=open('BX-Users.csv','rb')
data=f.readline()
print(chardet.detect(data))

# f=open('BX-Users.csv','rb')
#
# lines=str(f.readlines())
# print(lines.split(',')[:10])
# data=[]
# for line in lines:
#     data.append(line.split(';'))
# print(data[:10])
import pandas
test=pandas.read_csv("BX-Users.csv",sep=";",encoding="ascii")
lines=str(test.readlines())
print(lines.split(',')[:10])