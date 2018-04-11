# TweetAnalysis
*Sentiment analysis of tweets and its impact on the stock market*


Sentiment Analysis is the field of study that analyzes people's opinions, sentiments, evaluations, attitudes, and emotions from written languages. (Liu 2012)

<!-- TOC -->

- [Contents](#contents)
- [Objective](#objective)
- [Introduction](#introduction)
- [Reference](#Reference)
- [Open Source Implementations](#open-source-implementations)
    - [NodeJS](#nodejs)
    - [Java](#java)
    - [Python](#python)
    - [R](#r)
    - [Golang](#golang)
    - [Ruby](#ruby)
    - [CSharp](#csharp)
- [Acknowledgment](#Acknowledgment)    

<!-- /TOC -->

## Objective

The goal of this repository is to provide adequate links for scholars who want to research in this domain; and at the same time, be sufficiently accessible for developers who want to integrate sentiment analysis into their applications.

## Introduction

Sentiment Analysis happens at various levels: 
- Document-level Sentiment Analysis evaluate sentiment of a single entity (i.e. a product) from a review document. 
- Sentence-level Sentiment Analysis evaluate sentiment from a single sentence. 
- Aspect-level Sentiment Analysis performs finer-grain analysis. For example, the sentence “the iPhone’s call quality is good, but its battery life is short.” evaluates two aspects: call quality and battery life, of iPhone (entity). The sentiment on iPhone’s call quality is positive, but the sentiment on its battery life is negative. (Liu 2012)

Most recent research focuses on the aspect-based approaches. But not all opensource implementations are caught up yet.

There are many different approaches to solve the problem. Lexical methods, for example, look at the frequency of words expressing positive and negative sentiment (from i.e. SentiWordNet) occurring in the given sentence. Supervised Machine Learning, such as Naive Bayes and Support Vector Machine (SVM), can be used with training data. Since training examples are difficult to obtain, Unsupervised Machine Learning, such as Latent Dirichlet Allocation (LDA) and word embeddings (Word2Vec) are also used on large unlabeled datasets. Recent works also apply Deep Learning methods such as Convolutional Neural Network (CNN) and Long Short-term Memory (LSTM), as well as their attention-based variants. You will find more details in the survey papers.

## Survey Papers 

Liu, Bing. "Sentiment analysis and opinion mining." Synthesis lectures on human language technologies 5.1 (2012): 1-167. [[pdf]](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.244.9480&rep=rep1&type=pdf)

Vinodhini, G., and R. M. Chandrasekaran. "Sentiment analysis and opinion mining: a survey." International Journal 2.6 (2012): 282-292. [[pdf]](http://www.dmi.unict.it/~faro/tesi/sentiment_analysis/SA2.pdf)

Medhat, Walaa, Ahmed Hassan, and Hoda Korashy. "Sentiment analysis algorithms and applications: A survey." Ain Shams Engineering Journal 5.4 (2014): 1093-1113. [[pdf]](http://www.sciencedirect.com/science/article/pii/S2090447914000550)

