# Barracks

Simple file storing util for a series of data.

  

With `Barracks`, you don't have to concern about memory overflow,
because `Barracks` divide files automatically to `Chunks` per chunk size.

`Barracks` only load one `Chunk` at once, and load another `Chunk` if chunk's ID is changed,
and the chunk's ID is determined based on the key.

For example, keys 1 through 10000 have the same chunk ID,
so while reading and writing these chunks, the chunks are not loaded and used as is.

Then, when the key becomes 10001, the chunk changes
and the chunk does not change again until the key becomes 20001,
so **loading series of data is executed with no overhead, but code is turned really simple.**


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

