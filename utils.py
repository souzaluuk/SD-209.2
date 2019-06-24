import datetime as dt
import statistics as st

def strToDatetime(date_str):
	return dt.datetime.strptime(date_str, '%m/%d/%Y %H:%M')

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

	minOutlier = Q1 - A * 3 # extreme outlier min
	maxOutlier = Q3 + A * 3 # extreme outlier max
	print('minOutlier:',minOutlier)
	print('maxOutlier:',maxOutlier)

	inliers = list()
	for value in values:
		if minOutlier <= value and value<= maxOutlier:
			inliers.append(value)
	return inliers