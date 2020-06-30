from __future__ import print_function
for x in range(10):
	print("*", end=" ")
print()
for x in range(5):
	print("*", end=" ")
print() 
for x in range(20):
	print("*", end=" ")
print('\n')

for x in range(10):
	for y in range(10):
		print("*", end=" ")
	print()	

print('\n')
for x in range(10):
	for y in range(5):
		print("*", end=" ")
	print()


for x in range(10):
	for y in range(10):
		print(y, end=" ")
	print()
print()

for x in range(10):
	for y in range(10):
		print(x, end=" ")
	print()
print('\n')

for x in range(11):
	for y in range(x):
		print(y, end=" ")
	print()
print('\n')

for x in reversed(range(11)):
	for y in range(10-x):
		print("  ", end="")
	for z in range(x):
		print(z,end=" ")
	print()

