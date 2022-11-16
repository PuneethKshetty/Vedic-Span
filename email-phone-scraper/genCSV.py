import csv

def generateCSV( data ):
	# field names
	fields = ['Phone', 'Email']
	
	if (len(data['phoneList']) > len(data['emailList'])):
		maxlen = len(data['phoneList'])
		minlen = len(data['emailList'])
		for i in range(minlen, maxlen+1):
			data['emailList'].append("")
	else:
		maxlen = len(data['emailList'])
		minlen = len(data['phoneList'])
		for i in range(minlen, maxlen+1):
			data['phoneList'].append("")
		
	# name of csv file 
	filename = "result.csv"
	
	# writing to csv file 
	with open(filename, 'w',  newline="") as csvfile: 
		csvwriter = csv.writer(csvfile)

		csvwriter.writerow(fields)
		for i in range(maxlen):
			csvwriter.writerow( [data['phoneList'][i], data['emailList'][i]] )


if __name__ == "__main__":
	
	dummyData = {
		'phoneList': [911, 100, 300, 400],
		'emailList': ['123@gmail.com', 'xyz@gmail.com', 'xyz@gmail.com', 'xyz@gmail.com', 'xyz@gmail.com']
	}
	
	generateCSV( dummyData )