from newsapi import DataGatherer
from util.log import Logger
from datetime import datetime
from dateutil.tz import *


Logger.info('=====================Job Starting at: ' + str(datetime.now().astimezone(tzlocal())))
DataGatherer().indian_business_news()
Logger.info('=====================Job Completed at: ' + str(datetime.now().astimezone(tzlocal())))
