# coding=utf-8
from whoosh.qparser import QueryParser
from whoosh import qparser,sorting
from whoosh.index import open_dir
from whoosh.sorting import FieldFacet

index_filepath="./index/"
# source_filepath=index_filepath+"0407_songs_dr2.csv"
default_index = open_dir(index_filepath, indexname='book')  # 读取建立好的索引

# 默认排序为得分+album+song
default_facet = []
default_facet.append(sorting.ScoreFacet())
# default_facet.append(FieldFacet("album_title", reverse=True))  # 按序排列搜索结果
default_facet.append(FieldFacet("book_title", reverse=True))

# 默认查询为and模式，默认范围为全选
default_group=qparser.syntax.AndGroup
default_range=['book_title','book_author','year','publisher','ISBN']



# 基本的单曲查询
def basic_search(query,query_parse,group=default_group,facet=default_facet,index=default_index):
    searcher = index.searcher()
    parser = QueryParser(query_parse, index.schema,group=group)
    myquery = parser.parse(query)
    parser.remove_plugin_class(qparser.PhrasePlugin)
    parser.add_plugin(qparser.SequencePlugin())
    parser.add_plugin(qparser.FuzzyTermPlugin())
    results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    # print(results)
    return results

# 基本的循环查询，返回字典
def do_searching(query,search_range=default_range,group=default_group,index=default_index):
    # query:查询语句,search_range:搜索的范围
    result_dict = {}
    # 遍历搜索范围
    for qp in search_range:
        if index == default_index:
            results=basic_search(query,qp,group=group)
        else:
            results = basic_search(query, qp, group=group,index=index)
        # 建立song_id-detail的字典
        song_detail = {}
        # 遍历查询结果集
        for result in results:
            # print(result)
            return_dict=dict(result) # detail: {'album_title': 'xxx', 'song_author': 'xx', 'song_id': '123', 'song_lrc': '...
            song_detail[return_dict['ISBN']]=return_dict
        result_dict[qp]=song_detail
        # print(song_detail)
    # 返回的格式: {'search_range':{'song_id':'detail'}}
    return result_dict

# 普通查询，采用基本的and查询
def normal_searching(query,mode):
    if mode == 0:
        return do_searching(query)
    elif mode == 1:
        return do_searching(query,search_range=['book_title'])#
    elif mode == 2:
        return do_searching(query,search_range=['book_author'])#
    elif mode == 3:
        return do_searching(query,search_range=['year'])#
    elif mode == 4:
        return do_searching(query,search_range=['publisher'])#
    elif mode ==5:
        return do_searching(query,search_range=['ISBN'])
    else:
        pass


# 高级查询
def advanced_searching(and_query,or_query,search_range):
    if or_query == '' and and_query != None:
        or_query=and_query
    elif and_query == '' and or_query != None:
        and_query=or_query
    print(and_query,or_query,search_range)
    and_result = do_searching(query=and_query,search_range=search_range)
    or_result = do_searching(query=or_query,search_range=search_range,group=qparser.OrGroup)
    result = {}
    for qp in search_range:
        song_ids=list(and_result[qp].keys()&or_result[qp].keys())
        return_dict={}
        # print(song_ids)
        for id in song_ids:
            return_dict[id]=dict(and_result[qp][id])
            # print(return_dict[id])
        result[qp]=return_dict
        # print(result[qp])
    return result

# do_searching("0671039741",search_range=["ISBN"])
# normal_searching('后来',mode=2)
# print(basic_search('爱','album_title'))

# print(do_searching('0441805841'))

# 0786869216
# 0671039741
# 0385498721
# 0156012197
# 0439139597
# 0345339495
# 0140042598
# 0060529709
# 068486424X
# 0451179285
# 0385720467
# 0385512104