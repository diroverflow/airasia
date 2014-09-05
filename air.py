#!/usr/bin/python
#coding=utf-8

import urllib
import urllib2
import sys,os,string
from HTMLParser import HTMLParser

tagstack = []  
class ShowStructure(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.getflag = 0
        self.aork = 0
        self.price = {}
        self.pairs = []
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if len(attrs) == 0: pass
            else:
                for (variable, value)  in attrs:
                    if variable == "class" and value == "paxTypeDisplay":
                        self.getflag = 1
                    elif variable == "class" and value == "price":
                        self.getflag = 2
    def handle_endtag(self, tag):
        if tag == "div":
            self.getflag = 0
    def handle_data(self, data):  
        if data.strip():  
            if self.getflag == 1:
                if data == "Adult":
                    self.aork = 1
                elif data == "Kid":
                    self.aork = 2
            elif self.getflag == 2:
                if self.aork == 1:
                    self.price['adult']=data.replace(' MYR','').replace(' CNY','').replace(',','')
                elif self.aork == 2:
                    self.price['kid']=data.replace(' MYR','').replace(' CNY','').replace(',','')
                    self.pairs.append(self.price)
                    self.price = {}

def totalmin(prices):
    lowest = 100000
    lowpair = {}
    for pair in prices:
        adult = float(pair['adult'])
        kid = float(pair['kid'])
        total = adult+kid
        if total < lowest:
            lowest = total
            lowpair = pair
    print lowpair
    
def post(url, data):
	req = urllib2.Request(url)
	data = urllib.urlencode(data)
	#enable cookie
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req, data)
	return response.read()

def getoneday(fromcity,destcity,yearmonth,day):
	posturl = "http://booking.airasia.com/Select.aspx"
	data = {'__EVENTTARGET':'', '__EVENTARGUMENT':'', '__VIEWSTATE':'/wEPDwUBMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFP0NvbnRyb2xHcm91cFNlbGVjdFZpZXckU3BlY2lhbE5lZWRzSW5wdXRTZWxlY3RWaWV3JENoZWNrQm94U1NSc2KF+3FBQndP4mQD4nrPT4PNXNaR', 'pageToken':'', 'MemberLoginSelectView$HFTimeZone':'480', 'ControlGroupAvailabilitySearchInputSelectView$ButtonSubmit':'Go', 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$RadioButtonMarketStructure':'OneWay', 'ControlGroupAvailabilitySearchInputSelectView_AvailabilitySearchInputSelectVieworiginStation1':fromcity, 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$TextBoxMarketOrigin1':fromcity, 'ControlGroupAvailabilitySearchInputSelectView_AvailabilitySearchInputSelectViewdestinationStation1':destcity, 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$TextBoxMarketDestination1':destcity, 'date_picker':'', 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListMarketDay1':day, 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListMarketMonth1':yearmonth, 'date_picker':'', 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListMarketDay2':day, 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListMarketMonth2':yearmonth, 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListPassengerType_ADT':'3', 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListPassengerType_CHD':'1', 'ControlGroupAvailabilitySearchInputSelectView$AvailabilitySearchInputSelectView$DropDownListPassengerType_INFANT':'0', 'ControlGroupAvailabilitySearchInputSelectView$MultiCurrencyConversionViewSelectView$DropDownListCurrency':'default'}
	resp=post(posturl, data)
	getprice = ShowStructure()
	getprice.feed(resp)
	getprice.close()
	totalmin(getprice.pairs)

def main():
    for year in range(2014,2015):
        for month in range(10, 11):
            for day in range(1,32):
                if(day == 31 and month in (2,4,6,9,11)):
                    continue
                yearmonthstr = '%d-%.02d' % (year, month)
                daystr = '%.02d' % day
                print '%s-%s' % (yearmonthstr, daystr)
                getoneday('PEK', 'KUL', yearmonthstr, daystr) #KUL-Kuala Lumpur,HKT-Phucket

if __name__ == '__main__':
	main()
