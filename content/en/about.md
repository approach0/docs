## About
[Approach Zero](https://approach0.xyz) is a math-aware search engine.

“Math-aware” means you can add math expression(s) as some of your keywords to have search engine help you find similar expressions and return those documents/topics that you may find relevant to your query. In short, a typical search engine plus math search.

### Use Case
Math search can be helpful in Q&A websites: Assume that you are trying to solve a tough question in your homework, spending so much time on it without any clue. Yes, you do not simply want an answer, but all you need is some hints. However, spending a lot of time on it without any progress is absolutely a desperate experience, it would be very helpful if you can search for similar or identical questions that have been already answered somewhere.

### Online Demo
Visit https://approach0.xyz

![](https://cdn.jsdelivr.net/gh/approach0/docs@master/content/static/clip.gif)

### Current State
As for now, all basic functionalities are already implemented (see [features](features.html)) and
it is ready for using on a big dataset. However, this project is still considered a "hobby project", you may not use it for production for many reasons.

### A Little History...
In 2014, the idea of searching math formulas takes off as a graducate level course project (at the University of Delaware).

Later, I am persuaded by my instructor to further do some research work on this, she then became my advisor at that time.

In 2015 summer, [my thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf) on this topic is submitted.

In 2016, a [math-only search engine prototype](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ecir2016.pdf) is published in the ECIR 2016 conference.

Shortly after, this Github project is created, the goal was to rewrite most of the code and develop a math-aware search engine that can combine both math formula and text keywords into one query.

In late 2016, the first rewritten version of math-aware search engine is complete, it is announced in [Meta site of Mathematics StackExchange](https://math.meta.stackexchange.com/questions/24978) and top users on that site have acknowledged the usefulness and also provided some good advices.

In 2017, I go back to China and work at Huawei doing a STB (TV box) project, irrelevant to search engine whatsoever.

In 2017 Fall, with the feeling that a math-aware search engine would probably provide huge value, I gave up my job and continued working on this topic as a PhD student at [RIT](https://www.cs.rit.edu/~dprl/members.html).
During the first two years of my PhD study, I kept improving the effectiveness and efficiency of the formula retrieval model.

In 2019, the new model has brought me [my first research full paper](http://ecir2019.org/best-paper-awards/) at the ECIR 2019 conference (and a best application paper award!).

In May 2019, the new model has been put online, it has indexed over 1 million posts and there are only 3 search instances running on two low-cost Linode servers.

In early 2020, a paper focusing on efficiency has just been accepted at the [ECIR 2020](https://link.springer.com/chapter/10.1007/978-3-030-45439-5_47) conference, this paper shows our system is the first one to produce very effective math search results with realtime query runtimes in a single thread.
