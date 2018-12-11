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

The data structure details of posting list are written in the next section,
other technical details are not included in this document, but you are welcome to request in project issue page for more specific technical issues.

### Posting list structure
There are two different posting lists, `math posting list` and `term posting list`. A `math posting list` is mapped from a path token from tree representation of a math expression, e.g. VAR/ADD/TIMES. A `term posting list` is mapped from a text word from dictionary. Both posting list is concatenation of posting list items.

The data structure for term posting list item is divided into on-disk and in-memory (cached) posting list.
Indri takes care of on-disk term posting list and approach0 just calls Indri's API to get posting list items when needed.

The in-memory posting list item for terms is defined like below (each square bracket is a 32-bit field):

[docID][TF][pos_1][pos_2]...[pos_TF]

The math posting list currently only has on-disk version, its posting list item looks like below:

[expID, n_lr_paths, n_paths], [docID], [pathInfo pointer]

where pathInfo points to another posting list that stores additional information array for that item:

[leaf_id], [subr_id], [lf_symbol] ... (repeating `n_paths` times)

### Posting list compression
Take in-memory term posting list as example. Limited to free continous memroy space, we first have to divide a posting list into many trunks. And to achieve good compression rate, we put the values from same field together and compress them. Because the same fields of consecutive values is a good input for delta compression.

The compression takes place like this: First allocate several arrays to store corresponding field values, in term posting list case, there are docID_array, TF_array and pos_array. Assuming the number of items in a trunk is *n*, then the compressed trunk structure looks like this:

[n], compressed(docID_array), compressed(TF_array), compressed(pos_array).

The head value (one byte) is required otherwise at decompression you do not know how many value to extract/decompress. And the number of pos_array values to extract/decompress is calucated by summing the TF values.

The pseudo code for compression and decompression is given below.
```c
struct doc {
	field[0]
	field[1]
	...
	field[k] --> [...] (some of the fields may be a pointer to a consequtive allocated space)
};

A set of callback functions:
field_num() = the number of fields of doc structure
field_ptr(struct_addr, j) = the pointer of field j
field_size(doc[i], j) = the size of field j of doc[i]
field_codec(j) = the code/decode method of field j

allocate codec buffers (each has size/position inforamtion):
arr[0]
arr[1]
...
arr[k]

/*
 * Compression
 */
input: structure buffer doc[n]
output: posting buffer

for i < n:
	struct doc *cur = field_ptr(doc + i, 0)
	for j < field_num():
		sz = field_size(cur, j)
		/* need to make sure arr has enough free space here */
		memcpy(arr[j] + arr[j].pos, field_ptr(doc + i, j), sz)
		arr[j].pos += sz

for j < field_num():
	num = arr[j].size / sizeof(int)
	posting[posting.pos ++] = num
	/* need to make sure posting has enough free space here */
	posting.pos += compress_ints(field_codec(j), posting + posting.pos, arr[j], num)

/*
 * Decompression
 */
input: posting buffer
output: structure buffer doc[n]

for j < field_num():
	num = posting[posting.pos ++]
	posting.pos += decompress_ints(field_codec(j), arr[j], posting + posting.pos, num)

for i < n:
	struct doc *cur = field_ptr(doc + i, 0)
	for j < field_num():
		sz = field_size(cur, j)
		memcpy(field_ptr(doc + i, j), arr[j] + arr[j].pos, sz)
		arr[j].pos += sz
```
