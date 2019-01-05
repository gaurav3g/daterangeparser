from daterange import daterange
import csv

def readCsv(path):
	res_list = list()
	with open(path, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader, None)
		for row in csvreader:
			for s in row:
				res_list.append(s)
	return res_list

def writeCsv(path, lst):
	with open(path+'.csv', 'wb') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    wr.writerow(["date_input", "date_start", "date_end"])
	    for row in lst:
		    wr.writerow(row)

def main():
	input_arr = readCsv('/home/gaurav/projectDirectory/python-20180815/attachments/sample_file_input.csv')
	output_arr = list()

	obj = daterange()
	for dstr in input_arr:
		start_date, end_date = obj.parse(dstr)
		output_arr.append((dstr , start_date, end_date))

	if(len(output_arr) > 0):
		writeCsv('gauravgupta', output_arr)

if __name__ == '__main__':
	main()