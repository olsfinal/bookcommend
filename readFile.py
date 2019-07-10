import pandas as pd
import matplotlib.pyplot as plt

# 将文件转换为字典便于读取，读取User和Book
def getItem(filename):
    # BX-Users BX-Books
    # f=open(filename,"rb")
    with open(filename,'rb') as f:
        lines=str(f.read())
        # 行分隔符为\r\n ,同时去除多余的"
        lines=lines.replace(r'"',"").replace(r'\r','').split(r'\n')
        # 返回内容，key为
        items={}
        for line in lines[1:len(lines)-1]:
            try:
                item=line.split(";")
                if filename=='BX-Users.csv':
                    numItem=2
                elif filename=='BX-Books.csv':
                    numItem=3
                else:
                    break
                if item[numItem] == 'NULL':
                    item[numItem] = None
                else:
                    item[numItem] = eval(item[numItem])
                items[item[0]]=item[1:]
            except:
                continue
        # for i in items:
        #     print(items[i])
        return items

def getRating():
    # filename='ratings.csv'
    # f = open(filename, "rb")
    with open('ratings.csv','rb') as f:
        lines = str(f.read())
        # 行分隔符为\r\n
        lines = lines.replace(r'\r','').split(r'\n')
        # 返回内容，key为
        users = {}
        books = {}
        for line in lines[1:len(lines) - 1]:
            item = line.split(";")
            # 存储为user-rating和book-rating的两张字典
            if item[0] not in users:
                users[item[0]] = {item[1]:eval(item[2])}
            else:
                users[item[0]][item[1]]=eval(item[2])
            if item[1] not in books:
                books[item[1]] = {item[0]:eval(item[2])}
            else:
                books[item[1]][item[0]]=eval(item[2])
        # for i in users:
        #     print(i,users[i])
        # for j in count:
        #     print(j)
        # print(count)
        return users,books

# 统计分布
def countKeys(dic):
    count = {}
    for i in dic:
        # print(users[i])
        c = len(dic[i])
        # print(c)
        if c not in count:
            count[c] = 1
        else:
            count[c] += 1
    keys = count.keys()
    keys = sorted(keys,reverse=True)
    for i in keys:
        print(i, count[i])
    # df=pd.DataFrame(count,index=[0])
    # df.plot(kind='bar')
    # plt.show()


# book=getItem("BX-Books.csv")
# print(book)
# users,books=getRating()
# print(users)
# countKeys(books)
