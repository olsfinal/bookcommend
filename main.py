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
    ISBN=request.args.get('ISBN')
    # print(1)
    print(ISBN)
    results=[]
    detail = books[ISBN]
    print(detail)
    book_author = detail[1]
    book_title = detail[0]
    publisher = detail[3]
    year = detail[2]
    img=detail[6]
    # book_rating_user = userData[name][ISBN]
    if name!=None:
        if ISBN not in userData[name]:
            book_rating_user=0
        else:
            book_rating_user = userData[name][ISBN]
    else:
        book_rating_user=0
    # items = books[ISBN]
    # book_rating_all = float(sum(items.values())) / len(items)
    if books[ISBN]==None:
        book_rating_all=0
    else:
        items = bookData[ISBN]
        book_rating_all = round(float(sum(items.values())) / len(items),2)
    book_detail = {'ISBN': id, 'author': book_author, 'name': book_title, 'publisher': publisher,
                   'year': year, 'img': img}
    # print(book_detail)
    results.append(book_detail)
    return render_template('introduction.html', name=name,results=results,book_rating_user=book_rating_user,book_rating_all=book_rating_all)

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
        # print(hot_recommendations)
        if hot_recommendations != None:
            for i in range(len(hot_recommendations)):
                try:
                    id = hot_recommendations[i][0]
                    # print(id)
                    detail = books[id]
                    book_author = detail[1]
                    book_title = detail[0]
                    publisher = detail[3]
                    year = detail[2]
                    img = detail[6]
                    book_detail = {'ISBN': id, 'author': book_author, 'name': book_title, 'publisher': publisher,
                                   'year': year, 'img': img}
                    # print(book_detail)
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
                # print(i)
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
    return render_template('advancedshow.html',results=results)


@app.route('/searchhistory', methods=['GET'])
def searchhistory():
    if 'SearchHistory' in session:
        pass
    else:
        session['SearchHistory'] = ''
    if request.method == 'GET':
        if 'username' in session:
            userHistory = userData['username']
            results=[]
            print(userHistory)
            for i in userHistory:
                results.append({'ISBN':i,'rating':userHistory[i]})
            return render_template('searchhistory.html', results=results)
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
            print(session['username'])
            userHistory = userData[session['username']]
            results=[]
            # print(userHistory)
            for i in userHistory:
                # print(books[i])
                try:
                    bookTitle=books[i][0]
                    results.append({'ISBN':i,'title':bookTitle,'rating':userHistory[i]})
                except:
                    continue
            return render_template('songhistory.html', results=results)
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
