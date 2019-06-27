import datetime as dt
import statistics as st
import matplotlib.pyplot as plt
import math

def timestampToDate(timestamp):
    return dt.datetime.fromtimestamp(timestamp)

def strToDatetime(date_str):
    return dt.datetime.strptime(date_str, '%m/%d/%Y %H:%M')

def strSecToMilisec(sec_str):
    return float(sec_str.replace('.',''))

def quartis(values):
    meio = len(values)//2

    Q1 = st.median(values[:meio])
    Q2 = st.median(values)
    Q3 = st.median(values[meio:])
    
    print('Quartis:')
    print('Q1:',Q1)
    print('Q2:',Q2)
    print('Q3:',Q3)

    return [Q1,Q2,Q3]

def noOutliers(values):
    Q1,Q2,Q3 = quartis(values)

    A = Q3 - Q1
    print('A:',A)

    minOutlier = Q1 - A * 1.5 # mod outlier min
    maxOutlier = Q3 + A * 1.5 # mod outlier max
    print('minOutlier:',minOutlier)
    print('maxOutlier:',maxOutlier)

    inliers = list()
    for value in values:
        if minOutlier <= value <= maxOutlier:
            inliers.append(value)
    return inliers

def plotHistogram(values,titleHistogram='', op=0):
    print(titleHistogram)
    valuesSorted = sorted(values) # sorted important
    inliers = noOutliers(valuesSorted) # get inliers

    k = round(1+3.3*math.log10(len(inliers))) ; print('K:',k)# classes
    h = (max(inliers)-min(inliers))/k ; print('H:',h) # intervals
    
    print('total:',len(valuesSorted),'inliers:',len(inliers),sep='\n')
    
    if op == 1:
        inliers = [timestampToDate(value) for value in inliers]
    elif op ==2:
        inliers = [ (value/(1000*60))%60 for value in inliers]

    plt.hist(inliers,bins=k)
    plt.title(titleHistogram)
    plt.show()
    print()