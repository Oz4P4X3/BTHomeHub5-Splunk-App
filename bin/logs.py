import datetime
from assets import config
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# stores the location of the firefox driver
firefox_driver_path = os.path.dirname(os.path.realpath(__file__)) + "/assets/geckodriver"

# run firefox headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=firefox_driver_path)

# go to the relevant page on the BT HomeHub
driver.get('http://{}/?active_page=9144&request_id=1659938290&nav_clear=1'.format(config.BTHomeHub_ip))

# insert password and click the relevant buttons
password_field = driver.find_element_by_id("password").send_keys(config.password)
driver.find_element_by_xpath('//*[@id="frame_div"]/table/tbody/tr[14]/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr[2]/td[2]').click()

table = driver.find_element_by_xpath('//*[@id="frame_div"]/table[2]/tbody').text
tableObj = (table.splitlines())
lastEvent = tableObj[0].split()
eventTimeDate = lastEvent[1] + " " + lastEvent[2].replace(".", " ") + str(datetime.datetime.now().year) + " " +\
                lastEvent[0].replace(",", "")
compareTime = datetime.datetime.now() - datetime.timedelta(minutes=30)
compareTime = compareTime.strftime("%d %b %Y %H:%M:%S")

# while the event time is greater then 30 minutes (last time splunk ran the scripted input) print for splunk to ingest.
while eventTimeDate > compareTime:
    # get text from table
    table = driver.find_element_by_xpath('//*[@id="frame_div"]/table[2]/tbody').text
    tableObj = (table.splitlines())
    # remove the table header
    tableObj.remove("Time and date Message")
    # get the number of rows on the table
    length = len(tableObj)
    i = 0

    #for each row
    while i < length:
        # separate into lines
        lineObj = tableObj[i].split()

        # if the line is shorter than 10 characters, remove it as this isn't a complete event
        if len(tableObj[i]) < 10:
            deleted = tableObj.pop(i)
            i -= 1
            length = len(tableObj)
        else:
            # extract the timestamp for the while statement
            eventTimeDate = lineObj[1] + " " + lineObj[2].replace(".", " ") + str(datetime.datetime.now().year) + " " \
                            + lineObj[0].replace(",", "")
            # if the event is in the correct time range, print it for Splunk to ingest
            if eventTimeDate > compareTime:
                print(tableObj[i])
            i += 1
    # go to the next page of logs
    driver.find_element_by_xpath('//*[@id="frame_div"]/table[2]/tbody/tr[103]/td/table/tbody/tr/td[3]/table/tbody/tr/td'
                                 '/div/table/tbody/tr[2]/td[2]/span/a').click()

# close the webdriver once all the required data is extracted
driver.quit()
