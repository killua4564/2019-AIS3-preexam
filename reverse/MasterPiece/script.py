

data = open("data-14006B000", "r").read()

a = []
index = 0
for _ in range(266504):
	index = data.find("dup(", index) + 4
	a.append(int(data[index]))

print(a)
