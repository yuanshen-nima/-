h=2
s=8
IP=3
r,p=map(int,input().split())
r=r/2
s1=IP*r*r*p
s2=IP*r*r*h
print(s1,s2)
count=0
while s1>=s2:
    s2+=s
    count+=1
print(count)