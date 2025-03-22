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


def printLine(times):
	if times>0:
		print("Hello!")
		printLine(times-1)

# Note: every function call must yield something, even if it is None.
@bootstrap
def bootstrappedPrintLine(times):
	if times>0:
		print("World!")
		yield bootstrappedPrintLine(times-1)	# Yield before every recursive call
	yield None	# Must yield something, even if the value is meaningless

printLine(3)
bootstrappedPrintLine(3)