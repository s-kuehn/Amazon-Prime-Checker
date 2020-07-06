# -*- coding: utf-8 -*-
import re
import csv
import urllib
import mechanize
import time
from bs4 import BeautifulSoup

# initialize simulated chrome browser
chrome = mechanize.Browser()
chrome.set_handle_robots(False)
chrome.addheaders = [('User-agent', 
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]

print('\n')

with open("ASIN.txt", "r") as text_file:
    for asin in text_file:
        print(asin.rstrip())
        included = False
        primecounter = 0 
        namelist = []
        with open('PrimeSellers.csv', 'a', newline='') as createFile:
            pass
        with open('PrimeSellers.csv', 'r', newline='', encoding='utf-8') as asinfile:
            reader = csv.reader(asinfile)
            for row in reader:
                if asin.rstrip() in row[0]:
                    included = True
                    break
        if included == False:
            Error_status = False
            try:
                url = chrome.open(f"https://www.amazon.com/gp/offer-listing/{asin.rstrip()}")
                soup = BeautifulSoup(url, 'html.parser')
                with open("Output.txt", "w", encoding='utf-8') as text_file:
                    text_file.write(str(soup))

                with open("Output.txt", "r", encoding='utf-8') as text_file:
                    textParse = BeautifulSoup(text_file, 'html.parser')

                    with open('PrimeSellers.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                        csvWriter = csv.writer(csvfile)
                            
                        if csvfile.tell() == 0:
                            csvWriter.writerow(['Product ASIN', 'Seller Name', 'Prime Status', 'Condition'])

                        sName = ''
                        pStatus = ''
                        qCondition = ''

                        for i in textParse.findAll("div", {'class': 'a-row a-spacing-mini olpOffer'}):
                            name = i.find("h3", {'class': 'a-spacing-none olpSellerName'})
                            qCondition = i.find("div", {'class':'a-section a-spacing-small'}).get_text().strip()
                            if "img" in str(name):
                                 # print("Amazon")
                                sName = "Amazon"
                            else:
                                # print(name.get_text().strip())
                                sName = name.get_text().strip()

                            if i.find("i", {'class': 'a-icon a-icon-prime'}):
                                # print("Prime")
                                pStatus = "Prime"
                            else:
                                # print("Not Prime")
                                pStatus = "Not Prime"
                            if i.find("i", {'class': 'a-icon a-icon-prime'}) and "img" not in str(name) and qCondition == 'New' and name.get_text().strip() not in namelist:
                                primecounter += 1
                                namelist.append(name.get_text().strip())

                            #print(f'ASIN: {asin.rstrip()}, Seller: {sName}, Prime Status: {pStatus}, Condition: {qCondition}')
                                
                            csvWriter.writerow([asin.rstrip(), sName, pStatus, qCondition])

                                # print('\n')
            #if there is an error with mechanize then try it all again 
            except:
                time.sleep(2)
                try:
                    url = chrome.open(f"https://www.amazon.com/gp/offer-listing/{asin.rstrip()}")
                    soup = BeautifulSoup(url, 'html.parser')
                    with open("Output.txt", "w", encoding='utf-8') as text_file:
                        text_file.write(str(soup))

                    with open("Output.txt", "r", encoding='utf-8') as text_file:
                        textParse = BeautifulSoup(text_file, 'html.parser')

                        with open('PrimeSellers.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                            csvWriter = csv.writer(csvfile)
                            
                            if csvfile.tell() == 0:
                                csvWriter.writerow(['Product ASIN', 'Seller Name', 'Prime Status', 'Condition'])

                            sName = ''
                            pStatus = ''
                            qCondition = ''

                            for i in textParse.findAll("div", {'class': 'a-row a-spacing-mini olpOffer'}):
                                name = i.find("h3", {'class': 'a-spacing-none olpSellerName'})
                                qCondition = i.find("div", {'class':'a-section a-spacing-small'}).get_text().strip()
                                if "img" in str(name):
                                    # print("Amazon")
                                    sName = "Amazon"
                                else:
                                    # print(name.get_text().strip())
                                    sName = name.get_text().strip()

                                if i.find("i", {'class': 'a-icon a-icon-prime'}):
                                    # print("Prime")
                                    pStatus = "Prime"
                                else:
                                    # print("Not Prime")
                                    pStatus = "Not Prime"
                                if i.find("i", {'class': 'a-icon a-icon-prime'}) and "img" not in str(name) and qCondition == 'New' and name.get_text().strip() not in namelist:
                                    primecounter += 1
                                    namelist.append(name.get_text().strip())

                                #print(f'ASIN: {asin.rstrip()}, Seller: {sName}, Prime Status: {pStatus}, Condition: {qCondition}')
                                
                                csvWriter.writerow([asin.rstrip(), sName, pStatus, qCondition])

                                # print('\n')
                except:
                    Error_status = True      
            if Error_status == False:
                print('Prime Sellers: '+ str(primecounter) )
            else:
                print("Failed to Load URL")          
        else:
            print(f'ASIN: {asin.rstrip()} already in file.')




