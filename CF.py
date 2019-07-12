import readFile
import copy
from math import *

userData,bookData=readFile.getRating()

def Euclidean(item1, item2,items):
    # 取出两位用户评论过的电影和评分
    item1_data = items[item1]
    item2_data = items[item2]
    distance = 0
    # 找到两位用户都评论过的电影，并计算欧式距离
    for key in item1_data.keys():
        if key in item2_data.keys():
            # 注意，distance越小表示两者越相似
            distance += pow(float(item1_data[key]) - float(item2_data[key]), 2)
    return 1/(1+sqrt(distance))#这里返回值越大，相似度越大

def normalization(data):
    data_copy=copy.deepcopy(data)
    for key in data_copy:
        items=data_copy[key]
        # print(items)
        avg=float(sum(items.values()))/len(items)
        for i in items:
            items[i]-=avg
    return data_copy

def vectorModule(item_data):
    module=0
    for i in item_data:
        module+=float(item_data[i])**2
    return sqrt(module)

def cosinDistance(item1,item2,items):
    item1_data = items[item1]
    item2_data = items[item2]
    distance = 0
    for key in item1_data.keys():
        if key in item2_data.keys():
            distance += float(item1_data[key])*float(item2_data[key])
    if (vectorModule(item1_data)*vectorModule(item2_data))==0:
        return 0
    else:
        return distance/(vectorModule(item1_data)*vectorModule(item2_data))

#计算某个用户与其他用户的相似度
def topn_similar(itemID, data, n=10):
    data_copy=normalization(data)
    res = []
    for itemid in data.keys():
        #排除与自己计算相似度
        if not itemid == itemID:
            # simliar = Euclidean(itemID,itemid,data)
            similar=cosinDistance(itemID,itemid,data_copy)
            res.append((itemid,similar))
    res.sort(key=lambda val:val[1],reverse=True)
    # print(res)
    return res[:n]


# 根据用户推荐电影给其他人
def CFRecommend(user, data,n=10):
    # 相似度最高的用户
    items={}
    if user not in data:
        return 0
    for i in range(5):
        items.update(data[topn_similar(user, data)[i][0]])
    # print(top_sim_user)
    # 相似度最高的用户的观影记录
    # items = data[top_sim_user]
    # print(items)
    recommendations = []
    # 筛选出该用户未观看的电影并添加到列表中
    for item in items.keys():
        if item not in data[user].keys() and items[item]>=5:
            recommendations.append((item, items[item]))
    if recommendations==[]:
        return 0
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    # 返回评分最高的10部电影
    return recommendations[:n]

def subset(bookData,userData,ISBN):
    bookRating=bookData[ISBN]
    users=[i for i in bookRating.keys()]
    userSubset={}
    for i in users:
        userSubset[i]=userData[i]
    # print(userSubset)
    return userSubset


def mostRecommend(data,n=10):
    avg_data=[]
    for key in data:
        items=data[key]
        avg = float(sum(items.values())) / len(items)
        # 筛选均分大于5的项
        if avg>=5 and len(items)>5:
            avg_data.append((key,avg))
    avg_data.sort(key=lambda val: val[1], reverse=True)
    return avg_data[:n]


userSubset=subset(bookData,userData,'0671025864')
Recommendations = CFRecommend('262940', userSubset,n=1)
print(Recommendations)

# RES = topn_similar('265889',userData)
# print(RES)

# print(userData)
# rcm=mostRecommend(bookData)
# print(rcm)

# CFRating('262940',userData,'189317302X')

# subset(bookData,'0671025864',userData)
# print(subset(books,'0671025864'))