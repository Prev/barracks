"""
barracks
-----------------
Simple file storing util for a series of data

:author: Prev(prevdev@gmail.com)
:license: MIT
"""

import os
import io
import json
import lz4.frame

__version__ = '0.1.0'


class Barracks:

	def __init__(self, dirname, chucksize=10000, compressor='lz4'):
		""" Initialize Barracks instance
		:param dirname: Directory name to save data
		:param chucksize: Maximum length of items per chunk
		"""
		self.dirname = dirname
		self.chucksize = chucksize
		self.cur_chunk = None

		if compressor == 'lz4':
			self.compressor = Compressor.Lz4()
		elif compressor is None:
			self.compressor = Compressor.Naive()
		else:
			raise RuntimeError('Unknown compressor "%s"' % compressor)

		if not os.path.isdir(dirname):
			os.makedirs(dirname)

	def set(self, key, value):
		""" Set value with key
		[Notice] Key violation checking is not executed

		:param key: Integer. Unique key of data
		:param value: Object to store. Could be json serializable
		"""
		self.getchunk(key, 'w').append(key, value)

	def get(self, key):
		""" Get data by key.
			File is not indexed by key, so worst time complexity is O(chucksize).
			If you get data by increasing order,

		:param key: Integer. Unique key of data
		:return: String
		"""
		first_key = None
		chunk = self.getchunk(key, 'r')

		while True:
			key_i, value_i = chunk.nextitem(loop=True)
			if key_i is None:
				# Chunk is empty
				return None

			if key == key_i:
				# Found one.
				return value_i

			if first_key is None:
				# Set first_key to key that first comes.
				first_key = key_i
			elif first_key == key_i:
				# If first_key is same with current iterated-key,
				# it means all items in this chunk is checked,
				# so there is not data with this key.
				return None

	def save(self):
		""" Save current chunk
		:return: True if there was cur_chunk, False otherwise
		"""
		if self.cur_chunk and self.cur_chunk.mode == 'w':
			self.cur_chunk.save()
			return True
		else:
			return False

	def chunks(self):
		""" Yield all chunks in this barracks
		`chunk.open()` and `chunk.close()` is called automatically of each iteration step.
		:return: Iterator<Chunk>
		"""
		self.save()

		for file in os.listdir(self.dirname):
			cid = int(file[0:file.index('.')])
			chunk = Chunk(self, cid, 'r')
			chunk.open()
			yield chunk

	def getchunk(self, key, mode):
		""" Get chunk by key. If there is not chunk, create one.

		:param key: Integer. Unique key of data
		:param mode: 'r' on reading, 'w' on writing
		:return: Chunk
		"""
		chunkid = int(key / self.chucksize)

		if self.cur_chunk:
			if self.cur_chunk.id == chunkid and self.cur_chunk.mode == mode:
				# If there is opened chuck and it's same, return it.
				return self.cur_chunk
			else:
				# If there is opened chuck and now switch to another, save old.
				if self.cur_chunk.mode == 'w':
					self.cur_chunk.save()

		# Set current chunk to new one, and open chuck file.
		self.cur_chunk = Chunk(self, chunkid, mode)
		self.cur_chunk.open()
		return self.cur_chunk


class Chunk:

	def __init__(self, barracks, id, mode):
		""" Initialize Chunk instance
		:param barracks: Barracks instance belongs to
		:param id: ID of chunk (equal to 'key / chunksize')
		:param mode: 'r' on reading, 'w' on writing
		"""
		self.barracks = barracks
		self.id = id
		self.mode = mode

		self.filepath = os.path.join(self.barracks.dirname, '%d.dat' % self.id)
		self.buffer = None

	def open(self):
		""" Open file with chunk's mode
		"""
		if not os.path.isfile(self.filepath):
			self.buffer = io.StringIO()
		else:
			with open(self.filepath, 'rb') as file:
				content = self.barracks.compressor.decompress(file.read())

			self.buffer = io.StringIO()
			self.buffer.write(content)

	def save(self):
		""" Save data in buffer to file
		"""
		if self.mode != 'w':
			raise RuntimeError('Attempt writing in mode %s' % self.mode)

		data = self.barracks.compressor.compress(self.buffer.getvalue())
		with open(self.filepath, 'wb') as file:
			file.write(data)

	def append(self, key, value):
		""" Append new text to end of file.

		:param key: Integer
		:param value: Object
		"""
		if self.mode != 'w':
			raise RuntimeError('Attempt writing in mode %s' % self.mode)

		self.buffer.write('%d\t%s\n' % (key, json.dumps(value)))

	def nextitem(self, loop=False):
		""" Get nextitem from current file's position.
		If cursor reaches end of file, reset to first line.
		:param loop: If true, reset file position to first if reaches end of file
		:return: Key, Value pair
		"""
		if self.mode != 'r':
			raise RuntimeError('Attempt reading in mode %s' % self.mode)

		line = self.buffer.readline()
		if not line:
			if loop is True:
				# If line is None, reset file position to first, then fetch again.
				self.buffer.seek(0)
				line = self.buffer.readline()

			if not line:
				# If this line is also None, it means file is empty,
				# So just return None, None
				return None, None

		i = line.index('\t')
		return int(line[0:i]), json.loads(line[i+1:])

	def items(self):
		""" Iterate all items in this chunk
		:return: Iterator<Key, Value>
		"""
		if self.mode != 'r':
			raise RuntimeError('Attempt reading in mode %s' % self.mode)

		self.buffer.seek(0)
		while True:
			key, value = self.nextitem()
			if key is None:
				return
			yield key, value


class Compressor:
	class Naive:
		""" Naive Compressor (do not compress data)
		"""
		def compress(self, content):
			return content.encode()

		def decompress(self, data):
			return data.decode()

	class Lz4(Naive):
		""" Compressor using lz4 algorithm
		"""
		def compress(self, content):
			return lz4.frame.compress(content.encode())

		def decompress(self, data):
			return lz4.frame.decompress(data).decode()
