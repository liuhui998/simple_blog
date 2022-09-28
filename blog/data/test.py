from pprint import pprint
from ast import literal_eval

data = """
layout: post
title: 没有馅儿的包子
date: 2020-08-22 07:03
comments: true
categories: ["书摘","懒惰"]
""".strip()

arr = list((item.split(": ") for item in data.split("\n")))
res = dict(arr)
print("<>" * 40)
print(literal_eval(res['categories']))
print("<>" * 40)
res['categories'] = literal_eval(res['categories'])

print(res)

data1 = """
layout: post
title: 没有馅儿的包子
date: 2020-08-22 07:03
comments: true
categories:
""".strip()

arr = list((item.split(": ") for item in data1.split("\n")))
print(">" * 60)
for index in range(len(arr)):
    print("*" * 60)
    print(arr[index][0])
    if arr[index][0] == "categories:":
        print(">>> categories >>>")
        arr[index][0] = "categories"
        arr[index].append("[]")
        pprint(arr[index])
pprint(arr)
print(">" * 60)
res = dict(arr)
res['categories'] = literal_eval(res['categories'])

print(res)