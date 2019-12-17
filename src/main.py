from newsapi import DataGatherer
from util.log import Logger
from datetime import datetime
from tzlocal import get_localzone


Logger.info('=====================Job Starting at: ' + str(datetime.now().astimezone(get_localzone())))
DataGatherer().indian_business_news()
Logger.info('=====================Job Completed at: ' + str(datetime.now().astimezone(get_localzone())))
