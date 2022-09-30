---
layout: post
title: "从数据中提取季节性和趋势 [2-1]"
date: 2018-06-24 14:05
comments: true
categories:
---

因为最近在做销售预测的一些工作，同时也在Team内做一些小的分享；为了让自己把一些基础概念搞的更清楚，我试着翻译了一些有趣的文章。只是自己练练，哈哈！


读了这篇文章你能得到什么：

1. 你能知道你的手上数据的趋势到底是上升还是下降, 速度（斜率）怎么样

2. 知道怎么开始学数据的季度性（季节系数）

本文来自: [Extracting Seasonality and Trend from Data: Decomposition Using R](https://anomaly.io/seasonal-trend-decomposition-in-r/)

![time series decomposition seasonal trend](/static/images/seasonal-trend-decomposition-in-r/time-series-decomposition-seasonal-trend.png)

时间序列分解时间序列分成三个子序列。

译注：看起来很难，实际需要的数学只有加减剩除，如果有人抬杠说这篇需要线性代数，你可以先不理他哈。

## 理解时序分解

### 将一个时间序列分解为多个序列

时间序列分解是将时间序列转换为多个不同时间序列的数学过程。原始时间序列通常分为三个组件系列：

* 季节性：以固定时间段重复的模式。

例如，一个网站在周末可能会收到更多的访问; 这会产生季节性(周期)为7天的数据；

也可能是某个电商平台的每天销售数据，那么这样数据的季节性(周期)是 365.25天。

* 趋势：指标的基本趋势。一个日益流行的网站应该显示出一个普遍的趋势；某个电商品类也有有自己的趋势。

* 随机：也称为“噪音”，“不规则”或“余数(remainder)”，这是季节和趋势序列删除后原始时间序列的残差（residuals）；比如911事件对 对美国航空业的影响就是一个噪音，你很难预测他的产生。

### 使用加法或乘法分解？

为了实现成功的分解，在加法和乘法模型之间进行选择非常重要，这需要分析系列。例如，当时间序列增加时，季节性的大小是否会增加？

澳大利亚啤酒生产 - 季节性变化(方差)看起来不变; 当时间序列值增加时它不会改变。我们应该使用加法模型。
![aus beer produce, additive-model ](/static/images/seasonal-trend-decomposition-in-r/additive-model.png)

航空公司乘客数量 - 随着时间序列数量的增加，季节性变化(方差)也随之增加。这里我们应该使用乘法模型。
![Airline Passenger Numbers, Multiplicative-model ](/static/images/seasonal-trend-decomposition-in-r/multiplicative-model.png)


** 加法模型：时间序列=季节性+趋势+随机 **

*** 译注：如果时间序列的波峰波谷的差距一直差不多，就用加法模型。***

** 乘法模型：时间序列=趋势\*季节性\*随机 **

*** 译注：如果时间序列的波峰波谷的差距随着时间推移而一直加大，就用乘法模型。***

## 循序渐进：时间序列分解

我们将研究R中的decompose()函数。作为分解函数，它将时间序列作为参数，并将其分解为季节性，趋势和随机时间序列。我们将逐步重现R中的decompose()函数以了解它的工作原理。由于两种模式之间存在差异，我们将使用两个示例：澳大利亚啤酒生产（加法）和航空公司乘客数量（乘法）。

** 译注：如果不懂编程可跳过上面这段话；后面会有一些程序代码，没关系，你只看你能看的懂的文字和图表就可以了。**

** 这一系列文章使用的编程语言是 [R](https://blog.gtwang.org/programming/r/), 这是一门在机器学习非常简练的语言！**


### 第1步：导入数据

#### 加法模型

如前所述，加法模型时间序列的一个很好的例子是啤酒生产; 随着时间增加，季节性保持相对恒定。

```
install.packages("fpp")
library(fpp)
data(ausbeer)
timeserie_beer = tail(head(ausbeer, 17*4+2),17*4-4)
plot(as.ts(timeserie_beer))
```

![aus beer produce, additive-model ](/static/images/seasonal-trend-decomposition-in-r/additive-model.png)

#### 乘法模型

每月的航空公司乘客数字是乘法时间序列的一个很好的例子； 乘客数据越多，观察到的季节性就越大。

```
install.packages("Ecdat")
library(Ecdat)
data(AirPassengers)
timeserie_air = AirPassengers
plot(as.ts(timeserie_air))
```

![Airline Passenger Numbers, Multiplicative-model ](/static/images/seasonal-trend-decomposition-in-r/multiplicative-model.png)


### 第2步：检测趋势

为了检测潜在的趋势，我们使用[中心移动平均线](http://www.itl.nist.gov/div898/handbook/pmc/section4/pmc422.htm) 来平滑时间序列。要执行分解，使用具有季节性的确切大小的移动窗口非常重要。

** 译注：这听起来有点难懂，你可以把这个移动窗口想像成一个移动漏斗机器人，它会自己动把漏斗中心两边的数据取平均，然后再放下来！**

因此，要分解一个时间序列，我们需要知道季节性周期：每周，每月等...如果您不知道这个数字，可以  使用[傅里叶变换检测季节性](https://anomaly.io/detect-seasonality-using-fourier-transform-r/)。

#### 加法模型

澳大利亚啤酒生产明显遵循年度季节性。由于每季度记录一次，每年记录4个数据点，我们使用期数为4的移动平均窗口。

```
install.packages("forecast")
library(forecast)
trend_beer = ma(timeserie_beer, order = 4, centre = T) #计算移动平均数，期数为4
plot(as.ts(timeserie_beer))
lines(trend_beer)
plot(as.ts(trend_beer))
```
澳洲啤酒实际产量与趋势（移动平均数）的叠加
![aus beer produce, additive-model  : time series + trend](/static/images/seasonal-trend-decomposition-in-r/additive-moving-average.png)

澳洲啤酒产量趋势（移动平均数）
![aus beer produce, additive-model trend](/static/images/seasonal-trend-decomposition-in-r/additive-trend.png)


#### 乘法模型

这里的过程与添加剂模型相同。航空公司的乘客数季节性看起来也是年度的。但是，它是按月记录的，所以我们选择期数为12的移动平均窗口。

```
install.packages("forecast")
library(forecast)
trend_air = ma(timeserie_air, order = 12, centre = T) #计算移动平均数，期数为12
plot(as.ts(timeserie_air))
lines(trend_air)
plot(as.ts(trend_air))
```

澳洲实际空乘数与趋势（移动平均数）的叠加
![Airline Passenger Numbers, Multiplicative-model:  timeseries + trend](https://anomaly.io/wp-content/uploads/2015/12/multiplicative-moving-average.png)

澳洲空乘数趋势
![Airline Passenger Numbers, Multiplicative-model:  trend](https://anomaly.io/wp-content/uploads/2015/12/multiplicative-trend.png)


### 第3步：去掉趋势信息，得到季节性

从时间序列中去掉先前计算的趋势，让新的时间序列清楚地显示季节性。


#### 加法模型

```
detrend_beer = timeserie_beer - trend_beer #实际数据减去趋势
plot(as.ts(detrend_beer)) #画出季度性图
```

![additive-detrend](https://anomaly.io/wp-content/uploads/2015/12/additive-detrend.png)

#### 乘法模型

```
detrend_air = timeserie_air / trend_air #实际数据除以趋势
plot(as.ts(detrend_air)) #画出季度性图
```
![multiplicative-detrend](https://anomaly.io/wp-content/uploads/2015/12/multiplicative-detrend.png)



