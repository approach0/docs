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
* [openmpi](https://download.open-mpi.org/release/open-mpi/v2.0/openmpi-2.0.2.tar.bz2)

For Ubuntu 16.04 LTS (xenial), issue the following commands to install above dependencies:
```sh
$ sudo apt-get update
$ sudo apt-get install g++ cmake
$ sudo apt-get install bison flex libz-dev libevent-dev libopenmpi-dev
```

On Debian 9 for example, you may also need to install
```sh
$ sudo apt install libxml2-dev
```

### 2. Download and build Indri
This project currently relies on [Lemur/Indri](http://www.lemurproject.org/indri.php)
library to provide full-text index functionality (i.e. index writer and reader).
To combine math and full-text search, we merge the results from Indri index reader and those
from our math search, weight them using some combined score schema.

Lemur/Indri is not likely to be in your distribution's official software repository,
so you may need to build and manually specify its library path.

Build Indri:
```sh
$ cd ~
$ git clone https://github.com/approach0/fork-indri.git ./indri
$ (cd indri && ./configure && make)
```

If Indri reports `undefined reference to ...` when building/linking, install that library **and** run configure again:

> After installing the zlib-devel package you must rerun configure
> so that it correctly finds it and adds the library to the ld command.
	
> (https://sourceforge.net/p/lemur/discussion/546028/thread/e67752b2)

Also, if you build Indri with newer version of gcc, it may produce segmentation fault when doing text indexing. Please refer to [Appendix](appendix_indri.html#fix-segmentation-fault-in-newer-gcc-version) to resolve the issue.

### 3. Download CppJieba
Our indexer/searcher is able to handle English and Chinese document. Here
[CppJieba](https://github.com/yanyiwu/cppjieba) dependency enables Chinese term segmentation.
Although we have option to choose whether or not to invoke this functionality when calling
indexer/searcher programs, CppJieba is still required at compile time (at least for now) to
successfully build this project.

However, there is no need to build CppJieba source code, only its C++ header files are required.
```sh
$ cd ~
$ git clone git@github.com:approach0/fork-cppjieba.git cppjieba
```

If you encounter this error:
```
cppjieba/deps/limonp/StdExtension.hpp:19:17: error: 'template<class _Key, class _Tp, class _Hash, class _Pred, class _Alloc> class std::tr1::unordered_map' conflicts with a previous declaration
   19 | using std::tr1::unordered_map;
      |                 ^~~~~~~~~~~~~
```
then edit `cppjieba/deps/limonp/StdExtension.hpp`:
```diff
diff --git a/deps/limonp/StdExtension.hpp b/deps/limonp/StdExtension.hpp
index 098a268..d304e28 100644
--- a/deps/limonp/StdExtension.hpp
+++ b/deps/limonp/StdExtension.hpp
@@ -13,11 +13,8 @@
 #include <unordered_map>
 #include <unordered_set>
 #else
-#include <tr1/unordered_map>
-#include <tr1/unordered_set>
-namespace std {
-using std::tr1::unordered_map;
-using std::tr1::unordered_set;
+#include <unordered_map>
+#include <unordered_set>
#endif
```


### 4. Configure dependency path
Our project uses `dep-*.mk` files to configure most C/C++ dependency paths (such as CFLAGS and LDFLAGS). If you have installed above dependency libraries in your system environment, you can leave these `dep-*.mk` files untouched. Otherwise if you compile and build dependencies locally, please modify `dep-*.mk` files to point to your locally built library locations.

Before building, you need to invoke `./configure` to locate all external dependencies:
```
$ cd $PROJECT
$ ./configure --indri-path=~/indri --jieba-path=~/cppjieba
```

This `configure` script also checks necessary libraries for building. If `configure` outputs any library that can not be located by the linker, you may need to install the missing dependency before build.

### 5. Build
Issue `make` at project top level (i.e. `$PROJECT`) will do the job.

### 6. LaTeXML (optional)
You may also need to install LaTeXML depending on your build configuration. Please refer to [Appendix](appendix_indri.html#install-latexml) for instructions.
