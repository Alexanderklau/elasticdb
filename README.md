# elasticdb使用手册
---
接口参数说明

> 
|参数|必选|类型|说明|
|:-------   |:-------|:-----|-----                               |
|index |ture    |str|索引名 ，可认为是数据库|
|type|true    |str|索引类型，可认为是表名|
|keywords|ture    |str|关键字 |
|page|ture    |str|页数，分页逻辑|
|size|ture    |str|每页展示条数，分页逻辑使用|

1 查询包含的关键字的日志（展示前10条）

```
a = esdb.search_searchdoc(index=monlog, type="doc", keywords="cpu")
for i in a:
    print i["_source"]["message"]
```
2 查询指定的索引下的数据，并且分页  
示例：查询index为”oplog-2018-08,oplog-2018-12”，并且每页展示（size）5条，输出第二页（page）

```
for i in esdb.serch_by_index(index="oplog-2018-08,oplog-2018-12", page=2, size=5)["hits"]["hits"]:
     print(i["_source"]["message"])
```
3 输出所有日志(输出全部)

```
for i in esdb.search_all(client=esdb.conn, index="monlog-*", type="doc"):
     print i
```

4 输出去重后的日志(分页，带关键字）  
示例：关键字为空，搜索monlog的所有数据，展示第一页，并且每页展示10条

```
for i in esdb.serch_es_count(keywords = "", index="monlog-*", type="doc",page=1, size=10):
     print i
```

5 删除指定索引的值  
示例：删除monlog的所有值

```
esdb.delete_all_index(index="monlog-*", type="doc")
```

6 查询集群健康状态

```
esdb.check_health()
```

7 往索引中添加数据

```
body = {"name": 'lucy2', 'sex': 'female', 'age': 10}
print esdb.insertDocument(index='demo', type='test', body=body)
```

8 获取指定index、type、id对应的数据

```
print esdb.getDocById(index='demo', type='test', id='6gsqT2ABSm0tVgi2UWls')
```

9 更新指定index、type、id所对应的数据

```
body = {"doc": {"name": 'jackaaa'}}#修改部分字段
print esdb.updateDocById('demo', 'test', 'z', body)
```

10 批量插入数据

```
_index = 'demo'
_type = 'test_df'
import pandas as pd
frame = pd.DataFrame({'name': ['tomaaa', 'tombbb', 'tomccc'],
                        'sex': ['male', 'famale', 'famale'],
                        'age': [3, 6, 9],
                        'address': [u'合肥', u'芜湖', u'安徽']})

print esAction.insertDataFrame(_index, _type, frame)
```
