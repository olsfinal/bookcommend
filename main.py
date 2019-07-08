from flask import Flask, render_template, request, session, redirect, url_for, make_response
from search import *
from readFile import *
from CF import *

app = Flask(__name__)
books=getItem('BX-Books.csv')
users=getItem('BX-Users.csv')
userData,bookData=readFile.getRating()

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # if (request.form['Username'] == "obama" or request.form['Username'] == "admin"):
        #     session['username'] = request.form['Username']
        #     return redirect(url_for('index'))
        # else:
        #     error = 'Invalid username/password'
        #     return render_template('error.html', error=error)
        session['username'] = request.form['Username']
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html')
    return render_template('error.html', error=error)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/cleansearchhistory')
def cleansearchhistory():
    session.pop('SearchHistory', None)
    return redirect(url_for('index'))


@app.route('/cleansonghistory')
def cleansonghistory():
    session.pop('SongHistory', None)
    return redirect(url_for('index'))


@app.route('/error')
def error():
    return render_template('error.html', error='Something wrong')


@app.route('/introduction', methods=['POST', 'GET'])
def introcution():
    if 'username' in session:
        name = session['username']
    else:
        name = None
    if request.method == 'GET':
        return render_template('pagenotfound.html')
    elif request.method == 'POST':
        value = request.form['Name']
        # value为点击的值，value于数据库中进行查询比较,返回为results
        results = [
            {
                'img': '/static/img/zhangyu.jpg',
                'name': '张宇18讲',
                'description': '【现货正版】张宇2020考研数学一 高数18讲+线代9讲+概率论9讲+1000题(5册)张宇高数十八讲1000题数一张宇36讲可搭汤家凤1800',
                'details': '这本书，首先是题源，说白了，就是命题的源泉.建设好这个源泉，是这本书的指导思想.源头建设是极其不容易的，绝不是东拼西凑几个题目那样简单，众多命题专家和教学专家多年的经验和无私的奉献，才成就了这本书的高质量.很欣慰地看到，上一个考研年，本书不仅对2017的考研数学试题做出了的预测，而且还对考生参加**、各省市大学生数学竞赛，校内的期中、期末考试，都起到了积极的作用，甚至还有原题出现在各种形式的考试试卷上.这本书，又是习题集.考研数学复习，要辅以足量的习题训练，这是本书的目标与任务.这本书，还是**书.**有众多考生选择这本习题集，让本书作者倍感责任重大.这一版，仍然做了认真修改：增加、替换了一些要紧的题目，以适应新一年的命题趋势；',
                'grades': '4.9'
            }
        ]
        print(value)
        return render_template('introduction.html',name=name, results=results)


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        name = session['username']
    else:
        name = None
    if request.method == 'GET':
        # 用户储存在name中
        hots=[]
        hot_recommendations = mostRecommend(bookData, n=12)
        if hot_recommendations != None:
            for i in range(len(hot_recommendations)):
                try:
                    id = hot_recommendations[i][0]
                    print(id)
                    detail = books[id]
                    book_author = detail[1]
                    book_title = detail[0]
                    publisher = detail[3]
                    year = detail[2]
                    img = detail[6]
                    book_detail = {'ISBN': id, 'author': book_author, 'name': book_title, 'publisher': publisher,
                                   'year': year, 'img': img}
                    print(book_detail)
                    hots.append(book_detail)
                except:
                    continue
        recommends=[]
        if name!=None:
            recommendations = CFRecommend(name, userData,n=12)
            if recommendations!=None:
                for i in range(len(recommendations)):
                    try:
                        id = recommendations[i][0]
                        detail = books[id]
                        book_author = detail[1]
                        book_title = detail[0]
                        publisher = detail[3]
                        year = detail[2]
                        img=detail[6]
                        book_detail = {'ISBN': id, 'author': book_author, 'name': book_title, 'publisher': publisher,
                                       'year': year, 'img':img }
                        recommends.append(book_detail)
                    except:
                        continue
        return render_template('index.html', name=name, hots=hots, recommends=recommends)


