"""
HashMap Table Implementation

Collisions are handled in the neighbour and Table versions.

@jlengrand
2013/11
"""

class _HashMapItem():
	"""
	Hashmap items are the objects that will be contained in my Hashmaps.
	They permit to find the correct value back, even in case of collision.
	Not all of my HashMap implementations use HMItems.
	"""
	def __init__(self, key, value):
		self.k = key
		self.v = value

class HashMap():
	"""
	This implementation does NOT use _HashMapItems
	Also, this implementation will return an error in case of a collision.
	Data will not be lost, but another key will have to be used.
	"""
	def __init__(self, hash_size=513):
		self._hash_size = hash_size
		self._size = 0
		self.hmap = [None] * self._hash_size

	def add(self, key, value):
		"""
		Adds the provided value to the hashmap.
		Raises an Exception if a collision is detected
		"""
		my_key = self._hash(key)
		if self.hmap[my_key] == None:
			self.hmap[my_key] = value
			self._size += 1
		else:
			raise Exception("Collision detected at index %d", key)

	def get(self, key):
		"""
		Finds the element in the hash table that may contain the id for
		the string we are looking for
		"""
		my_key = self._hash(key)
		return self.hmap[my_key]

	def size(self):
		return self._size

	def _hash(self, value):
		"""
		Generates a hash for the given value.
		The input is expected to be a String, with only ASCII characters.

		# hash function taken from HT3.
		# We shift and add : << 4 is a *16
		"""
		if len(value) < 1:
			raise Exception("Size of value must be greater than one")

		h = 0
		for letter in value:
			h = (h << 4) + ord(letter)

		return h % self._hash_size

class HashMapWithItem():
	"""
	This implementation USES _HashMapItems
	Also, this implementation will return an error in case of a collision.
	Data will not be lost, but another key will have to be used.
	"""
	def __init__(self, hash_size=513):
		self._hash_size = hash_size
		self._size = 0
		self.hmap = [None] * self._hash_size

	def add(self, key, value):
		"""
		Adds the provided value to the hashmap.
		Raises an Exception if a collision is detected
		"""
		# item to be saved in the HM
		item = _HashMapItem(key, value)

		my_key = self._hash(key)
		if self.hmap[my_key] == None:
			self.hmap[my_key] = item
			self._size += 1
		else:
			raise Exception("Collision detected at index %d", key)

	def get(self, key):
		"""
		Finds the element in the hash table that may contain the id for
		the string we are looking for
		"""
		my_key = self._hash(key)
		return self.hmap[my_key].v # returns the value

	def size(self):
		return self._size

	def _hash(self, value):
		"""
		Generates a hash for the given value.
		The input is expected to be a String, with only ASCII characters.

		# hash function taken from HT3.
		# We shift and add : << 4 is a *16
		"""
		if len(value) < 1:
			raise Exception("Size of value must be greater than one")

		h = 0
		for letter in value:
			h = (h << 4) + ord(letter)

		return h % self._hash_size

class HMTableCollision(HashMap):
	"""
	This implementation USES HMItems
	Extension of the previous HashMap implementation that takes care of
	collisions.
	Instead of having only one slot available per index in the table,
	each index will contain a list. This means several elements can be
	stored with the same index.
	"""
	def __init__(self, hash_size=513):
		self._hash_size = hash_size
		self._size = 0
		self.hmap = [None] * self._hash_size

	def add(self, key, value):
		"""
		Adds the provided value to the hashmap.
		Raises an Exception if a collision is detected
		"""
		# item to be saved in the HM
		item = _HashMapItem(key, value)

		my_key = self._hash(key)

		if self.hmap[my_key] == None:
			self.hmap[my_key] = [item]
		else:
			# we check if same key already exists
			if [key in item.k for item in self.hmap[my_key]]:
				raise Exception("This key already exists!")
			self.hmap[my_key].append(item)
		self._size += 1

	def get(self, key):
		"""
		Finds the element in the hash table that may contain the id for
		the string we are looking for
		"""
		my_key = self._hash(key)
		items = self.hmap[my_key]

		if items is None:
			return items # Nothing found
		elif len(items) == 1:
			return items[0].v # Returns correct value
		else:
			if [key in item.k for item in items]:
				return item.v # result found
			else:
				return None # result not found
			# TODO: Test this

	def size(self):
		return self._size

	def _hash(self, value):
		"""
		Generates a hash for the given value.
		The input is expected to be a String, with only ASCII characters.

		# hash function taken from HT3.
		# We shift and add : << 4 is a *16
		"""
		if len(value) < 1:
			raise Exception("Size of value must be greater than one")

		h = 0
		for letter in value:
			h = (h << 4) + ord(letter)

		return h % self._hash_size


class HMNeighbourCollision():
	def __init__(self, hash_size=513):
		self._hash_size = hash_size
		self._size = 0
		self.hmap = [None] * self._hash_size

	def add(self, key, value):
		"""
		Adds the provided value to the hashmap.
		Raises an Exception if a collision is detected
		"""
		my_key = self._hash(key)
		idx = self._find_free_idx(my_key)

		self.hmap[idx] = value
		self._size += 1

	def _find_free_idx(self, key):
		"""
		Given an index in the current hash table, finds the nearest
		element with a free value
		"""
		idx = key
		cur_ptr = 1
		negative = True

		while(True):
			if self.hmap[idx] == None:
				return idx
			else:
				if negative:
					idx = key - cur_ptr
					negative = False
				else:
					idx = key + cur_ptr
					negative = True
					cur_ptr += 1

	def get(self, key):
		"""
		Finds the element in the hash table that may contain the id for
		the string we are looking for
		"""
		my_key = self._hash(key)

		# Test all the possible indexes for the key
		# Stop when we reach the limits of the hasmaps
		# or we find a free index
		idx = my_key
		cur_ptr = 1
		negative = True
		while(idx > 0 and idx < self._hash_size):
			item = self.hmap[item]

			if item == None:
				return None
			elif item.k == key:
				# We found a match
				return item.v
			else:
				if negative:
					idx = key - cur_ptr
					negative = False
				else:
					idx = key + cur_ptr
					negative = True
					cur_ptr += 1

		return None # key not in the HM

	def size(self):
		return self._size

	def _hash(self, value):
		"""
		Generates a hash for the given value.
		The input is expected to be a String, with only ASCII characters.

		# hash function taken from HT3.
		# We shift and add : << 4 is a *16
		"""
		if len(value) < 1:
			raise Exception("Size of value must be greater than one")

		h = 0
		for letter in value:
			h = (h << 4) + ord(letter)

		return h % self._hash_size
