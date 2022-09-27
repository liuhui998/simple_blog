data = """
layout: post
title: 没有馅儿的包子
date: 2020-08-22 07:03
comments: true
categories: ["书摘","懒惰"]
""".strip()

arr = list((item.split(": ") for item in data.split("\n")))
res = dict(arr)
print(res)
