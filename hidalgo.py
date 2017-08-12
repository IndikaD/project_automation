# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Hidalgo(unittest.TestCase):


    def setUp(self):
        path = "D:\\Personal\\Projects\\Guru\\chromedriver.exe"
        self.driver = webdriver.Chrome(path)
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://pa.co.hidalgo.tx.us/"
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_hidalgo(self):
        driver = self.driver
        driver.get(self.base_url + "/default.aspx")
        driver.find_element_by_link_text("Jail Records").click()
        csv_path = "D:\\Personal\\Projects\\Guru\\inmates.csv"
        fname = ""
        lname = ""
        mname = ""
        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fname = row['FNAME']
                xname=fname.split()
                fname = xname[0]
                del xname[0]
                mname= ' '.join(xname)
                lname = row['LNAME']

                print xname
                print "L: "+lname + " F: "+ str(fname) + " M: "+mname

                driver.find_element_by_id("LastName").clear()
                driver.find_element_by_id("LastName").send_keys(lname)
                driver.find_element_by_id("FirstName").clear()
                driver.find_element_by_id("FirstName").send_keys(fname)
                driver.find_element_by_id("MiddleName").clear()
                driver.find_element_by_id("MiddleName").send_keys(mname)
                driver.find_element_by_id("DateBookingOnAfter").clear()
                driver.find_element_by_id("DateBookingOnAfter").send_keys("01/01/1985")
                driver.find_element_by_id("SearchSubmit").click()

                #return to home
                driver.find_element_by_link_text("New Jail Search").click()

                #driver.find_element_by_link_text("F-1081-17").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
