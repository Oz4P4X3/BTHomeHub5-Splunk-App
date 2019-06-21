import os
import re
from assets import config

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# stores the location of the firefox driver
firefox_driver_path = os.path.dirname(os.path.realpath(__file__)) + "/assets/geckodriver"

# run firefox headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=firefox_driver_path)

# go to the relevant page on the BT HomeHub
driver.get('http://{}/index.cgi?active_page=9121&request_id=1825134365&nav_clear=1'.format(config.BTHomeHub_ip))

# insert password and click the relevant buttons
password_field = driver.find_element_by_id("password").send_keys(config.password)
driver.find_element_by_xpath('//*[@id="frame_div"]/table/tbody/tr[14]/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/div/table/tbody/tr[2]/td[2]').click()
uptime = driver.find_element_by_xpath('//*[@id="PTS"]').text

# extract the days and hours from the uptime returned by the BT HomeHub
days = re.findall(r"^\d", str(uptime))
hours = re.findall(r"\d{2}:\d{2}:\d{2}", str(uptime))

# arrange output into a Splunk friendly way
print("days=" + days[0] + " " + "hours=" + hours[0])

driver.quit()
