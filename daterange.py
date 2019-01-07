from dateutil.parser import parse,parserinfo
from datetime import datetime
import re

class daterange:

	_timestr = ''
	_month_dict = {
		'jan': 1,
		'feb': 2,
		'mar': 3,
		'apr': 4,
		'may': 5,
		'jun': 6,
		'jul': 7,
		'aug': 8,
		'sep': 9,
		'oct': 10,
		'nov': 11,
		'dec': 12
	}
	

	_month_regex = re.compile(r'(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)', flags=re.IGNORECASE)
	_year_regex = re.compile(r'((19|20|\')\d{2}(-((19|20|\')?)\d{2})?)')
	_date_regex = re.compile(r'\b(\d{1,2})(st|rd|th)?')
	_time_regex = re.compile(r'\b((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))')
	

	def parse(self, timestr):
		self._timestr = timestr
		start_date,end_date = '',''
		if self._isparsabledate(self._timestr):
			return self._strToDate(self._timestr),self._strToDate(self._timestr)
		else:
			if not bool(re.search('[a-zA-Z]', self._timestr)) and self._timestr.count('-')==1:
				subdate = self._timestr.split("-")
				if self._isparsabledate(subdate[0]) and self._isparsabledate(subdate[1]):
					return self._strToDate(subdate[0]),self._strToDate(subdate[1])
			
			start_date_list,end_date_list = {'date': '', 'month': '', 'year': ''}, {'date': '', 'month': '', 'year': ''}
			
			# get monthlist from string
			monthlist = self._findmonth(self._timestr)
			if(len(monthlist)>0):
				monthlistindex = list() 
				
				for monthname in monthlist:
					monthlistindex.append(self._month_dict[monthname])
				
				start_date_list['month'],end_date_list['month'] = monthlist[0],monthlist[len(monthlist)-1]

			# get yearlist from timestr and remove year from string
			yearlist = self._findyear(self._timestr)
			if(len(yearlist)>0):
				if(self._month_dict[start_date_list['month']]>self._month_dict[end_date_list['month']]):
					yearlist.append(max(yearlist) - 1)
				start_date_list['year'],end_date_list['year'] = min(yearlist),max(yearlist)
			
			# get timelist from timestr and remove time from string
			timelist = self._findtime(self._timestr)
			
			# get datelist from timestr and remove time from string
			datelist = self._finddate(self._timestr)
			print(datelist)
			if len(datelist)>0:
				start_date_list['date'],end_date_list['date'] = datelist[0],datelist[len(datelist)-1]
			
			temp_start_date,temp_end_date = str(start_date_list['date']) +' '+ start_date_list['month'] +' '+ str(start_date_list['year']), str(end_date_list['date']) +' '+ end_date_list['month'] +' '+ str(end_date_list['year'])

			if self._isparsabledate(temp_start_date):
				start_date = self._strToDate(temp_start_date)

			if self._isparsabledate(temp_end_date):
				end_date = self._strToDate(temp_end_date)

			return start_date,end_date

	def _strToDate(self,timestr):
		timestr = timestr.strip()
		if bool(re.search('[a-zA-Z]', timestr)):
			return parse(timestr).strftime("%-d-%b-%Y")
		else:
			try:
				rep = re.sub(r'[-/.]', '#', timestr)
				return datetime.strptime(rep , '%d#%m#%Y').strftime("%-d-%b-%Y")
			except Exception as e:
				return ''

	def _isparsabledate(self,timestr):
		if timestr.count('-') != 1:
			try:
			    parse(timestr)
			    return True
			except ValueError:
			    return False
		else:
			return False

	def _isyear(self,timestr):
		try:
			if bool(self._year_regex.search(timestr)):
				return True
			else:
				return False
		except Exception as e:
			return False

	def _formatyear(self,timestr):
		if(len(timestr)<4):
			timestr = ('20' if int(timestr.replace('\'','')) <= int(datetime.now().strftime("%y"))+25 else '19') + timestr.replace('\'','')
		return timestr

	def _findyear(self,timestr):
		yearlist = list()
		if bool(self._year_regex.search(timestr)):
			yearstr = self._year_regex.findall(timestr)
			for x in yearstr:
				if x[0].count('-')>0:
					temp = x[0].split("-")
					for y in temp:
						if(self._formatyear(y) not in yearlist):
							self._timestr = self._timestr.replace(y,'')
							yearlist.append(int(self._formatyear(y)))
				else:
					if(self._formatyear(x[0]) not in yearlist):
						self._timestr = self._timestr.replace(x[0],'')
						yearlist.append(int(self._formatyear(x[0])))

		return yearlist

	def _findmonth(self,timestr):
		monthlist = list()
		if bool(self._month_regex.search(timestr)):
			monthstr = self._month_regex.findall(timestr)
			for x in monthstr:
				if(x[0][:3] not in monthlist):
					monthlist.append(x[0][:3].lower())

		return monthlist

	def _findtime(self,timestr):
		timelist = list()
		if bool(self._time_regex.search(timestr)):
			timestr = self._time_regex.findall(timestr)
			for x in timestr:
				if(x[0] not in timelist):
					timelist.append(x[0])
					self._timestr = self._timestr.replace(x[0],'')
		return timelist

	def _finddate(self,timestr):
		datelist = list()
		if bool(self._date_regex.search(timestr)):
			datestr = self._date_regex.findall(timestr)
			for x in datestr:
				if(x[0] not in datelist):
					datelist.append(int(x[0]))
					
		return datelist
