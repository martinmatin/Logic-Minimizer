# Author: Martin Crappe
# Date: 2016
# Using Python 3.5
import os
import copy
import time
start_time = time.time()

# Sous windows, mettre le dossier 'fonction' dans le dossier contenant le code
fileDir = os.path.dirname(os.path.realpath('__file__'))
#changer le numéro de fonction si vous le souhaitez
filename = os.path.join(fileDir, 'fonction/fonctionC.cubes')
def readFile(filename):
    with open(filename) as f:
        return [[int(x) for x in line.split()] for line in f]
    filehandle.close()
liste = readFile(filename)

#OU ALORS, entrez votre matrice manuellement sous le nom de 'liste' comme ci dessous
# liste = [[2,3,3,2,1,1],
#          [2,3,2,1,1,2],
#          [1,1,3,3,1,3],
#          [1,2,1,1,3,2],
#          [3,2,2,1,3,3],
#          [2,1,3,1,1,3],
#          [3,1,3,3,3,3],
#          [2,3,3,3,3,2],
#          [1,2,2,1,3,1],
#          [3,2,3,1,2,2]]

#determiner nombre de variable
if(type(liste[0])==int):
    nbvar = len(liste)
else:
    nbvar = len(liste[0])

def IsBiforme(cubelist,nbvar): #retourne si c'est biforme ou non ainsi que la variable biforme
    biformity=[0] * nbvar
    biforme=False
    balance = [0] * nbvar
    minimum_balance=0

    #on cherche s'il y a de la diformité, si c'est la cas, on somme le nombre de difformité dans "diformity"
    for var in range(0,nbvar):
        comparaison=3
        for elem in cubelist:
            if(elem[var]!=3):
                biformity[var]+=1
                if (comparaison==3): #si comparaison n'a pas été encore changé il égal 3, s'il est monoforme il est égal à 0
                    comparaison=elem[var]
                if(comparaison!=3 and comparaison!=elem[var]):
                    comparaison=0
        if(comparaison!=0):
            biformity[var]=0

    #biformité ou non
    if(all(elem == 0 for elem in biformity)): # pas de biformité, tous monoforme ces petis filous
        return False,None
    else: # il y a de la biformité
        #on regarde quels sont les maximums dans biformity
        for var in range(0,len(biformity)):
            if biformity[var]==max(biformity):
                for elem in cubelist: #s'il c'est un maximum de biformity, on fait la balance
                    if(elem[var]!=3): balance[var]+= (-2*elem[var])+3
                balance[var]=abs(balance[var])
        try:
            minimum_balance = min(i for i in balance if i > 0)
        except:
            minimum_balance = 0
        for var in range(0,len(biformity)): # on regarde lequel parmi les maximums de biforme à la plus petite balance
            if (biformity[var]==max(biformity) and (balance[var] in(minimum_balance,0))):
                return True, var #var = colonne

def MonoformeVal(cubelist,nbvar):
        monoformity=[0] * nbvar

        for var in range(0,nbvar):
            for elem in cubelist:
                if(elem[var]!=3):
                    monoformity[var]+=1
        for var in range(0,len(monoformity)):
            if(monoformity[var])==max(monoformity):
                return var

def CheckIdent(cubelist): #retirer des accolades s'il y en a en trop: [[1]] to [1]

    while len(cubelist)!=0 and (type(cubelist[0]) is not int) and len(cubelist)==1:
        cubelist = cubelist[0]

    return cubelist

def Cofacteur(cubelist,variable):
    positiveCo = copy.deepcopy(cubelist)
    negativeCo = copy.deepcopy(cubelist)

    #positiveCo
    for cube in range(0,len(positiveCo)): #parcourir la liste de cube dans la variable déterminée
        try:
            while positiveCo[cube][variable] == 2:
                positiveCo.pop(cube)
            if positiveCo[cube][variable] == 1:
                positiveCo[cube][variable] =3
        except IndexError:
            break;

    for cube in range(0,len(negativeCo)): #parcourir la liste de cube dans la variable déterminée
        try:
            while negativeCo[cube][variable] == 1:
                negativeCo.pop(cube)
            if negativeCo[cube][variable] == 2:
                negativeCo[cube][variable] =3
        except IndexError:
            break;
    positiveCo,negativeCo = map(CheckIdent, (positiveCo, negativeCo))
    return positiveCo,negativeCo

def Expansion(complement,variable,n): #Expension remplace dans la cologne de la variable choisie par des zero ou des 1 (n dans notre cas)
    if type(complement[0]) is int:
        complement[variable]=n
        return complement
    else:
        for elem in complement:
            elem[variable]=n
        return complement


def Complement(cubelist,nbvar):
    #Vérifier si cube est vide
    if (len(cubelist)==0):
        cube = [3] * nbvar
        return cube

    #Vérifier si la liste de cube contient au moins 1 All don't care cube
    elif(type(cubelist[0]) is list):
        for cube in cubelist:
            #vérifier si c'est un All don't care cube
            if(all(elem == 3 for elem in cube)):
                return []

    elif(type(cubelist[0]) is int): #S'il n'y a qu'un seul cube
        #vérifier si c'est un All don't care cube
        if(all(elem == 3 for elem in cubelist)):
            return []

        #si le cube n'est pas un All don't care cube, utiliser la loi de Morgan
        Demorgan = []
        for i in range(0,nbvar):
            cube = [3] * nbvar
            if(cubelist[i]!=3):
                cube[i]=-cubelist[i]+3  #fonction pour complémenter 1 et 2
                Demorgan.append(cube)

        return Demorgan


    variable=0
    #Si aucun de ces trois au dessus, vérifier s'il y a une variable biforme
    boolean,variable =IsBiforme(cubelist,nbvar)
    if(boolean):
        pass
    else:
        variable = MonoformeVal(cubelist,nbvar)

    positiveCof,negativeCof=Cofacteur(cubelist,variable)
    # input('next....') #activer les INPUTS pour voir step by step dans le terminal
    positiveComp=Complement(positiveCof,nbvar)
    # input("next....")
    negativeComp = Complement(negativeCof,nbvar)
    # input("next....")
    compf = []
    if(len(positiveComp)!=0):
        exp = Expansion(positiveComp,variable,1)
        exp = CheckIdent(exp)
        if type(exp[0]) is not int:
            for elem in exp:
                compf.append(elem)
        else:
            compf.append(exp)
        # compf.append(Expansion(positiveComp,variable,1))
    if(len(negativeComp)!=0):
        exp = Expansion(negativeComp,variable,2)
        exp = CheckIdent(exp)
        if type(exp[0]) is not int:
            for elem in exp:
                compf.append(elem)
        else:
            compf.append(exp)
    compf = CheckIdent(compf)

    return(compf)


compf = Complement(liste,nbvar)
print('Fct minimisée')
if len(compf)!=0 and type(compf[0]) is not int:
    for elem in compf:
        print(elem)
else:
    print(compf)
print("--- %s seconds ---" % (time.time() - start_time))

print(len(liste[0]))
