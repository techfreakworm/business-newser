from newsapi import DataGatherer
from util.log import Logger
from datetime import datetime
from tzlocal import get_localzone

tz = get_localzone()
Logger.info('=====================Job Starting at: ' + str(tz.localize(datetime.now())))
DataGatherer().indian_business_news()
Logger.info('=====================Job Completed at: ' + str(tz.localize(datetime.now())))
