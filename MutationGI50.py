__author__ = 'Ben'

clGI50 = {}
mutationCL = {}
mutationGI50 = {}

with open('CellLineIC50v3.txt', 'r') as f: #opens and reads in the file containing the cell line and GI50 info
    data = f.readlines()

    for line in data:
        #separates and stores the cell line and GI50 info from each line 
        temp = line.split()

        cellLine = temp[0]
        gi50 = float(temp[1])
        
        #adds cell line and GI50 info to the dict, using cell line as key and GI50 as value 
        if cellLine not in clGI50:
            clGI50.setdefault(cellLine, []).append(gi50)
        elif gi50 not in clGI50[cellLine]:
            clGI50[cellLine].append(gi50)
            
        
with open('CellLine-Mutationv3.txt', 'r') as f:
    data = f.readlines()
    
    for line in data:
        temp = line.split()
        
        cellLine = temp[0]
        mutation = temp[1]
        
        #adds cell line and mutation info to the dict, using mutation as key and cell line as value
        if mutation not in mutationCL:
            mutationCL.setdefault(mutation, []).append(cellLine)
        elif cellLine not in mutationCL[mutation]:
            mutationCL[mutation].append(cellLine)

#matches mutations with corresponding GI50 values
for mutation in mutationCL:
    for cellLine in clGI50:

        if cellLine in mutationCL[mutation]:
            if mutation not in mutationGI50:
                mutationGI50.setdefault(mutation, []).extend(clGI50[cellLine])
            else:
                mutationGI50[mutation].extend(clGI50[cellLine])


with open('CL - GI50v3.txt', 'w') as out:
    for cellLine in clGI50:
        out.write('%s\t' %cellLine)

        for gi50 in clGI50[cellLine]:
            out.write('%0.3f\t' %gi50)

        out.write('\n')

with open('Mutation - Cell Linev3.txt', 'w') as out:
    for mutation in mutationCL:
        out.write('%s\t' %mutation)

        for cellLine in mutationCL[mutation]:
            out.write('%s\t' %cellLine)

        out.write('\n')



with open('Mutation_GI50v3.txt', 'w') as out:
    for mutation in mutationGI50:
        out.write('%s\t' %mutation)

        for gi50 in mutationGI50[mutation]:
            out.write('%0.3f\t' %gi50)

        out.write('\n')


