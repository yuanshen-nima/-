N, M = map(int, input().split())
listNum = list(map(int, input().split()))
listSum = []
for i in range(0, N-M):
    temp = 1
    for j in range(i, i + M):
        temp *= listNum[j]
    listSum.append((temp, i))
listSum.sort()
print(listSum[0][0],listSum[0][1]+1)
