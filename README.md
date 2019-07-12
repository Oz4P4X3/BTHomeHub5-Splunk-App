# Splunk BT HomeHub 5 App

## About
This app will collect security related data from your BT HomeHub 5 and visualise it in a Splunk dashboard. This may work for other BT HomeHub versions however, this hasn't been tested. 

## Prerequisites 
The app requires Firefox to be installed on the search heads for the scripts to work. 

## Setup

1. Download the Splunk app
2. Update ```bin/assets/config.py``` with the following:

    ```
    * IP address for your BT HomeHub (default is 192.168.1.254)
    * Admin username for your BT HomeHub (default is admin)
    * Admin password (not WiFi) for your BT HomeHub (default is written on the password card provided with your BT HomeHub).
    ```

3. Install the app and enjoy :) 
