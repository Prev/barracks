# Barracks &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Prev/barracks/blob/master/LICENSE) [![Coverage Status](https://coveralls.io/repos/github/Prev/barracks/badge.svg)](https://coveralls.io/github/Prev/barracks)  [![Build Status](https://travis-ci.org/Prev/barracks.svg)](https://travis-ci.org/Prev/barracks)

Simple file storing util for reading & writing series of data for data mining.


## Automatic chunk management

With `Barracks`, you don't have to concern about memory overflow,
because `Barracks` divide files automatically to `Chunks` per chunk size.

`Barracks` only load one `Chunk` at once, load another `Chunk` if chunk's ID is changed,
and the chunk's ID is determined based on the key.

For example, keys 1 through 10000 have the same chunk ID,
so while reading and writing these chunks, new chunk would not be loaded.  
When the key becomes 10001, then the chunk changes,
and the chunk would not be changed again until the key becomes 20001.

---

On data mining, especially training data, there are many **situations to load series of data**,
but codes to load and process these data is not that simple (Be dirty).

With this util, **designed to read data serially**, code will be turned really simple, with no overhead.


## Compression

All chunk files is saved after compressing.

We use [lz4](https://github.com/lz4/lz4), which is extremely fast compression algorithm,
so it is perfectly fit to manage **training data/pre-processed data**, which are used occasionally,
rather than in real-time-service.


## Usage

### Basic usage
We can easily use this like key-value store.

```python
from barracks import Barracks

b = Barracks('data')
b.set(1, 'my data')
assert b.get(1) == 'my data'

b.set(2, 222)
assert b.get(2) == 222
```


#### For huge amount of data

```python
from barracks import Barracks

b = Barracks('data')

for i in range(0, 100000):
	b.set(i, str(i))

for chunk in b.chunks():
	for key, value in chunk.items():
		print(key, value)
```

