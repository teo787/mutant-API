def isMutant(dna):
    n=len(dna)
    if n<4:
        return False
    directions=[(0,1), (1,0), (1,1)]
    sequences_found=0
    for i in range(n):
        for j in range(n):
            for di, dj in directions:
                end_i=i+3*di
                end_j=j+3*dj
                if not(0<=end_i<n and 0<=end_j<n):
                    continue
                base=dna[i][j]
                if all(dna[i+k*di][j+k*dj]==base for k in range(1, 4)):
                    sequences_found+=1
                    if sequences_found>1:
                        return True
    return False