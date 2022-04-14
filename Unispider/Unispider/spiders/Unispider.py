from glob import glob
from math import degrees
from sys import dllhandle
from unicodedata import name
from xml.etree.ElementPath import xpath_tokenizer
import scrapy
from Unispider.items import UnispiderItem
import re
import os
from firebase_test import PushToFirebase

url = "https://gradadmissions.mit.edu/programs/degrees/masters-degrees"

class Unispider(scrapy.Spider):

    name = 'Unispider'
    start_urls = [url]

    def parse(self, response):
        
        program_id = []
        school_name = 'Massachusetts Institute of Technology'
        program_name = []
        program_website = []
        
        # crawl for program_id:
        for i in range(1,32):
            temp=response.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div['+str(i)+']/div[1]/span/a').extract()[0].split('>', 1)[1].split('<')[0] 
            # for example temp = 'Aeronautics and Astronautics'
            temp = temp.replace(' ','_').replace('/','or')
            temp = 'MIT_'+temp
            program_id.append(temp)

        # crawl for program_name
        for i in range(1,32):
            temp=response.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div['+str(i)+']/div[1]/span/a').extract()[0].split('>', 1)[1].split('<')[0] 
            # for example temp = 'Aeronautics and Astronautics'
            temp=temp.replace('/','or')
            program_name.append(temp)

        # crawl for application_deadline
        # for i in range(1,32):
        #     temp=response.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div['+str(i)+']/div[2]/div/span').extract()[0].split('>', 1)[1].split('<')[0] 
        #     # for example temp = 'December 15' -- change the format
        #     program_name.append(temp)
        
        # for program_website
        for i in range(1,32):
            temp = response.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div['
            +str(i)+']/div[1]').extract()[0].split('href="')[1].split('"',1)[0]     # get intermediate url
            program_website.append('https://gradadmissions.mit.edu'+temp)

        for i in range(31):
            this_program_id = program_id[i]
            this_school_name = school_name
            this_program_name = program_name[i]
            this_program_website = program_website[i]
            yield scrapy.Request(program_website[i], callback=self.nextScrawl, dont_filter=True, meta = {"program_id":this_program_id , "school_name":this_school_name,"program_name":this_program_name,"program_website":this_program_website})
    
    
    
    def nextScrawl(self, response):
        item = {}
        item["program_id"] = response.meta["program_id"]
        item["school_name"] = response.meta["school_name"]
        item["program_name"] = response.meta["program_name"]
        item["program_website"] = response.meta["program_website"]
        degree = []
        term_of_enrollment = []
        research_area = []
        requirements = []
        standardized_test_scores = []
        application_deadline = []
        interdisciplinary_program = []

        xpath_list = ["//*[@id]/div/div[2]/div[1]/div[1]/section", # degree
                    "//*[@id]/div/div[2]/div[1]/section/div/div",  # terms of enrollment
                    "//*[@id]/div/div[3]/div[1]/section/div/div", # areas of research
                    "//*[@id]/div/div[3]/div[2]/section/div", # Application Requirements //*[@id]/div/div[2]/div[1]/div/section/div/div
                    "//*[@id]/div/div[2]/div[1]/div/section/div/div",
                    "//*[@id]/div/div[2]/div[2]/section/div/div", # standardize test result
                    "//*[@id]/div/div[1]/div[1]/div[6]/section[3]/div", # deadline
                    "//*[@id]/div/div[2]/div[1]/div[2]/section/div"]# Interdisciplinary Programs
                     
    
        # begin = '<div class="field-items"><div class="field-item even">'
        # mid1 = '</div><div class="field-item odd">'
        # mid2 = '</div><div class="field-item even">'
        # end = '</div></div>'


                

        for i in xpath_list:
            
            try:
                temp = response.xpath(i).extract()[0]
            except:
                print("\n\n\n\n"+i+" "+"is an invalid xpath\n")
            else:
                # dealing with degree
                if(temp and i == "//*[@id]/div/div[2]/div[1]/div[1]/section"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    while 'Degrees:\xa0' in temp:
                        temp.remove('Degrees:\xa0')
                    degree=degree+temp
                elif(not temp):
                    degree.append("None")
                
                
                # dealing with term_of_enrollment
                if(temp and i == "//*[@id]/div/div[2]/div[1]/section/div/div"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    while 'Terms of Enrollment:\xa0' in temp:
                        temp.remove('Terms of Enrollment:\xa0')
                    term_of_enrollment=term_of_enrollment+temp
                    print("\n\n\n\n\n")
                    print("terms of enrollment")
                    print("terms of enrollment")
                    print("terms of enrollment")
                    print("terms of enrollment")
                    print("terms of enrollment")
                    print("terms of enrollment")
                    print(term_of_enrollment)
                    print("\n\n\n\n\n")
                elif(not temp):
                    term_of_enrollment.append("None")
                    print("elif(not temp)")
                    print("elif(not temp)")
                    print("elif(not temp)")
                    print("elif(not temp)")
                    print("elif(not temp)")
                    print("elif(not temp)")

                # research_area
                if(temp and i == "//*[@id]/div/div[3]/div[1]/section/div/div"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    research_area=research_area+temp
                elif(not temp):
                    research_area.append("Not Applicable")

                # requirement
                if(temp and i == "//*[@id]/div/div[3]/div[2]/section/div" or i=="//*[@id]/div/div[2]/div[1]/div/section/div/div"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    requirements=requirements+temp
                elif(not temp):
                    requirements.append("None")

                # standardized_test_scores
                if(temp and i == "//*[@id]/div/div[2]/div[2]/section/div/div"):
                    temp.replace('\n','')
                    standardized_test_scores.append(temp)
                elif(not temp):
                    standardized_test_scores.append("None")
                
                # for deadlines
                if(temp and i == "//*[@id]/div/div[1]/div[1]/div[6]/section[3]/div"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    application_deadline=application_deadline+temp
                elif(not temp):
                    application_deadline.append("None")
                
                # interdisciplinary_program
                if(temp and i == "//*[@id]/div/div[2]/div[1]/div[2]/section/div"):
                    temp = re.sub('<[^<]+?>', ';', temp).strip().split(";")
                    while '' in temp:
                        temp.remove('')
                    interdisciplinary_program=interdisciplinary_program+temp
                elif(not temp):
                    interdisciplinary_program.append("None")

        
        item['degree'] = degree
        item['term_of_enrollment'] = term_of_enrollment
        item['research_area'] = research_area
        item['requirements'] = requirements
        item['standardized_test_scores'] = standardized_test_scores
        item['application_deadline'] = application_deadline
        item['interdisciplinary_program'] = interdisciplinary_program

        PushToFirebase(program_id=item['program_id'],
                        school_name=item['school_name'],
                        program_name=item['program_name'],
                        program_website=item['program_website'],
                        degree=item['degree'],
                        term_of_enrollment=item['term_of_enrollment'],
                        research_area=item['research_area'],
                        requirements=item['requirements'],
                        standardized_test_scores=item['standardized_test_scores'],
                        application_deadline=item['application_deadline'],
                        interdisciplinary_program=item['interdisciplinary_program'])



            