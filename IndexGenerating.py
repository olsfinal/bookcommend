# coding=utf-8
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
# # from get_comment import SQL
from whoosh.sorting import FieldFacet
import csv
import readFile

# dirpath="searchweb/"
# index_filepath=dirpath+"index/"
# source_filepath=index_filepath+"0407_songs_dr2.csv"
readFile.getItem("BX-Books.csv")
# analyser = ChineseAnalyzer()  # 导入中文分词工具
schema = Schema(ISBN=TEXT(stored=True,sortable=True),
                book_title=TEXT(stored=True,sortable=True),
                book_author=TEXT(stored=True,sortable=True),
                year=TEXT(stored=True,sortable=True),
                publisher=TEXT(stored=True,sortable=True))  # 创建索引结构ix = create_in("/home/jack/manage.py", schema=schema, indexname='indexname') #path 为索引创建的地址，indexname为索引名称
ix = create_in("./index/", schema=schema, indexname='book')  # path 为索引创建的地址，indexname为索引名称
writer = ix.writer()
f=readFile.getItem("BX-Books.csv")
flag = 0
for key in f:
    if flag==0:
        flag+=1
        pass
    else:
        writer.add_document(ISBN=key, book_title=f[key][0], book_author=f[key][1], year=str(f[key][2]), publisher=f[key][3])
writer.commit()
print("建立完成一个索引")