## Internals
Some old papers/posters describe in detail what our search
methods are. You may find useful to read these resources first:

1. [ECIR16 Slides](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-OPMES-slides-handouts.pdf)
2. [ECIR16 Poster](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-Wei-Poster-publish.pdf)
3. [ECIR16 Demo](https://github.com/tkhost/tkhost.github.io/blob/master/opmes/ecir2016.pdf)
4. [My graduate thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf)
5. [ECIR19 Paper - Structure search model](https://ecir2019.org/accepted-papers/)

Although Approach0 is a complete rewrite based on previous
prototype (OPMES), the basic ideas of searching math expression
remain unchanged in both systems. Approach0 mainly makes an advance
in the following aspects on top of OPMES:

1. Combine math-only search with fulltext search
2. Adds some feature (e.g. math expression wildcards)
3. Better code framework

### Math posting list structure
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
