## Build

### 0. Clone source code:
```sh
$ git clone --depth=1 https://github.com/approach0/search-engine.git
```
The following instructions assume you have cloned this project in to directory `$PROJECT`.

### 1. Install system dependencies
Other than commonly build-in libraries (pthread, libz, libm, libstdc++), ther are some system dependencies you may need to download and install on your system environment:

* [bison](http://ftp.gnu.org/gnu/bison/bison-3.0.tar.xz)
* [flex and libfl](http://sourceforge.net/projects/flex/files/flex-2.5.39.tar.xz/download)
* [libz](http://zlib.net/zlib-1.2.8.tar.gz)
* [libevent](https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz)

For Ubuntu 16.04 LTS (xenial), type the following commands to install above dependencies (including essential programs):
```sh
$ sudo apt-get update
$ sudo apt-get install g++ cmake
$ sudo apt-get install bison flex libz-dev libevent-dev
```
### 2. Download and build Indri
This project currently relies on [Lemur/Indri](http://www.lemurproject.org/indri.php)
library as dependency to provide full-text index functionality (i.e. index writer and reader),
this helps us focus on math search implementation.
To combine math and full-text search, we merge the results from Indri index reader and those
from math search, weight them using some combined score schema. (Very high level idea)

Lemur/Indri is not likely to be in your distribution's official software repository,
so you may need to build and manually specify its library path.

Download and decompress Indri tarball (indri-5.11 is recommended), build its libraries:

```sh
$ cd ~
$ wget 'https://sourceforge.net/projects/lemur/files/lemur/indri-5.11/indri-5.11.tar.gz/download' -O indri.tar.gz
$ tar -xzf indri.tar.gz
$ (cd indri-5.11 && chmod +x configure && ./configure && make)
```

If Indri reports `undefined reference to ...` when building/linking, install that library **and** run configure again:

> After installing the zlib-devel package you must rerun configure
> so that it correctly finds it and adds the library to the ld command.
	
> (https://sourceforge.net/p/lemur/discussion/546028/thread/e67752b2)

Also, if you build Indri with newer version of gcc, it may produce segmentation fault when doing text indexing. Please refer to [Appendix](appendix_indri.html#fix-segmentation-fault-in-newer-gcc-version) to resolve the issue.

### 3. Download CppJieba
Our indexer/searcher is able to handle English and Chinese document. Here
[CppJieba](https://github.com/yanyiwu/cppjieba) provides us Chinese term segmentation functionality.
Although we have option to choose whether or not to invoke this functionality when calling
indexer/searcher programs, CppJieba is still required at compile time (at least for now) to
successfully build this project.

We do not need to build CppJieba since using the header files of this C++ project is sufficient.
```sh
$ cd ~
$ wget 'https://github.com/yanyiwu/cppjieba/archive/v4.8.1.tar.gz' -O cppjieba.tar.gz
$ mkdir -p ~/cppjieba
$ tar -xzf cppjieba.tar.gz -C ~/cppjieba --strip-components=1
```

### 4. Configure dependency path
Our project uses `dep-*.mk` files to configure most C/C++ dependency paths (or CFLAGS and LDFLAGS). If you have installed above dependency libraries in your system environment, you can leave these `dep-*.mk` files untouched. Otherwise if you compile and build dependencies locally, please modify `dep-*.mk` files to point to your locally built library locations.

If you followed the above instruction and downloaded (and compiled) Lemur/Indri and CppJieba project at `$HOME` address, just type:

```
$ cd $PROJECT
$ ./configure
```

If Lemur/Indri and CppJieba project are downloaded to paths other than the `$HOME` path used above, you have to manually specify them:

```
$ cd $PROJECT
$ ./configure --indri-path=~/indri-5.11 --jieba-path=~/cppjieba
```

This `configure` script also checks necessary libraries for building. If `configure` outputs any library that can not be located by the linker, you may need to install the missing dependency before build.

### 5. Build
Type `make` at project top level (i.e. `$PROJECT`) will do the job.

### 6. LaTeXML
You may also need to install LaTeXML depending on your build configuration. Please refer to [Appendix](appendix_indri.html#install-latexml) for instructions.
