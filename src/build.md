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
$ sudo apt-get g++ cmake
$ sudo apt-get install bison flex libz-dev libevent-dev
```
### 2. Download and build Indri
This project currently relies on [Lemur/Indri](http://www.lemurproject.org/indri.php)
library as dependency to provide full-text index functionality (i.e. index writer and reader).
Thus we avoid reinventing the wheel, and we can focus on math search implementation.
To combine math and full-text search, we merge their results and weight them using
a some combined score schema.

Lemur/Indri is not likely to be in your distribution's official software repository,
so you may need to build and manually specify its library path:

Download and decompress Indri tarball (indri-5.9 for example), build its libraries:

```sh
$ cd ~
$ wget 'https://sourceforge.net/projects/lemur/files/lemur/indri-5.9/indri-5.9.tar.gz/download' -O indri-5.9.tar.gz
$ tar -xzf indri-5.9.tar.gz
$ (cd indri-5.9 && chmod +x configure && ./configure && make)
```

If Indri reports `undefined reference to ...` when building/linking, install that library **and** rerun configure again:

> After installing the zlib-devel package you must rerun configure
> so that it correctly finds it and adds the library to the ld command.
	
> (see https://sourceforge.net/p/lemur/discussion/546028/thread/e67752b2)

### 2. Download CppJieba
[CppJieba](https://github.com/yanyiwu/cppjieba) provides us Chinese term segmentation functionality.
Although we have option to choose whether or not to invoke this functionality when calling
indexer/searcher programs, CppJieba is still required at compile time (at least for now) to
successfully build this project.

We do not need to build CppJieba since using the header files of this C++ project is sufficient.
```sh
$ cd ~
$ wget 'https://github.com/yanyiwu/cppjieba/archive/v4.8.1.tar.gz' -O cppjieba.tar.gz
$ tar -xzf cppjieba.tar.gz
```

### 3. Configure dependency path
Our project uses `dep-*.mk` files to configure most C/C++ dependency paths (or CFLAGS and LDFLAGS). If you have installed above dependency libraries in your system environment, you can leave these `dep-*.mk` files untouched.

If you followed the above instruction and downloaded (and compiled) Lemur/Indri and CppJieba project at `$HOME` address, just type:

```
$ cd $PROJECT
$ ./configure
```

Alternatively, if Lemur/Indri and CppJieba project are downloaded elsewhere, you have to manually specify their paths:

```
$ cd $PROJECT
$ ./configure --indri-path=~/indri-5.9 --jieba-path=~/cppjieba
```

This `configure` script also checks necessary libraries for building. If `configure` outputs any library that can not be located by the linker, you may need to install the missing dependency before build.

### 3. Build
Type `make` at project top level (i.e. `$PROJECT`) will do the job.
