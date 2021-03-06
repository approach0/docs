## Usage
The binaries generated from build are distributed in the `run` directories in most modules.
And many of binaries are named `test-*.out` (such as `blob-index/run/test-blob-index.out`), they are for testing purpose.
Others are commands to be used by search engine users (e.g. `searchd/run/searchd.out`).

Here we only document a few commands that are considered important.

In general, you can issue `command -h` in most important commands to see its command line options and usage description.

### Tex parser
Run our TeX parser to see the corresponding operator tree of a math expression. And often this command is used to investigate a TeX grammar parsing error in the indexing process described later.

Below is an example of parsing \\(\dfrac a b + c\\).
```
$ ./tex-parser/run/test-tex-parser.out
edit: \frac a b +c
return string: no error (max path ID = 3).
return code: 0
Operator tree:
     └──(plus) #4, token=ADD, subtr_hash=`41020', pos=[6, 12].
           │──(pos) #5, token=SIGN, subtr_hash=`39068', pos=[6, 9].
           │     └──(frac) #6, token=FRAC, subtr_hash=`46604', pos=[6, 9].
           │           │──#1(hanger) #7, token=HANGER, subtr_hash=`4808', pos=[6, 7].
           │           │     └──(base) #8, token=BASE, subtr_hash=`1160', pos=[6, 7].
           │           │           └──[normal`a'] #1, token=VAR, subtr_hash=`a', pos=[6, 7].
           │           └──#2(hanger) #9, token=HANGER, subtr_hash=`4820', pos=[8, 9].
           │                 └──(base) #10, token=BASE, subtr_hash=`1164', pos=[8, 9].
           │                       └──[normal`b'] #2, token=VAR, subtr_hash=`b', pos=[8, 9].
           └──(pos) #11, token=SIGN, subtr_hash=`26816', pos=[11, 12].
                 └──(hanger) #12, token=HANGER, subtr_hash=`4832', pos=[11, 12].
                       └──(base) #13, token=BASE, subtr_hash=`1168', pos=[11, 12].
                             └──[normal`c'] #3, token=VAR, subtr_hash=`c', pos=[11, 12].

Suffix paths (leaf-root paths/total = 3/9):
- [path#1, leaf#1] normal`a': VAR(#1)/BASE(#8)/HANGER(#7)/rank1(#0)/FRAC(#6)/SIGN(#5)/ADD(#4)
* [path#1, leaf#7] 1560: HANGER(#7)/rank1(#0)/FRAC(#6)/SIGN(#5)/ADD(#4) 
- [path#2, leaf#2] normal`b': VAR(#2)/BASE(#10)/HANGER(#9)/rank2(#0)/FRAC(#6)/SIGN(#5)/ADD(#4)
* [path#2, leaf#9] 156c: HANGER(#9)/rank2(#0)/FRAC(#6)/SIGN(#5)/ADD(#4) 
* [path#0, leaf#6] b8a4: FRAC(#6)/SIGN(#5)/ADD(#4) 
* [path#0, leaf#5] 9b34: SIGN(#5)/ADD(#4) 
- [path#3, leaf#3] normal`c': VAR(#3)/BASE(#13)/HANGER(#12)/SIGN(#11)/ADD(#4) 
* [path#3, leaf#12] 1578: HANGER(#12)/SIGN(#11)/ADD(#4) 
* [path#0, leaf#11] 6b58: SIGN(#11)/ADD(#4) 
```
Type `\` followed by `Tab` to auto-complete some frequently used TeX commands.

### Crawler
A Python script crawler (`demo/crawler/crawler-math.stackexchange.com.py`) is included specifically for crawling *math stackexchange*.
Users are asked to write their own crawlers if they are trying to crawl data from other websites.

Install BeautifulSoup4 used by demo crawler.
```
$ apt-get install python3-pip
$ pip3 install BeautifulSoup4
```

Debian users may also need to install pycurl:
```
$ apt-get install python3-pycurl
```

To crawl *math stackexchange* from page 1 to 3:
```
$ cd $PROJECT/demo/crawler
$ ./crawler-math.stackexchange.com.py --begin-page 1 --end-page 3
```
Crawler will output all harvest files (in JSON) to `./tmp` directory which is a conventional directory name for output and it will not be tracked by git as specified by `.gitignore`.

You can press Ctrl-C to stop crawler in the middle of crawling process.

The output of crawler for each post will have two files, one is `*.json` corpus file (for now it contains URL and plain text of the post extracted by crawler), another is `*.html` file, which is for previewing this post corpus. (to preview it, connect to Internet and open it with your browser)

For quick starter, you can skip the time-consuming crawling process and directly [download a test corpus](https://www.cs.rit.edu/~dprl/data/mse-corpus.tar.gz) (~ 930 MB) to play around.  This corpus contains over one million posts we previously
crawled from *math stackexchange*.

Another crawler script `crawler-artofproblemsolving.com.py` is available for crawling [artofproblemsolving.com](https://artofproblemsolving.com).

### Indexer
After corpus is generated by crawler. Indexer is used to index corpus files to highly optimized search engine indices.
To invoke one-time `indexer` and generate indices from corpus files under `./test-corpus` directory

```
$ cd $PROJECT/indexer
$ ./run/indexer.out -p ./test-corpus 2> error.log
```

Again, the output (resulting index) is generated under
`./tmp` directory unless you specify `-o` option to name
a output directory.

Current indexer does not support index update.
If you are using indexer to add new documents into existing
index in multiple runs, you need to ensure that the newly added
documents are not previously indexed. Otherwise duplicate document
may occur in search results.

If you are indexing a corpus with Chinese words, use `-d`
option to specify CppJieba dictionary path when calling
`indexer.out`. This will slow down indexing but it enables
searcher/searchd to search Chinese terms later (one also has to
to specify `-d` in searcher/searchd).

### Indexd
`indexd` is the daemonized version of indexer, example commmand:
```sh
$ ./run/indexd.out -o ~/nvme0n1/mnt-mathtext.img/ > /dev/null 2> error.log
```
Like indexer, `-o` option specifies the output directory.

Script `indexer/scripts/json-feeder.py` is provided to feed json files under your
corpus directory recursively to a running indexd. Show usage from `--help` option:
```sh
$ ./scripts/json-feeder.py --help 
usage: json-feeder.py [-h] [--maxfiles MAXFILES] [--corpus-path CORPUS_PATH]
                      [--indexd-url INDEXD_URL]

Approach0 indexd json feeder.

optional arguments:
  -h, --help            show this help message and exit
  --maxfiles MAXFILES   limit the max number of files to be indexed.
  --corpus-path CORPUS_PATH
                        corpus path.
  --indexd-url INDEXD_URL
                        indexd URL (optional).
```

### Single query searcher
To test and run a query on the index you have just created,
run a *single-query searcher* which takes your query, searches for
relevant documents and exits immediately.

To run mixed-query searcher with a test query *function* and
\\(f(x) = x^2 + 1\\) mixed keywords against index `../indexer/tmp`, issue:

```sh
$ cd $PROJECT/search
$ ./run/test-search.out -i ../indexer/tmp -t 'function' -m 'f(x) = x^2 + 1'
```

This searcher returns the first "page" of top-K relevant search
results (relevant keywords are highlighted in console). You
can use `-p` option to specify another page number to be returned.

### Search daemon
On the top of our search engine modules is search daemon
program `searchd`, located at `searchd/run/searchd.out`.
It runs as a HTTP daemon that handles every query (in JSON)
sent to it and return search results (in JSON too).

`searchd` can be specified to cache a portion of
index posting into memory.  You can specify the maximum cache limit 
for term index and math index using `-c` and `-C` option(s) respectively.

To run searchd,
```
$ cd $PROJECT/searchd
$ ./run/searchd.out -i <index path> &
```

You can then test searchd by running *curl* scripts existing
in searchd directory:

```
$ ./scripts/test-query.sh ./tests/query-valid.json
```

To shutdown searchd, type command
```
$ kill -INT <pid>
```

### Search daemon cluster
Search daemon can scale horizontally to multiple nodes across multiple cores or machines.
This functionality is implemented using OpenMPI. The search results retrieved from all nodes
are merged and returned from master node.
Scaling out can be used to reduce search latency by dividing data into multiple smaller
segments.

Also, as each instance produces its own log files, it is highly recommanded to run binaries in
different folders, one can do this by simply creating two folders and make symbolic
binaries in each of them.

One example command to run 3 instances over two single machines, with local machine runing 2
instances and a remote host runing 1 instance:
```
$ mpirun --host localhost,localhost,192.168.210.5 \
     -n 1 --wdir ./run1 searchd.out -i ../mnt-demo.img/ -c 800 : \
     -n 1 --wdir ./run2 searchd.out -i ../mnt-demo2.img/ -c 800 : \
     -n 1 --wdir /root ./searchd.out -i ./mnt-demo3.img/ -c 1024
```

To stop all nodes in a cluster gracefully, send `USR1` signal to master instance:
```
$ killall -USR1 searchd.out
```
