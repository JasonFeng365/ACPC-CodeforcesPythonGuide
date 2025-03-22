from types import GeneratorType

def bootstrap(f, stack=[]):
	def wrappedfunc(*args, **kwargs):
		if stack:
			return f(*args, **kwargs)
		else:
			to = f(*args, **kwargs)
			while True:
				if type(to) is GeneratorType:
					stack.append(to)
					to = next(to)
				else:
					stack.pop()
					if not stack:
						break
					to = stack[-1].send(to)
			return to

	return wrappedfunc


arr = [2, 4, 3, 5, 1]

# Base function
def getMax(i):
	if i==len(arr): return 0
	return max(arr[i], getMax(i+1))

# Same function, converted to bootstrap to avoid recursion limit
@bootstrap
def bootstrappedGetMax(i):
	if i==len(arr): yield 0
	# Note: yield cannot be inlined.
	nxt = yield bootstrappedGetMax(i+1)
	yield max(arr[i], nxt)

print(getMax(0))	# 5
print(bootstrappedGetMax(0))	# 5