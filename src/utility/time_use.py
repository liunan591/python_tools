import datetime

"""string format
%Z	Time zone name (empty string if the object is naive).————(empty), UTC, EST, CST
%y	Year without century as a zero-padded decimal number.————00, 01, …, 99
%Y	Year with century as a decimal number.————0001, 0002, …, 2013, 2014, …, 9998, 9999
%m	Month as a zero-padded decimal number.————01, 02, …, 12
%b	Month as locale’s abbreviated name.————Jan, Feb, …, Dec (en_US);Jan, Feb, …, Dez (de_DE)
%B	Month as locale’s full name.————January, February, …, December (en_US);Januar, Februar, …, Dezember (de_DE)
%U	Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days 
    in a new year preceding the first Sunday are considered to be in week 0.	00, 01, …, 53
%W	Week number of the year (Monday as the first day of the week) as a decimal number. All days in a 
    new year preceding the first Monday are considered to be in week 0.	00, 01, …, 53
%a	Weekday as locale’s abbreviated name.————Sun, Mon, …, Sat (en_US);So, Mo, …, Sa (de_DE)
%A	Weekday as locale’s full name.————Sunday, Monday, …, Saturday (en_US);Sonntag, Montag, …, Samstag (de_DE)
%w	Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.————0, 1, …, 6
%d	Day of the month as a zero-padded decimal number.————01, 02, …, 31
%j	Day of the year as a zero-padded decimal number.————001, 002, …, 366
%p	Locale’s equivalent of either AM or PM.	————AM, PM (en_US);am, pm (de_DE)
%H	Hour (24-hour clock) as a zero-padded decimal number.————00, 01, …, 23
%I	Hour (12-hour clock) as a zero-padded decimal number.————01, 02, …, 12
%M	Minute as a zero-padded decimal number.————00, 01, …, 59
%S	Second as a zero-padded decimal number.————00, 01, …, 59
%f	Microsecond as a decimal number, zero-padded on the left.————000000, 000001, …, 999999
%%	A literal '%' character.
"""

#date
#class methods
datetime.date(year, month, day)
datetime.date.today() #equivalent to datetime.date.fromtimestamp(time.time())
datetime.date.fromordinal(6666) #creat date form the number between now and 1-1-1
dt1 = datetime.date.fromisoformat("1999-12-03") #"1999-12-3" is not allowed
#Instance attributes (read-only):
date.year   #Between MINYEAR and MAXYEAR inclusive.
date.month  #Between 1 and 12 inclusive.
date.day    #Between 1 and the number of days in the given month of the given year.
#Instance methods: > < >= ==
date2 = dt1 + timedelta
date2 = dt1 - timedelta   #timedelta = date1 - date2
dt1.ctime() #Return a string representing the date,such as 'Wed Dec 4 00:00:00 2002'
dt1.replace(year=self.year, month=self.month, day=self.day)
dt1.toordinal()   #Return the ordinal of the date, where January 1 of year 1 has ordinal 1.
dt1.weekday() #Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
dt1.isoweekday()  #Return the day of the week as an integer, where Monday is 1 and Sunday is 7. 
dt1.isocalendar() #Return a 3-tuple, (ISO year, ISO week number, ISO weekday).
dt1.isoformat()   #Return a string representing the date in ISO 8601 format, ‘YYYY-MM-DD’.
dt1.strftime("format")    #Return a string representing the date, controlled by an explicit format string.

#datetime
datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
dt = datetime.datetime.today()   #Return the current local datetime
datetime.datetime.now(tz=None)   #Return the current local date and time. 
datetime.datetime.utcnow()  #Return the current UTC date and time
datetime.datetime.fromtimestamp(timestamp, tz=None)  #Return the local date and time corresponding to the POSIX timestamp, such as is returned by time.time()
datetime.datetime.utcfromtimestamp(timestamp)    #Return the UTC datetime corresponding to the POSIX timestamp, with tzinfo None.
datetime.datetime.fromordinal(ordinal)   #Return the datetime corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1.
datetime.datetime.combine(date, time, tzinfo=self.tzinfo)    #Return a new datetime object
datetime.datetime.strptime(date_string, format)  #Return a datetime corresponding to date_string, parsed according to format.


#time delta
#class methods
"""0 <= microseconds < 1000000; 0 <= seconds < 60*60*24; -999999999 <= days <= 999999999"""
datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
#Instance attributes (read-only):
days	#Between -999999999 and 999999999 inclusive
seconds	#Between 0 and 86399 inclusive
microseconds	#Between 0 and 999999 inclusive
#operations:: + - * /a
t1 = 2.5 * datetime.timedelta(seconds=2500)
f = datetime.timedelta(seconds=2500)/datetime.timedelta(seconds=100)
i1 = datetime.timedelta(seconds=2500)//datetime.timedelta(seconds=101)#The floor is computed
f2 = datetime.timedelta(seconds=2500)%datetime.timedelta(seconds=101) #The remainder is computed
i1, f2 = divmod(datetime.timedelta(seconds=2500),datetime.timedelta(seconds=101))
t = abs(-f)
f_s = f.total_seconds() #equivalent to f/datetime.timedelta(seconds=1)
