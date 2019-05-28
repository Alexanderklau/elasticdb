# coding: utf-8
__author__ = 'lau.wenbo'

from elasticsearch import Elasticsearch
from elasticsearch import helpers


class Es:
    def __init__(self):
        self.hosts = "127.0.0.1"
        self.conn = Elasticsearch(hosts=self.hosts, port=9200)


    def check(self):
        '''
        输出当前系统的ES信息
        '''
        return self.conn.info()

    def ping(self):
        return self.conn.ping()


    def check_health(self):
        '''
        检查集群的健康状态
        :return:
        '''
        status = self.conn.transport.perform_request('GET', '/_cluster/health', params=None)["status"]
        return status

    def __del__(self):
        self.close()


    def get_index(self):

        return self.conn.indices.get_alias("*")

    def searchDoc(self, index=None, type=None, body=None):

            return self.conn.search(index=index, doc_type=type, body=body)

    def search_specify(self, index=None, type=None, keywords=None, page=None, size=None):
        # 查询包含的关键字的日志
        query = {
            'query': {
                'match': {
                    'message': keywords
                }
            },
            'from':page * size,
            'size':size
        }
        message = self.searchDoc(index, type, query)
        return message

    def search_searchdoc(self, index=None, type=None, keywords=None):
        # 查询包含的关键字的日志
        query = {
            'query': {
                'match': {
                    'message': keywords
                }
            }
        }
        message = self.searchDoc(index, type, query)
        return message


    def serch_count(self, keywords = None, index=None):
        # 输出不去重的日志
        if keywords == '':
            query = {
                "query": {
                    "match_all": {}
                },
                "size": 0,
                "aggs": {
                    "message_count": {
                        "cardinality": {
                            "field": "message.keyword"
                        }
                    }
                }
            }
        else:
            query ={
                "query": {
                    "match": {
                        'message': keywords
                    }
                },
                "size": 0,
                "aggs": {
                    "message_count": {
                        "cardinality": {
                            "field": "message.keyword"
                        }
                    }
                }
            }

        return self.conn.search(index=index, doc_type="doc", body=query)

    # 输出去重后的日志
    def serch_es_count(self, keywords=None, index=None, page=None, size=None):
        if keywords == '':
            query = {
                "query": {
                    "match_all": {}
                },
                "collapse": {
                    "field": "message.keyword"
                },
                "sort":
                    { "@timestamp":
                          { "order": "desc" }
                    },
                "from":page * size,
                "size":size
            }
        else:
            query = {
                "query": {
                    "match": {
                        'message': keywords
                    }
                },
                "collapse": {
                    "field": "message.keyword"
                },
                "sort":
                    { "@timestamp":
                          { "order": "desc" }
                    },
                "from": page * size,
                "size": size
            }

        return self.conn.search(index=index, doc_type="doc", body=query)

    def search_by_index(self, index=None, type=None, page=None, size=None):
        # 查询index，分页处理
        query = {
            'query': {'match_all': {}},
            'from':page * size,
            'size':size
        }
        message = self.searchDoc(index, type, query)
        return message

    def search_all(self, client=None, index=None, type=None):
        # 查询所有的日志,输出所有日志，不分页处理
        try:
            query = {"query": {"match_all": {}}}
            return helpers.scan(client, query, scroll="10m", index=index, doc_type=type, timeout="10m")
        except:
            return (-1, "connetion esdb error")

    def delete_all_index(self, index, type=None):
        '''
        删除指定index下的所有数据
        '''
        try:
            query = {'query': {'match_all': {}}}
            return self.conn.delete_by_query(index=index, body=query, doc_type=type)
        except Exception, e:
            return str(e) + ' -> ' + index

    def getDocById(self, index, type, id):
        '''
        获取指定index、type、id对应的数据
        '''
        return self.conn.get(index=index, doc_type=type, id=id)

    def updateDocByIGd(self, index, type, id, body=None):
        '''
        更新指定index、type、id所对应的数据
        '''
        return self.conn.update(index=index, doc_type=type, id=id, body=body)

    def deleteDocByQuery(self, index, query, type=None):
        '''
        删除idnex下符合条件query的所有数据
        '''
        return self.conn.delete_by_query(index=index, body=query, doc_type=type)

    def insertDataFrame(self, index, type, dataFrame):
        '''
        批量插入接口;
        bulk接口所要求的数据列表结构为:[{{optionType}: {Condition}}, {data}]
        '''
        dataList = dataFrame.to_dict(orient='records')
        insertHeadInfoList = [{"index": {}} for i in range(len(dataList))]
        temp = [dict] * (len(dataList) * 2)
        temp[::2] = insertHeadInfoList
        temp[1::2] = dataList
        try:
            return self.conn.bulk(index=index, doc_type=type, body=temp)
        except Exception, e:
            return str(e)

    def insertDocument(self, index, type, body, id=None):
        '''
        插入一条数据body到指定的index、指定的type下;可指定Id,若不指定,ES会自动生成
        '''
        return self.conn.index(index=index, doc_type=type, body=body, id=id)

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception, e:
                pass
            finally:
                self.conn = None


if __name__ == '__main__':
    pass