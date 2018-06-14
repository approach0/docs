## Internals
Some old papers/posters describe in detail what our search
methods are. You may find useful to read these resources first:

1. [ECIR16 Slides](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-OPMES-slides-handouts.pdf)
2. [ECIR16 Poster](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/ECIR16-Wei-Poster-publish.pdf)
3. [ECIR16 Paper](https://github.com/tkhost/tkhost.github.io/blob/master/opmes/ecir2016.pdf)
4. [My graduate thesis](https://github.com/tkhost/tkhost.github.io/raw/master/opmes/thesis-ref.pdf)

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
	field[k][...]
};

def: size(doc[i], j) = the size of field j of doc[i]

alloc: codec buffers:
arr[0] using codec method[0]
arr[1] using codec method[1]
...
arr[k] using codec method[k]

/*
 * Compression
 */
input: buf[n docs]
output: payload
for i < n:
	for j < k:
		arr[j].pos += copy(arr[j][arr[j].pos], buf[i].j, len = size(buf[i], j))

cur = 0
payload[cur] = n
for j < k:
	cur += codec_compress_ints(method[j], in = arr[j], len = arr[j].len, out = payload + cur)

/*
 * Decompression
 */
input: payload
output: buf[n docs]
cur = 0
n = payload[cur]
for j < k:
	cur += codec_decompress_ints(method[j], in = payload + cur, len = arr[j].len, out = arr[j])

for i < n:
	for j < k:
		arr[j].pos += copy(buf[i].j, arr[j][arr[j].pos], len = size(buf[i], j))
```
