## Appendix

### Indri usage
The [Lemur/Indri](http://www.lemurproject.org/indri.php) project is a dependency of Approach Zero and it is responsible for text search functionality (math index and text index are separate, and they can be merged together by using a posting list interface on top of them).
We choose Indri because it is written in C++ and it can be easily integrated with Approach Zero which is written in C.
Unfortunately, Indri codebase is quite large and its documentation is very limited.

Here we use a newer version Indri to show how to do indexing and run query in a very minimal way.
```sh
$ cd ~
$ wget 'https://sourceforge.net/projects/lemur/files/lemur/indri-5.13/indri-5.13.tar.gz/download'
$ tar -xzf indri.tar.gz
$ cd indri-5.13 && ./configure && make
```

Create a parameters.xml at project directory:
```
<parameters>
        <memory>1024M</memory>
        <index>/path/to/new_indri_index</index>
        <trecFormat>false</trecFormat>
        <stemmer><name>krovertz</name></stemmer>
        <corpus>
                <path>/path/to/corpus</path>
                <class>txt</class>
        </corpus>
</parameters>
```
where the `new_indri_index` directory will be created shortly and `corpus` directory contains text files to be indexed, for example,
```sh
$ cat /path/to/corpus/ohsumed/0010927
Fatal Capnocytophaga canimorsus septicemia in a previously healthy woman.  A
previously healthy 47-year-old woman presented to the emergency department with
septic shock five days after a small dog bite on the dorsum of her hand.
Capnocytophaga canimorsus was isolated from blood cultures.  Despite intensive
therapy, multiple organ failure developed, and the patient died 27 days after
admission.  Characteristics of Capnocytophaga (formerly CDC group Dysgonic
Fermenter-2) infection are briefly discussed.  This unusual outcome in a
previously healthy patient and the need for careful management of dog bite
wounds, even if initially very small, is emphasized.
``` 

Create specified index output directory
```sh
$ mkdir ./new_indri_index
```

Build the index
```sh
$ cd ./buildindex
$ ./IndriBuildIndex ../parameters.xml
...
...
0:00: Documents parsed: 504 Documents indexed: 504
0:00: Closed /home/tk/wuhao_search/corpus/ohsumed/0018280
0:00: Opened /home/tk/wuhao_search/corpus/ohsumed/0017664
0:00: Documents parsed: 505 Documents indexed: 505
0:00: Closed /home/tk/wuhao_search/corpus/ohsumed/0017664
0:00: Opened /home/tk/wuhao_search/corpus/ohsumed/0013377
0:00: Documents parsed: 506 Documents indexed: 506
0:00: Closed /home/tk/wuhao_search/corpus/ohsumed/0013377
0:00: Closing index
0:00: Finished
```

Run a test query
```sh
$ cd ../runquery/
$ ./IndriRunQuery test-query.xml ../parameters.xml 
kstem_add_table_entry: Duplicate word emeritus will be ignored.
-7.11437        /home/tk/wuhao_search/corpus/ohsumed/0010927    0       97
-7.76151        /home/tk/wuhao_search/corpus/ohsumed/0017950    0       112
-7.8206 /home/tk/wuhao_search/corpus/ohsumed/0016765    0       271
```
where `test-query.xml` is a query file (you should create it) which in here it specifies a single query keyword *dog*:
```
<parameters>
        <query>
                <number>1</number>
                <text>food imports</text>
        </query>
</parameters>
```

### Fix segmentation fault in newer GCC version
It seems after gcc version 7.2 (in my case gcc 8.2.1, see this [thread](https://sourceforge.net/p/lemur/bugs/299)) the default build configuration of Indri will cause segmentation fault when you do indexing.
The issue is caused by gcc performing vectorization on trees, this optimization
trick somehow causes trouble (see [this issue](https://jira.mongodb.org/browse/SERVER-13824?focusedCommentId=660868&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-660868), but not sure if it is the same reason).

> Note that the loop has been vectorized to use the xmm registers using the movdqa instruction. From the intel arch documentation: "When the source or destination operand is a memory operand, the operand must be aligned on a 16-byte boundary or a general-protection exception (#GP) will be generated." 
> 
> (extracted from that issue)

To fix it, edit `MakeDefns` file (after running `./configure`) and add `-fno-tree-vectorize` to `CFLAGS` and `CXXFLAGS`:
```sh
...
# C compiler and compiling options
# C++ compiler and compiling/linking options
CFLAGS = -DPACKAGE_NAME=\"Indri\" ... (omitted many here) .... -fno-tree-vectorize
CXXFLAGS = -DPACKAGE_NAME=\"Indri\" ... (omitted many here) .... -fno-tree-vectorize
...
```
then issue `make clean` and `make` again. Do not forget to also re-build Approach Zero afterwards.

### Install LaTeXML
If `TEX_PARSER_USE_LATEXML` is defined in `tex-parser/config.h`, you are required to install LaTeXML. LaTeXML helps Approach Zero parser to handle LaTeX markups that are either ambiguous or unrecognized by built-in parser.

You may observe the following warning if LaTeXML is needed
> I/O warning : failed to load external entity "math.xml.tmp"

To test if LaTeXML is available 
```bash
$ /usr/bin/latexmlmath
-bash: /usr/bin/latexmlmath: No such file or directory
```

To install LaTeXML,
```bash
$ sudo apt install libxslt-dev libxml-libxslt-perl # for Debian buster
$ git clone --depth=1 https://github.com/brucemiller/LaTeXML
$ cd LaTeXML
$ perl Makefile.PL
$ sudo cpanm .
$ make
$ sudo make install
$ sudo ln -s `which latexmlmath` /usr/bin/latexmlmath
```

As a test after installation, you can issue the following to generate representational and content mathML using LaTeXML,
```bash
echo 'a+b' | latexmlmath --presentationmathml=representation.xml -
echo 'a+b' | latexmlmath --contentmathml=content.xml -
```
Corresponding xml file will be generated under current directory.

If you get the following error, try to downgrade your perl to version 5.28. (My brucemiller/LaTeXML version is `22db863d7358d56e197a3845375775714577cc82`)
```bash
LibXML.c: loadable library and perl binaries are mismatched (got handshake key 0xce00080, need
ed 0xcd00080)
```

For convenience, we have made this particular version of MathML available on DockerHub, to start:
```bash
$ apt-get update
$ which docker || curl -fsSL https://get.docker.com -o get-docker.sh
$ which docker || sh get-docker.sh
$ docker pull approach0/latexml:22db863d7358d56e197a3845375775714577cc82
$ docker tag approach0/latexml:22db863d7358d56e197a3845375775714577cc82 latexml:latest
$ docker run latexml /usr/bin/latexmlmath --help
$ cat  <<-EOF > /usr/bin/latexmlmath
#!/bin/sh
OUTDIR=\$(pwd)
docker run -v \$OUTDIR:/tmp --workdir="/tmp" latexml /usr/bin/latexmlmath \$@
EOF
$ chmod +x /usr/bin/latexmlmath
$ latexmlmath --VERSION
latexmlmath (LaTeXML version 0.8.3; revision 22db863d)
```

### MPI mechanism
Here is a short note on the mechanism behind MPI which Approach Zero uses to scale out search instances.

> Unless you are running under a (supported) resource manager (such as Slurm, PBS or other), the plm/rsh component will be used to start the MPI app.
> Long story short, Open MPI uses a distributed virtual machine (DVM) to launch the MPI tasks. The first step is to have one daemon per node. The initial "daemon" is mpirun, and then one orted daemon have to be remotely spawned on each other node, and this is where plm/rsh uses SSH.
> By default, if you are running on less than 64 nodes, then mpirun will SSH to all the other nodes. But if you are running on a larger number of nodes, then mpirun will use a tree spawn algorithm, in which other nodes might ssh to other nodes. Bottom line, if you are using ssh with Open MPI, and unless you are running on a small cluster with default settings, all nodes should be able to ssh passwordless to all nodes.

reference: [https://stackoverflow.com/questions/48893146](https://stackoverflow.com/questions/48893146)

### Anaconda Environment
[Anaconda](https://www.anaconda.com/products/individual) is a favored way to install Python environment without system-wise permission, and you can have a convenient virtual environment that is easy to install and switch between different Python versions.

Here is a short note on how to install Anaconda environment:
```sh
$ wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
$ chmod +x Anaconda3-2020.11-Linux-x86_64.sh && ./Anaconda3-2020.11-Linux-x86_64.sh
$ eval "$(/home/`whoami`/anaconda3/bin/conda shell.bash hook)"
$ conda create --name py38 python=3.8
$ conda activate py38
$ python -V
Python 3.8.8
$ pip -V
pip 21.0.1 from /home/w32zhong/anaconda3/envs/py38/lib/python3.8/site-packages/pip (python 3.8)
```

When a `python setup.py install` is needed, you can instead issue `pip install .`.

Anaconda can also be used to create a C/C++ build environment:
```sh
$ conda install gcc_linux-64
$ conda install gxx_linux-64
$ conda install -c anaconda make
$ conda upgrade -c conda-forge --all
$ echo $CC; echo $CXX
/home/YOUR_USER_NAME_HERE/anaconda3/envs/py38/bin/x86_64-conda_cos6-linux-gnu-cc
/home/YOUR_USER_NAME_HERE/anaconda3/envs/py38/bin/x86_64-conda_cos6-linux-gnu-c++
$ export LD_LIBRARY_PATH=$(dirname $CXX)/../lib
```

Some other required libraries and binaries:
```sh
$ conda install zlib icu libevent
$ conda install flex bison
$ conda install -c conda-forge openmpi # use openmpi=4.1.2 if libmpi.so is not found (conda-forge package bug)
$ conda install -c anaconda libxml2
```

To switch compiling with system environment and Anaconda environment, use `conda deactivate` or `conda activate`
```sh
$ conda deactivate
$ xml2-config --libs
-lxml2 -lz -llzma -licui18n -licuuc -licudata -lm -ldl
$ conda activate
$ xml2-config --libs
-L/home/tk/anaconda3/lib -lxml2 -L/home/tk/anaconda3/lib -lz -L/home/tk/anaconda3/lib -llzma -lpthread -L/home/tk/anaconda3/lib -L/home/tk/anaconda3/lib -licui18n -licuuc -licudata -lm -ldl
```
