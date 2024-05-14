ECB_VALUE =	0
CBC_VALUE =	1

PAD_NORMAL_VALUE = 1
PAD_PKCS5_VALUE = 2

class BaseDes():
	def __init__(self, mode=ECB_VALUE, initialValue=None, pad=None, padmode=PAD_NORMAL_VALUE):
		if initialValue:
			initialValue = self.unicodeProtection(initialValue)
		if pad:
			pad = self.unicodeProtection(pad)
		self.block_size = 8
		self.mode = mode
		self.initialValue = initialValue
		self.padding = pad
		self.padMode = padmode

	def pad(self, data, pad, padmode):
		if padmode is None:
			padmode = self.getPadMode()
		if padmode == PAD_NORMAL_VALUE:
			if len(data) % self.block_size == 0:
				return data
			if not pad:
				pad = self.getPadding()
			data += (self.block_size - (len(data) % self.block_size)) * pad
		
		elif padmode == PAD_PKCS5_VALUE:
			pad_len = 8 - (len(data) % self.block_size)
			data += bytes([pad_len] * pad_len)

		return data

	def unpad(self, data, pad, padmode):
		if not data:
			return data
		padmode = padmode or self.getPadMode()

		if padmode == PAD_NORMAL_VALUE:
			pad = pad or self.getPadding()
			if pad:
				normal_data, separator, padded = data.rpartition(pad * self.block_size)
				if separator:
					data = normal_data + padded.replace(pad, '')

		elif padmode == PAD_PKCS5_VALUE:
			pad_len = data[-1]
			data = data[:-pad_len] if 0 < pad_len < self.block_size else data

		return data


	def unicodeProtection(self, data):
		if isinstance(data, str):
			try:
				return data.encode('ascii')
			except UnicodeEncodeError:
				pass
			raise ValueError("DES can only work with encoded strings.")
		return data
	
	def getKey(self):
		return self.key

	def setKey(self, key):
		key = self.unicodeProtection(key)
		self.key = key

	def getMode(self):
		return self.mode

	def setMode(self, mode):
		self.mode = mode

	def getPadding(self):
		return self.padding

	def setPadding(self, pad):
		if pad is not None:
			pad = self.unicodeProtection(pad)
		self.padding = pad

	def getPadMode(self):
		return self.padMode
		
	def setPadMode(self, mode):
		self.padMode = mode

	def getInitialValue(self):
		return self.initialValue

	def setInitialValue(self, IV):
		IV = self.unicodeProtection(IV)
		self.initialValue = IV

