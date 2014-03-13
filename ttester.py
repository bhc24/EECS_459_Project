__author__ = 'Ben'

import scipy.stats, re 


fp = open('Mutation_GI50v3.txt', 'rb')
#print "hey"
#Mut_GI50 = pickle.load(fp)
    #Mut_GI50 = fp.readlines()
fp.close()

Mut_GI50 = {}

with open("Mutation_GI50v3.txt") as f:
    for line in f:  #Line is a string
        #split the string on whitespace, return a list of numbers 
        # (as strings)
        numbers_str = line.split()
        #convert numbers to floats
        mutation = numbers_str[0]
        if mutation not in Mut_GI50:
            Mut_GI50.setdefault(mutation, [])

        Mut_GI50[mutation].extend([float(x) for x in numbers_str[1:]])

singleVsAll = {}
geneVsAll = {}
singleVsGene = {}

#each mutation vs all - mutation
def single_vs_all(Mutation_GI50, isFirst):
    for targetMutation in Mutation_GI50:
        targetGI50 = []
        otherGI50 = []

        targetGI50.extend([float(x) for x in Mutation_GI50[targetMutation]])

        for otherMutation in Mutation_GI50:
            if otherMutation == targetMutation:
                continue

            otherGI50.extend([float(x) for x in Mutation_GI50[otherMutation]])
        if isFirst:

            if targetMutation not in singleVsGene:
                singleVsGene.setdefault(targetMutation, []).extend(scipy.stats.ttest_ind(targetGI50, otherGI50, axis=None, equal_var=False))
        else:
            if targetMutation not in singleVsAll:
                singleVsAll.setdefault(targetMutation, [])
                singleVsAll[targetMutation].extend(scipy.stats.ttest_ind(targetGI50, otherGI50, axis=None, equal_var=False))




#all 'p10' vs all - p10
def gene_vs_all(Mutation_GI50):
    checkedMutations = []
    for targetMutation in Mutation_GI50:
        targetMutationList = re.split('_', targetMutation)
        print(targetMutationList)
        targetGI50 = []
        otherGI50 = []

        if targetMutationList[0] not in checkedMutations:
            checkedMutations.append(targetMutationList[0])
            targetGI50.extend([float(x) for x in Mutation_GI50[targetMutation]])
        else:
            continue

        for otherMutation in Mutation_GI50:
            otherMutationList = re.split('_', otherMutation)

            if otherMutationList[0] in targetMutationList:
                targetGI50.extend([float(x) for x in Mutation_GI50[otherMutation]])
            else:
                otherGI50.extend([float(x) for x in Mutation_GI50[otherMutation]])

        if targetMutation not in geneVsAll:
            geneVsAll.setdefault(targetMutation, [])
            geneVsAll[targetMutation].extend(scipy.stats.ttest_ind(targetGI50, otherGI50, axis=None, equal_var=False))


#each 'p10' vs all 'p10' - selected
def single_vs_gene(Mutation_GI50):
    geneGI50 = {}
    for mutation in Mutation_GI50:
        temp = mutation.split('_')
        geneName = temp[0]

        if geneName not in geneGI50:
            geneGI50.setdefault(geneName, {}).setdefault(mutation, []).extend([float(x) for x in Mutation_GI50[mutation]])
        elif mutation not in geneGI50[geneName]:
            geneGI50[geneName].setdefault(mutation, []).extend([float(x) for x in Mutation_GI50[mutation]])

    for geneName in geneGI50:
        single_vs_all(geneGI50[geneName], True)

single_vs_all(Mut_GI50, False)
gene_vs_all(Mut_GI50)
single_vs_gene(Mut_GI50)

otpt = open('singleVsAllv3.txt', 'w')

for keyName in singleVsAll:
    otpt.write('%s\t' % keyName)

    for valueName in singleVsAll[keyName]:

        value = float(valueName)

        otpt.write('%.4f\t' % valueName)

    otpt.write('\n')

otpt.close()

otpt = open('geneVsAllv3.txt', 'w')

for keyName in geneVsAll:
    otpt.write('%s\t' % keyName)

    for valueName in geneVsAll[keyName]:

        value = float(valueName)

        otpt.write('%.4f\t' % valueName)

    otpt.write('\n')

otpt.close()

otpt = open('singleVsGenev3.txt', 'w')

for keyName in singleVsGene:
    otpt.write('%s\t' % keyName)

    for valueName in singleVsGene[keyName]:

        value = float(valueName)

        otpt.write('%.4f\t' % valueName)

    otpt.write('\n')

otpt.close()




#fp = open('singleVsAll.pkl', 'wb')
#pickle.dump(singleVsAll, fp)
#fp.close()

#fp = open('geneVsAll.pkl', 'wb')
#pickle.dump(geneVsAll, fp)
#fp.close()

#fp = open('singleVsGene.pkl', 'wb')
#pickle.dump(singleVsGene, fp)
#fp.close()