import os
from assets import config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# stores the location of the firefox driver
firefox_driver_path = os.path.dirname(os.path.realpath(__file__)) + "/assets/geckodriver"

# run firefox headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=firefox_driver_path)

# go to the page on BTHomeHub 5 where the hostname and ip address table is.
driver.get('http://{}/index.cgi?active_page=9098&request_id=139483056&nav_clear=1'.format(config.BTHomeHub_ip))
table = driver.find_element_by_xpath('//*[@id="frame_div"]/table[3]/tbody').text

# split the "My Home Network" table returned by selenium into an obj by new lines.
tableObj = (table.splitlines())

# iterate through the table and pull out the hostname, mac address and ip address and format in a way Splunk likes.
for i in range(len(tableObj)):
    lineObj = tableObj[i].split()
    if len(lineObj) == 3:
        print("hostname=" + lineObj[0] + " " + "mac_address=" + lineObj[1] + " " + "ip_address=" + lineObj[2])
    elif len(lineObj) == 4 and lineObj[1] != "No":
        print("hostname=" + lineObj[1] + " " + "mac_address=" + lineObj[2] + " " + "ip_address=" + lineObj[3])
    elif len(lineObj) == 6 and lineObj[0] != "Find" and lineObj[0] != "Network" and lineObj[3] != "No":
        print("hostname=" + lineObj[3] + " " + "mac_address=" + lineObj[4] + " " + "ip_address=" + lineObj[5])

# closes the browser once all operations have finished
driver.quit()

