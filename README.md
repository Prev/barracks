# Barracks &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Prev/barracks/blob/master/LICENSE) [![Coverage Status](https://coveralls.io/repos/github/Prev/barracks/badge.svg)](https://coveralls.io/github/Prev/barracks)  [![Build Status](https://travis-ci.org/Prev/barracks.svg)](https://travis-ci.org/Prev/barracks)

Simple file storing util for reading & writing series of data for data mining.


### Basic usage

You can easily use `Barracks` like key-value store.

```python
from barracks import Barracks

b = Barracks('data')
b.set(1, 'my data')
print(b.get(1))
# 'my data'

b.set(2, 222)
print(b.get(2))
# 222

b.set(3, {'foo': 'bar'})
print(b.get(3)['foo'])
# 'bar'

```

## Automatic chunk management

With `Barracks`, you don't have to concern about memory overflow,
because `Barracks` divide files automatically to `Chunks` per chunk size.
`Barracks` only load one `Chunk` at once, loading another `Chunk` is executed if chunk's ID is changed.

Chunk's ID is determined based on the key,
so if iterating 100,000 objects for chunksize=10,000,
chunk will be changed only 10 times on whole iteration.


On data mining, there are many **situations to load series of data**,
but codes to load and process these data is not that simple (dirty code to chunk data).

With this util, code will be turned really **simple**, with **no overhead**.


```python
# For huge amount of data

from barracks import Barracks

b = Barracks('data')

for i in range(0, 100000):
	b.set(i, str(i))

for chunk in b.chunks():
	for key, value in chunk.items():
		print(key, value)
```


## Compression

All chunk files is saved with compression.

We use [lz4](https://github.com/lz4/lz4), which is extremely fast compression algorithm,
so it is perfectly fit to manage **training data/pre-processed data**, which are used occasionally,
rather than in real-time-service.


## Optimized for serial reading, but search is also available

Although `Barracks` aimed to sequential reading/writing,
but search is also available.

It searches `key` from the current `buffer pointer` until looping all keys in that chunk.  
So best case for searching is O(1) when finding item next to previous one,
and worst case is O(chunksize) when finding reverse order.  

Usage for search and getting next item is not different.
There might be some **exceptions on sequential reading** (like *missing data*),
but you can easily deal with these exceptions using `Barracks` .

```python
from barracks import Barracks

b = Barracks('data')

for key in range(10001, 20000):
	b.set(key, some_data_from_training[key])

b.get(10001)
b.get(10002)
# Skip 10003
b.get(10004) # Skip 1 line, No problem!
b.get(10010) # Skip 5 lines, No problem!
```

## How to Install

Install via pypi

```bash
$ pip install barracks
```

## License

[MIT](https://github.com/Prev/barracks/blob/master/LICENSE) License