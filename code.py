n = int(input())
arr = [int(x) for x in input().split()]

max_val = arr[0]
for x in arr:
    if x > max_val:
        max_val = x

exp = 1
while max_val // exp > 0:
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        
    for i in range(n):
        arr[i] = output[i]
        
    exp *= 10

print(*(arr))
