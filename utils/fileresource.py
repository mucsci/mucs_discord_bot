import json
import asyncio

class FileBackedResource:

	def __init__(self, filename):
		self.filename = filename
		self.data = self._load_json()
		self.lock = asyncio.Lock()
	
	def _load_json(self):
		with open(self.filename, 'r') as f:
			self.data = json.load(f)

	def _store_json(self):
		with open(self.filename, 'w') as f:
			json.dump(self.data, f)
	
	async def get(self, item, defvalue):
		async with self.lock:
			self._load_json()
			if item in self.data:
				return self.data[item]
			return defvalue

	async def set(self, item, value):
		async with self.lock:
			self._load_json()
			self.data[item] = value
			self._store_json()
			return value
