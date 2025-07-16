#16.交易星
#在一个遥远的星球上，有一个名为“交易星”的繁华都市。这个城市由 n 个不同的商业区组成，每个商业区都有其独特的商品和交易规则。在这个星球上，商人之间进行商品交易时，需要通过一种名为“能量券”的货币进行支付。然而，每个商业区间进行能量券转移时，都会有一定的能量损耗，这种损耗以百分比的形式表示。
#现在，交易星的商人协会发起了一项挑战：商人 A 需要将一定数量的能量券转移到商人 B，以确保 B 能够收到恰好 100 单位的能量券。你需要帮助商人 A 计算出，为了完成这笔交易，他至少需要支付多少单位的能量券。
#输入格式
#第一行包含两个正整数 n 和 m，分别表示商业区的数量和可进行能量券转移的路径数量。
#接下来的 m 行，每行包含三个正整数 u、v 和 p，表示商业区 u 和商业区 v 之间的路径以及该路径上的能量损耗百分比 p（1 <= p < 100）。路径是双向对称的。
#最后一行包含两个正整数 A 和 B，表示能量券转移的起始商业区和目标商业区。
#数据范围： 1 ≤ n ≤ 2000, m ≤ 10^5
#输出格式
#输出一个小数，表示商人 A 需要支付的最小能量券数量，确保商人 B 收到至少 100 单位的能量券。结果保留 8 位小数。
#输入样例1
#3 3
#1 2 5
#2 3 5
#1 3 10
#1 3
#输出样例1
#110.80332410
#输入样例2
#4 4
#1 2 20
#2 3 20
#3 4 20
#1 4 5
#1 4
#输出样例2
#105.26315789
n,m=map(int,input().split())
a=[[0]*n for i in range(n)]
for i in range(m):
    u,v,p=map(int,input().split())
    a[u-1][v-1]=p
    a[v-1][u-1]=p
start,end=map(int,input().split())
print(a)
if start==end:
    print(100)
if a[start-1][end-1]==0:
    print(100)
def dfs(start,end,visited,ans1):
    for i in range(n):
        if a[start][i]!=0 and visited[i]==0:
            visited[i]=1
            ans1=dfs(i,end-1,visited,ans1*a[start][i])
            visited[i]=0
        if i==end:
            ans=min(ans,ans1*a[start][i])
            
    return ans
visited=[0]*n
ans=a[start-1][end-1]
ans1=1
ans=dfs(start-1,end-1,visited,ans1)
print((ans+1)*100)

