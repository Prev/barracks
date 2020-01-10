from barracks import Barracks, __version__
import pytest
import os

DIRNAME = 'datadir'


@pytest.fixture
def clear_before():
	if os.path.isdir(DIRNAME):
		for file in os.listdir(DIRNAME):
			os.remove(os.path.join(DIRNAME, file))


def test_integers(clear_before):
	with Barracks(DIRNAME) as b:
		assert b.get(1) is None
		assert b.get(2) is None

		b.set(1, 1)
		assert b.get(2) is None

		b.set(2, 2)
		b.set(3, 3)
		assert b.get(2) == 2
		assert b.get(3) == 3

		b.set(5, 5)
		assert b.get(2) == 2
		assert b.get(1) == 1

		b.set(6, 6)
		assert b.get(6) == 6


def test_no_compressor(clear_before):
	with Barracks(DIRNAME, compressor=None) as b:
		assert b.get(1) is None

		b.set(1, 1)
		assert b.get(2) is None

		b.set(2, 2)
		b.set(3, 3)
		assert b.get(2) == 2
		assert b.get(3) == 3


def test_strings(clear_before):
	with Barracks(DIRNAME) as b:
		b.set(1131, 'hello')
		assert b.get(1131) == 'hello'

		b.set(4131, 'world')
		assert b.get(4131) == 'world'


def test_header(clear_before):
	with Barracks(DIRNAME) as b:
		b.set(1, 1)

		assert b.getchunk(1, 'r').header['_version'] == __version__


def test_many(clear_before):
	with Barracks(DIRNAME) as b:
		for i in range(0, 100000):
			b.set(i, 'a%d' % i)

		for i in range(0, 100000):
			if i % 4 == 0:
				assert b.get(i) == ('a%d' % i)

		for chunk in b.chunks():
			base_key = chunk.id * 10000
			i = 0
			for key, value in chunk.items():
				assert key == base_key + i
				assert value == 'a%d' % (base_key + i)
				i += 1