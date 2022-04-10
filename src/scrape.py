from util.selenium_dispatcher import SeleniumDispatcher


sel = SeleniumDispatcher()

driver = sel.get_driver()
driver.get('https://yahoo.com')
print('Working fine')