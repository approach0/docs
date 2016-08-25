## Indices in a File Image
Since our math indexer creates a large amount of directories and
files on disk proportionally to the number of expressions you are
going to index.
If you are using a typical file system on Linux, e.g. EXT4, you are
limited to create so many directories/files by the number of inodes
on your file system.

To overcome this problem, as well as improve efficiency of math index,
it is better to create a disk image as a loopback device to be
partitioned by some file systems which do not put restriction on inodes.
The file system should be efficient in crucial aspects of benchmarks that
have great impact on search performance. Later, we can simply mount this
disk image to be used as our index "disk".

After some investigation, we choose to use ReiserFS as our default index
file system due to its overall fast sequential read and random seek
(see
[ref1](http://girlyngeek.blogspot.com/2011/04/ultimate-linux-filesystems-benchmark.html)
and
[ref2](https://debian-administration.org/article/388/Filesystems_ext3_reiser_xfs_jfs_comparison_on_Debian_Etch)
).

To create, mount and unmount a ReiserFS disk image, we provide a few simple
scripts located under `$PROJECT/indexer/scripts`. Creating and mounting a
disk image are simple as follows:

```sh
$ cd $PROJECT/indexer
$ ./scripts/vdisk-creat.sh
$ sudo ./scripts/vdisk-mount.sh `whoami` ./tmp
```
A `vdisk.img` is created as our ReiserFS disk image, and is mounted to
`./tmp` so we can just use indexer and searcher on `./tmp` like a
normal directory.

After you are done, unmount `./tmp`:
```sh
$ sudo ./scripts/vdisk-umount.sh
```

### Some notices

### 1. Lacking kernel support for ReiserFS
If you are running on Ubuntu 16.04, where kernel does not support ReiserFS, modify scripts above
and change file system to `btrfs` for similar performance.

### 2. `dd` command reports exhausted memory
When you experience `dd` command not being able to create certain size of image file:

```sh
dd: memory exhausted by input buffer of size 1073741824 bytes (1.0 GiB)
```
Try either reduce the `bs` argument number of `dd`, or use a disk swap file:
```
dd if=/dev/zero of=/swapspace bs=1M count=4000
mkswap /swapspace
swapon /swapspace
```
