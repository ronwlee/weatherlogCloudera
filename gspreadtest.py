import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('IOTcloudera-709dafe09ce9.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("WeatherLog").sheet1

arg1=1
arg2=2
arg3=3
ts = datetime.datetime.now()
print (ts)
wks.append_row([ts.ctime(),arg1,arg2,arg3])