@app.route('/advancedsearchweb', methods=['GET'])
def advancedsearchweb():
    if 'username' in session:
        name = session['username']
    else:
        name = None
    if request.method == 'GET':
        return render_template('AdvancedSearchWeb.html', name=name)
        # elif request.method == 'POST':
        #     str = request.values.to_dict() #input可能会有空输入，只能这样获取
        #     if 'SearchHistory' in session:
        #         value = list(session['SearchHistory'])
        #     else:
        #         value = []
        #     value.append(str)   ##STR需要处理
        #     print(value)
        #     key = {'SearchHistory': value}
        #     session.update(key)
        #     print(session)
        #     print(str.values())
        #
        #     #搜索处理
        #
        #     results =[
        #     {
        #         'songname': 'In my life',
        #         'description': 'LaLaLa',
        #         'singer': 'Beatles',
        #         'album': 'Only One',
        #         'lyrics': 'in my life love them all'
        #     },
        #     {
        #         'songname': 'Photograph',
        #         'description': 'Ed sheeran\'s song',
        #         'singer': 'Ed sheeran',
        #         'album': 'X',
        #         'lyrics': 'Loving can hurt, loving can hurt sometimes'
        #     }
        # ]
        # return render_template('advancedshow.html', results=results)


@app.route('/basicshow', methods=['GET', 'POST'])
def basicshow():
    if 'username' in session:
        name = session['username']
    else:
        name = None
    if request.method == 'GET':
        return render_template('pagenotfound.html')
    elif request.method == 'POST':
        value = request.form['InputKeyWord']
        # results存放搜索结果
        result_set=do_searching(value)
        # print(result_set)
        results=[]
        for key in result_set:
            for i in result_set[key]:
                # print(result_set[key][i])
                print(i)
                try:
                    detail=result_set[key][i]
                    id=detail['ISBN']
                    book_author=detail['book_author']
                    book_title=detail['book_title']
                    publisher=detail['publisher']
                    year=detail['year']
                    # , 'name': book_title, 'author': book_author, 'publisher': publisher, 'year': year, 'img': \
                    # books[key][6]
                    book_detail={'ISBN':id,'author':book_author,'name':book_title,'publisher':publisher,'year':year,'img':books[id][6]}
                    # print(book_detail)
                    results.append(book_detail)
                except:
                    # print(book_title)
                    continue
        # print(results)
        return render_template('basicshow.html', name=name,results=results)



@app.route('/star', methods=['POST'])
def star():
    if request.method == 'POST':
        value = request.form['Rank']
        print(value)
        #数据库处理部分
        return ''


@app.route('/advancedshow', methods=['GET', 'POST'])
def advancedshow():
    if request.method == 'GET':
        return render_template('pagenotfound.html')
    elif request.method == 'POST':
        # str = request.values.to_dict()
        str = request.values.to_dict()
        # print(str)
        # print(list(str))
        results = []
        if 'Sort' in str:
            key = session['SearchHistory']  # 获取搜索记录
            sort = str['Sort']
            if sort == '1':  # 重新排序代码
                print(sort)
            elif sort == '2':
                print(sort)
            elif sort == '3':
                print(sort)
            elif sort == '4':
                print(sort)
            return render_template('advancedshow.html', results=results)

        if 'SearchHistory' in session:
            value = list(session['SearchHistory'])
        else:
            value = []
        value.append(str)  ##STR需要处理
        # print(value)
        key = {'SearchHistory': value}
        session.update(key)
        # print(session)
        # print(str.values())

        # 搜索处理

        results = [
            {
                'songname': 'In my life',
                'description': 'LaLaLa',
                'singer': 'Beatles',
                'album': 'Only One',
                'lyrics': 'in my life love them all'
            },
            {
                'songname': 'Photograph',
                'description': 'Ed sheeran\'s song',
                'singer': 'Ed sheeran',
                'album': 'X',
                'lyrics': 'Loving can hurt, loving can hurt sometimes'
            }
        ]
    return render_template('advancedshow.html',name=name, results=results)


@app.route('/searchhistory', methods=['GET'])
def searchhistory():
    if 'SearchHistory' in session:
        pass
    else:
        session['SearchHistory'] = ''
    if request.method == 'GET':
        if 'username' in session:
            return render_template('searchhistory.html', results=session['SearchHistory'])
        else:
            return redirect(url_for('login'))


@app.route('/songhistory', methods=['GET', 'POST'])
def songhistory():
    if 'SongHistory' in session:
        pass
    else:
        session['SongHistory'] = ''
    if request.method == 'GET':
        if 'username' in session:
            return render_template('songhistory.html', results=session['SongHistory'])
        else:
            return redirect(url_for('login'))
    elif request.method == 'POST':
        value = []
        if 'SongHistory' in session:
            value = list(session['SongHistory'])
        value.append(request.form['Songname'])
        key = {'SongHistory': value}
        session.update(key)
        return make_response("正在播放")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pagenotfound.html'), 404


if __name__ == '__main__':
    # nav.init_app(app)
    app.run(debug=True)
