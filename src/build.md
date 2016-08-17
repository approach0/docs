## Build

### 0. Clone source code:
```sh
$ git clone --depth=1 https://github.com/approach0/search-engine.git
```
The following instructions assume you have cloned this project in to directory `$PROJECT`.

### 1. Install dependencies
Other than commonly system build-in libraries (pthread, libz, libm, libstdc++), ther are some external dependencies you may need to download and install on your system environment:

* [bison](http://ftp.gnu.org/gnu/bison/bison-3.0.tar.xz)
* [flex and libfl](http://sourceforge.net/projects/flex/files/flex-2.5.39.tar.xz/download)
* [libz](http://zlib.net/zlib-1.2.8.tar.gz)
* [Lemur/Indri](https://sourceforge.net/projects/lemur/files/lemur/indri-5.9/indri-5.9.tar.gz/download)
* [libevent](https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz)

For Ubuntu 16.04 LTS (xenial), type the following commands to install above dependencies (including essential programs):
```sh
$ sudo apt-get update
$ sudo apt-get g++ cmake
$ sudo apt-get install bison flex libz-dev libevent-dev
```
Lemur/Indri is not likely to be in your distribution's official software repository, so you may need to build and manually specify its library path (see the next step).

Lemur/Indri library is an important dependency for this project, currently this project relies on it to provide full-text index functionality (including index writer and reader).
Thus we avoid reinventing the wheel, and we can focus on math search implementation. To combine two search engines, simply merge their results and weight their scores accordingly.

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

### 2. Configure dependency path
Our project uses `dep-*.mk` files to configure most C/C++ dependency paths (or CFLAGS and LDFLAGS). If you have installed above dependency libraries in your system environment, you can leave these `dep-*.mk` files untouched.

One dependency path you probably have to specify manually is the Lemur/Indri library. If you have downloaded and compiled Lemur/Indri source code at `~/indri-5.9`, type:

```
$ cd $PROJECT
$ ./configure --indri-path=~/indri-5.9
```
to setup build configuration. This `configure` script also checks necessary libraries for building. If `configure` outputs any library that can not be located by the linker, you may need to install the missing dependency before build.

### 3. Build
Type `make` at project top level (i.e. `$PROJECT`) will do the job.
