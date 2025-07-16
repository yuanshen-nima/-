N=eval(input())
listNum=list(map(int,input().split()))
count=0
list=[]
for i in range(N):
    if listNum[i]%6==0:
        count+=1
        list.append(listNum[i])
if count == 0:
    print(-1)
else:
    print(str(list[0])+" "+str(list[1]))