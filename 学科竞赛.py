N,C=map(str,input().split())
listNUM=[]
N=int(N)
for i in range(N):
    listNUM.append(list(map(int,input().split())))
priontlist=[]
if C=='I':
    priontlist.append(listNUM[1]+listNUM[2])
elif C=='B':
    priontlist.append(listNUM[3]+listNUM[1])
elif C=='H':
    priontlist.append(listNUM[4]+listNUM[5])
print