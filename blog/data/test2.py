data = """
---
layout: post
title: 不要忧虑
date: 2020-08-28 07:12
comments: true
categories: ["圣经","马太福音"]
---

我们每天都在忧虑，也许担心明天家人是否健康和睦，工作是否顺利，子女是否如意。

忧虑如同一个幽灵一样如影相随；随着年龄的增大，人无力感也在与日俱增。

但是我们如果知道自己只是受造物，这结局会大不一样？

![road](/images/unsplash/9X0tqbxCFpI.jpg)

Photo from [unsplash](https://unsplash.com/photos/9X0tqbxCFpI)


下面最多是我初信主时时所领受的经文：


马太福音第6章:

25 所以我告诉你们，不要为生命忧虑吃什么，喝什么。为身体忧虑穿什么。生命不胜于饮食吗？身体不胜于衣裳吗？

26 你们看那天上的飞鸟，也不种，也不收，也不积蓄在仓里，你们的天父尚且养活它。你们不比飞鸟贵重得多吗？

27 你们哪一个能用思虑使寿数多加一刻呢？（或作使身量多加一肘呢）

28 何必为衣裳忧虑呢？你想野地里的百合花，怎么长起来，它也不劳苦，也不纺线。

29 然而我告诉你们，就是所罗门极荣华的时候，他所穿戴的，还不如这花一朵呢。

30 你们这小信的人哪，野地里的草今天还在，明天就丢在炉里，神还给它这样的妆饰，何况你们呢。

31 所以不要忧虑，说，吃什么？喝什么？穿什么？

32 这都是外邦人所求的。你们需用的这一切东西，你们的天父是知道的。

33 你们要先求他的国和他的义。这些东西都要加给你们了。

34 所以不要为明天忧虑。因为明天自有明天的忧虑。一天的难处一天当就够了。


当我忧虑时，我读到这段经文时我又力量了！

用一句大话：“不要今天把明天的饭吃了，明天不吃饭会饿的！”
""".strip()

from pprint import pprint
import marko
#def check_header(data):
blog_lines = data.split("\n")
hr_lines = list(1 if (line == "---") else 0 for line in blog_lines[0:30])
print(sum(hr_lines))

second_occur_hr = -1
for index in range(1, 30):
    if "---" == blog_lines[index]:
        second_occur_hr = index
        break
print(second_occur_hr)

body = "\n".join(blog_lines[second_occur_hr + 1:])
print(marko.convert(body))