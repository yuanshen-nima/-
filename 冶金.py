def find_production_scheme(c, d, t):  
    # c = [c1, c2, c3] for M1  
    # d = [d1, d2, d3] for M2  
    # t = [t1, t2, t3] for inventory  
    min_waste = float('inf')  
    best_x1, best_x2 = 0, 0  
    
    for x1 in range((t[0] // c[0] + 1) if c[0] > 0 else 1):  # 0 to max possible x1 for M1  
        for x2 in range((t[1] // d[0] + 1) if d[0] > 0 else 1):  # 0 to max possible x2 for M2  
            waste1 = t[0] - (c[0] * x1 + d[0] * x2)  
            waste2 = t[1] - (c[1] * x1 + d[1] * x2)  
            waste3 = t[2] - (c[2] * x1 + d[2] * x2)  
            
            if waste1 >= 0 and waste2 >= 0 and waste3 >= 0:  
                total_waste = waste1 + waste2 + waste3  
                if (total_waste < min_waste) or (total_waste == min_waste and x1 < best_x1):  
                    min_waste = total_waste  
                    best_x1 = x1  
                    best_x2 = x2  
                    
    return best_x1, best_x2  

# Input  
c = list(map(int, input().strip().split()))  
d = list(map(int, input().strip().split()))  
t = list(map(int, input().strip().split()))  

# Find the scheme  
x1, x2 = find_production_scheme(c, d, t)  

# Output  
print(x1, x2)