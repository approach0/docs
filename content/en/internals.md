## Internals
Some old papers/posters describe in detail what our search
methods are. You may find useful to read these resources first:

1. [ECIR16 Slides](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-OPMES-slides-handouts.pdf)
2. [ECIR16 Poster](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-Wei-Poster-publish.pdf)
3. [ECIR16 Demo](https://github.com/tkhost/tkhost.github.io/blob/master/opmes/ecir2016.pdf)
4. [Master thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf)
5. [ECIR19 Paper - Structure search model](https://ecir2019.org/accepted-papers/)
6. [ECIR20 Paper - Formula query efficiency](https://drive.google.com/open?id=1QjKVpgsTAIMLqrIDhdDOHvDa7sLvoxq7)

### TeX Parser
TeX parser converts TeX to Operator Tree (or OPT) and leaf-root paths. There are many details involved, among them
* Each node in OPT will be assigned a ID in a way that leaf nodes always occupy lower space
* Each node in OPT will save its position [start, end] information from original TeX string
* Fingerprint (or `fp`) is generated for each leaf-root path
* A subtree Hash is generated for each subtree
* A pathID and a leafID (starting from 1) are generated for each path, initially they are the same
* Max pathID/leafID is also the number of leaf-root paths here, they are no greater than MAX_SUBPATH_ID = 64
* Any nil node will be pruned

The following is an example output for expression `$a+bc=$` (notice the RHS has nothing so it will reduce into nil)
```
edit: a+bc=
return string: no error (max path ID = 3).
return code: 0
Operator tree:
     └──(equal) #4, token=GTLS, subtr_hash=`55144', pos=[0, 4].
           └──(plus) #5, token=ADD, subtr_hash=`64808', pos=[0, 4].
                 │──(pos) #6, token=SIGN, subtr_hash=`26696', pos=[0, 1].
                 │     └──(hanger) #7, token=HANGER, subtr_hash=`4808', pos=[0, 1].
                 │           └──(base) #8, token=BASE, subtr_hash=`1160', pos=[0, 1].
                 │                 └──[normal`a'] #1, token=VAR, subtr_hash=`a', pos=[0, 1].
                 └──(pos) #9, token=SIGN, subtr_hash=`38088', pos=[2, 4].
                       └──(times) #10, token=TIMES, subtr_hash=`46408', pos=[2, 4].
                             │──(hanger) #11, token=HANGER, subtr_hash=`4820', pos=[2, 3].
                             │     └──(base) #12, token=BASE, subtr_hash=`1164', pos=[2, 3].
                             │           └──[normal`b'] #2, token=VAR, subtr_hash=`b', pos=[2, 3].
                             └──(hanger) #13, token=HANGER, subtr_hash=`4832', pos=[3, 4].
                                   └──(base) #14, token=BASE, subtr_hash=`1168', pos=[3, 4].
                                         └──[normal`c'] #3, token=VAR, subtr_hash=`c', pos=[3, 4].

6 leaf-root paths
- [path#1, leaf#1] normal`a': VAR(#1)/BASE(#8)/HANGER(#7)/SIGN(#6)/ADD(#5)/GTLS(#4) (fp 3552)
- [path#2, leaf#2] normal`b': VAR(#2)/BASE(#12)/HANGER(#11)/TIMES(#10)/SIGN(#9)/ADD(#5)/GTLS(#4) (fp 5552)
- [path#3, leaf#3] normal`c': VAR(#3)/BASE(#14)/HANGER(#13)/TIMES(#10)/SIGN(#9)/ADD(#5)/GTLS(#4) (fp 5552)
```

### Math posting list structure
Here is the pseudo C code showing our inverted list item structure
```c
/* math inverted list items */
struct math_invlist_item {
	/* 8-byte global key */
	uint32_t docID; /* 4 bytes */
	union {
		uint32_t secID;
		struct {
			uint16_t sect_root;
			uint16_t expID;
		};
	}; /* 4 bytes */

	uint8_t  sect_width;
	uint8_t  orig_width;
	/* padding 16 bits here */
	uint32_t symbinfo_offset; /* pointing to symbinfo file offset */
	/* 4 bytes */
}; /* 4 x 4 = 16 bytes in total */

#define MAX_INDEX_EXP_SYMBOL_SPLITS 8

struct symbsplt {
	uint16_t symbol;
	uint8_t  splt_w;
};

struct symbinfo {
	uint32_t ophash:24;
	uint32_t n_splits:8;

	struct symbsplt split[MAX_INDEX_EXP_SYMBOL_SPLITS];
};
```

(more to be written here...)