class Des(BaseDes):

	PC1 = [56, 48, 40, 32, 24, 16,  8,
		  0, 57, 49, 41, 33, 25, 17,
		  9,  1, 58, 50, 42, 34, 26,
		 18, 10,  2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13,  5, 60, 52, 44, 36, 28,
		 20, 12,  4, 27, 19, 11,  3
	]

	LEFT_ROTATIONS = [
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
	]

	PC2 = [
		13, 16, 10, 23,  0,  4,
		 2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

	INITIAL_PERMUTATIONS = [
		57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]

	EXPANSION_TABLE = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

	BOX = [
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],


		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

	P = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]

	FIRST_PERMUTATION = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]

	ENCRYPT =	0x00
	DECRYPT =	0x01

	def __init__(self, key, mode=ECB_VALUE, IV=None, pad=None, padmode=PAD_NORMAL_VALUE):
		BaseDes.__init__(self, mode, IV, pad, padmode)
		self.key_size = 8
		self.LEFT = []
		self.RIGHT = []
		self.map = [ [0] * 48 ] * 16
		self.final = []

		self.setKey(key)

	def setKey(self, key):
		BaseDes.setKey(self, key)
		self.createSubKeys()

	def string2BitList(self, data):
		size_with_bit = len(data) * 8
		result = [0] * size_with_bit
		index = 0
		for ch in data:
			i = 7
			while i >= 0:
				if ch & (1 << i) != 0:
					result[index] = 1
				else:
					result[index] = 0
				index += 1
				i -= 1
		return result

	def bitList2String(self, data):
		result_str = []
		index = 0
		c = 0
		while index < len(data):
			c += data[index] << (7 - (index % 8))
			if (index % 8) == 7:
				result_str.append(c)
				c = 0
			index += 1

		return bytes(result_str)

	def permutate(self, table, block):
		return list(map(lambda x: block[x], table))
	
	def createSubKeys(self):
		key = self.permutate(Des.PC1, self.string2BitList(self.getKey()))
		i = 0
		self.LEFT = key[:28]
		self.RIGHT = key[28:]
		while i < 16:
			j = 0
			while j < Des.LEFT_ROTATIONS[i]:
				self.LEFT.append(self.LEFT[0])
				del self.LEFT[0]
				self.RIGHT.append(self.RIGHT[0])
				del self.RIGHT[0]
				j += 1
			self.map[i] = self.permutate(Des.PC2, self.LEFT + self.RIGHT)
			i += 1

	def desEncrypt(self, block, encryptionType):
		block = self.permutate(Des.INITIAL_PERMUTATIONS, block)
		self.LEFT = block[:32]
		self.RIGHT = block[32:]
		if encryptionType == Des.ENCRYPT:
			iteration = 0
			iterationAdjustment = 1
		else:
			iteration = 15
			iterationAdjustment = -1
		i = 0
		while i < 16:
			tempR = self.RIGHT[:]
			self.RIGHT = self.permutate(Des.EXPANSION_TABLE, self.RIGHT)
			self.RIGHT = list(map(lambda x, y: x ^ y, self.RIGHT, self.map[iteration]))
			SONUC = [self.RIGHT[:6], self.RIGHT[6:12], self.RIGHT[12:18], self.RIGHT[18:24], self.RIGHT[24:30], self.RIGHT[30:36], self.RIGHT[36:42], self.RIGHT[42:]]
			j = 0
			xd = [0] * 32
			position = 0
			while j < 8:
				m = (SONUC[j][0] << 1) + SONUC[j][5]
				n = (SONUC[j][1] << 3) + (SONUC[j][2] << 2) + (SONUC[j][3] << 1) + SONUC[j][4]
				v = Des.BOX[j][(m << 4) + n]
				xd[position] = (v & 8) >> 3
				xd[position + 1] = (v & 4) >> 2
				xd[position + 2] = (v & 2) >> 1
				xd[position + 3] = v & 1
				position += 4
				j += 1
			self.RIGHT = self.permutate(Des.P, xd)
			self.RIGHT = list(map(lambda x, y: x ^ y, self.RIGHT, self.LEFT))
			self.LEFT = tempR
			i += 1
			iteration += iterationAdjustment
		self.final = self.permutate(Des.FIRST_PERMUTATION, self.RIGHT + self.LEFT)
		return self.final

	def crypt(self, data, encryptionType):
		if not data:
			return ''
		if len(data) % self.block_size != 0:
				data += (self.block_size - (len(data) % self.block_size)) * self.getPadding()
		if self.getMode() == CBC_VALUE:
			if self.getInitialValue():
				iv = self.string2BitList(self.getInitialValue())
		i = 0
		result = []
		while i < len(data):
			block = self.string2BitList(data[i:i+8])
			if self.getMode() == CBC_VALUE:
				if encryptionType == Des.ENCRYPT:
					block = list(map(lambda x, y: x ^ y, block, iv))
				pb = self.desEncrypt(block, encryptionType)

				if encryptionType == Des.DECRYPT:
					pb = list(map(lambda x, y: x ^ y, pb, iv))
					iv = block
				else:
					iv = pb
			else:
				pb = self.desEncrypt(block, encryptionType)

			result.append(self.bitList2String(pb))
			i += 8
		return bytes.fromhex('').join(result)

	def encrypt(self, data, pad=None, padmode=None):
		data = self.unicodeProtection(data)
		if pad is not None:
			pad = self.unicodeProtection(pad)
		data = self.pad(data, pad, padmode)
		return self.crypt(data, Des.ENCRYPT)

	def decrypt(self, data, pad=None, padmode=None):
		data = self.unicodeProtection(data)
		if pad is not None:
			pad = self.unicodeProtection(pad)
		data = self.crypt(data, Des.DECRYPT)
		return self.unpad(data, pad, padmode)
	
