---
title: "Pandas使用技巧"
date: 2022-09-01T20:07:17+08:00
description: "Pandas使用技巧"
author: "shaun"
featured: true
toc: false
# menu: main
usePageBundles: false
codeMaxLines: 10
codeLineNumbers: false
figurePositionShow: true
categories:
  - Technology
tags:
  - pandas
---
`Pandas`是一个开源的，BSD许可的库，为[Python](https://www.python.org/) (opens new window)编程语言提供高性能，易于使用的数据结构和数据分析工具。
<!--more-->

### 入门
[Pandas入门文档](https://www.pypandas.cn/docs/getting_started/10min.html)

### loc && iloc

#### 区别
- loc: 通过行标签索引行数据 
- iloc: 通过行号索引行数据 
- ix: 通过行标签或者行号索引行数据（基于loc和iloc 的混合） 

{{% notice tip "注意📢" %}}
iloc是按照行数取值，而loc按着index名取值
{{% /notice %}}

#### loc

```py
import numpy as np
import pandas as pd
from pandas import *
from numpy import *
 
data=DataFrame(np.arange(16).reshape(4,4),index=list("ABCD"),columns=list("wxyz"))
print(data)
#    w   x   y   z
#A   0   1   2   3
#B   4   5   6   7
#C   8   9  10  11
#D  12  13  14  15
 
#loc
#行的选取
print(data.loc["A"])
print(type(data.loc["A"]))
#w    0
#x    1
#y    2
#z    3
#Name: A, dtype: int32
#<class 'pandas.core.series.Series'>
 
print(data.loc[["A"]])
print(type(data.loc[["A"]]))
#   w  x  y  z
#A  0  1  2  3
#<class 'pandas.core.frame.DataFrame'>
#综上，[]返回Series,[[]]返回DataFrame
 
print(data.loc["A","w"])
print(type(data.loc["A","w"]))
#0
#<class 'numpy.int32'>
 
print(data.loc[:,"w"])
print(type(data.loc[:,"w"]))
#A     0
#B     4
#C     8
#D    12
#Name: w, dtype: int32
#<class 'pandas.core.series.Series'>
 
print(data.loc["A":"C"])
print(type(data.loc["A":"C"]))
#   w  x   y   z
#A  0  1   2   3
#B  4  5   6   7
#C  8  9  10  11
#<class 'pandas.core.frame.DataFrame'>
 
print(data.loc["A":"C","w":"y"])
print(type(data.loc["A":"C","w":"y"]))
#   w  x   y
#A  0  1   2
#B  4  5   6
#C  8  9  10
#<class 'pandas.core.frame.DataFrame'>
 
print(data.loc[["A","C"],["w","y"]])
print(type(data.loc[["A","C"],["w","y"]]))
#   w   y
#A  0   2
#C  8  10
#<class 'pandas.core.frame.DataFrame'>
 
print(data.loc[:,["w","y"]])
print(type(data.loc[:,["w","y"]]))
#    w   y
#A   0   2
#B   4   6
#C   8  10
#D  12  14
#<class 'pandas.core.frame.DataFrame'>
 
#列的选取
print(data["w"])#等同于print(data.loc[:,"w"])
#A     0
#B     4
#C     8
#D    12
#Name: w, dtype: int32
print(data.loc[:,"w"])
#A     0
#B     4
#C     8
#D    12
#Name: w, dtype: int32
print(data["w"].equals(data.loc[:,"w"]))#True
 
#根据特殊条件选取行列
print(data["w"]>5)
#A    False
#B    False
#C     True
#D     True
#Name: w, dtype: bool
 
print(data.loc[data["w"]>5])
#    w   x   y   z
#C   8   9  10  11
#D  12  13  14  15
print(data.loc[data["w"]>5,"w"])
print(type(data.loc[data["w"]>5,"w"]))
#C     8
#D    12
#Name: w, dtype: int32
#<class 'pandas.core.series.Series'>
print(data.loc[data["w"]>5,["w"]])
print(type(data.loc[data["w"]>5,["w"]]))
#    w
#C   8
#D  12
#<class 'pandas.core.frame.DataFrame'>
print(data["w"]==0)
print(data.loc[lambda data:data["w"]==0])
print(type(data.loc[lambda data:data["w"]==0]))
#A     True
#B    False
#C    False
#D    False
#Name: w, dtype: bool
#   w  x  y  z
#A  0  1  2  3
#<class 'pandas.core.frame.DataFrame'>
 
#loc赋值
print(data)
#    w   x   y   z
#A   0   1   2   3
#B   4   5   6   7
#C   8   9  10  11
#D  12  13  14  15
data.loc[["A","C"],["w","x"]]=999
print(data)
#     w    x   y   z
#A  999  999   2   3
#B    4    5   6   7
#C  999  999  10  11
#D   12   13  14  15
 
```

### iloc

```py
data=DataFrame(np.arange(16).reshape(4,4),index=list("ABCD"),columns=list("wxyz"))
print(data)
#    w   x   y   z
#A   0   1   2   3
#B   4   5   6   7
#C   8   9  10  11
#D  12  13  14  15
 
print(data.iloc[0])
print(type(data.iloc[0]))
#w    0
#x    1
#y    2
#z    3
#Name: A, dtype: int32
#<class 'pandas.core.series.Series'>
#print(data.iloc["A"])报错
 
#print(data.loc[0])报错
print(data.loc[["A"]])
print(type(data.loc["A"]))
#   w  x  y  z
#A  0  1  2  3
#<class 'pandas.core.series.Series'>
```

### 删除数据
### drop函数
语法：
```py
DataFrame.drop(labels,axis=0,level=None,inplace=False,errors='raise')
```



| 参数   | 说明                                                         |
| ------ | :----------------------------------------------------------: |
| labels | 接收string或array，代表要删除的行或列的标签（行名或列名）。无默认值 |
|axis|	接收0或1，代表操作的轴（行或列）。默认为0，代表行；1为列。|
|level|	接收int或索引名，代表标签所在级别。默认为None|
|inplace|	接收布尔值，代表操作是否对原数据生效，默认为False|
|errors|	errors='raise’会让程序在labels接收到没有的行名或者列名时抛出错误导致程序停止运行，errors='ignore’会忽略没有的行名或者列名，只对存在的行名或者列名进行操作。默认为‘errors=‘raise’’。|

#### 删除列
```py
del df['columns']  # 改变原始数据
df.drop('columns',axis=1)  # 删除不改表原始数据，可以通过重新赋值的方式赋值该数据
df.drop('columns', axis=1,inplace='True')  # 改变原始数据
df.drop(["columns1", "columns2", "columns3"], axis=1,inplace='True')  # 删除多列，改变原始数据
```
#### 删除行
```py
df.drop(labels=['a', 'b'], axis=1) # 同时删除a,b列
df.drop(labels=range(2)) # 等价于df.drop(labels=[0,1])
```

### 遍历

按行遍历，将`DataFrame`的每一行迭代为`(index, Series)`对，可以通过`row[name]`或`row.name`对元素进行访问。

#### iterrows
```py
for index, row in df.iterrows():
    print(row['s0'])  # 也可使用 row.s0
```

#### itertuples
```py
for index, row in df.iteritems():
    print(row[0])
```

#### iteritems
```py
for index, row in df.iteritems():
    print(row[0])
```

### 排序

#### df. sort_values()
```py
DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
```
**参数说明**

| 参数 | 值   | 说明 |
| ---- | ---- | :--- |
|axis| {0 or ‘index’, 1 or ‘columns’},</br>default 0，|默认按照列排序，即纵向排序；如果为1，则是横向排序。|
|by| str or list of str；|如果axis=0，那么by="列名"；如果axis=1，那么by="行名"。|
|ascending| 布尔型，|True则升序，如果by=['列名1','列名2']，则该参数可以是[True, False]，即第一字段升序，第二个降序。|
|inplace| 布尔型 |是否用排序后的数据框替换现有的数据框。|
|kind| str {‘quicksort’, ‘mergesort’, ‘heapsort’}, default ‘quicksort’| 排序算法，似乎不用太关心。|
|na_position| {‘first’, ‘last’}, default ‘last’，|默认缺失值排在最后面。|



```py
df.sort_index()
df.sort_index(ascending=False)

```

#### df. sort_index()

**调用方式**
```py
sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, by=None)
```
**参数说明**

| 参数 | 说明 |
| ---- | :--- |
|axis| 0按照行名排序；1按照列名排序|
|level| 默认None，否则按照给定的level顺序排列---貌似并不是，文档|
|ascending| 默认True升序排列；False降序排列|
|inplace| 默认False，否则排序之后的数据直接替换原来的数据框|
|kind| 排序方法，{‘quicksort’, ‘mergesort’, ‘heapsort’}, default ‘quicksort’。似乎不用太关心。|
|na_position| 缺失值默认排在最后{"first","last"}|
|by| 按照某一列或几列数据进行排序，但是by参数貌似不建议使用|

### 去重

#### drop_duplicates
```py
def drop_duplicates(
        self,
        subset: Optional[Union[Hashable, Sequence[Hashable]]] = None,
        keep: Union[str, bool] = "first",
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> Optional[DataFrame]:
  pass
```

**参数说明：**
* subset：指定重复数据所在列
* keep：</br>（1）first:去除重复列后第一次出现的行数据；</br>（2）last：去除重复列后最后一次出现的行数据；</br>（3）False：删除所有重复项
* inplace：</br>True：直接在原数据删除；</br>False：不直接在原数据删除并生成一个副本

### 重命名

```py
def rename(
        self,
        mapper: Optional[Renamer] = None,
        *,
        index: Optional[Renamer] = None,
        columns: Optional[Renamer] = None,
        axis: Optional[Axis] = None,
        copy: bool = True,
        inplace: bool = False,
        level: Optional[Level] = None,
        errors: str = "ignore",
    ) -> Optional[DataFrame]:
    pass

# 将a,b,c 替换成A,B,C
df.rename(columns={'a': 'A', 'b': 'B', 'c': 'C'}, inplace=True)
```
**参数说明**
* mapper: 字典值，键表示旧名称，值表示新名称。这些参数只能一次使用。
* axis: int或字符串值，“ 0”表示行，“ 1”表示列。
* copy: 如果为True，则复制基础数据。
* inplace: 如果为True，则在原始 DataFrame 中进行更改。
* level: 用于在数据帧具有多个级别索引的情况下指定级别。

### 清洗空值

如果我们要[删除包含空字段](https://mp.weixin.qq.com/s/DHN_S3JGOoHp4fj5oFjwhw)的行，可以使用 dropna() 方法，语法格式如下：
```py
DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
```
**参数说明：**

* axis：默认为 0，表示逢空值剔除整行，如果设置参数 axis＝1 表示逢空值去掉整列。
* how：默认为 'any' 如果一行（或一列）里任何一个数据有出现 NA 就去掉整行，如果设置 how='all' 一行（或列）都是 NA 才去掉这整行。
* thresh：设置需要多少非空值的数据才可以保留下来的。
* subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
* inplace：如果设置 True，将计算得到的值直接覆盖之前的值并返回 None，修改的是源数据。


