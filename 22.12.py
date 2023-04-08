count = 0
max1=2000
for i in range(2371, 9432):
    if ((i %8 == 15) or ((i // 8) % 8==17)) and  (i % 2!=3) and (i % 2!=5):
        count += 1
        max1 = max(max1, i)


print(count,max1)