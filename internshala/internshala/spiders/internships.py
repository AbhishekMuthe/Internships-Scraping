import scrapy
from time import sleep
import re
from datetime import datetime
import pandas as pd



class InternshipsSpider(scrapy.Spider):
    name = 'internships'
    allowed_domains = ['internshala.com']
    start_urls = ['https://internshala.com/']
    a = []
    b = []
    l = []
    d = []
    e = []
    f = []
    g = []
    h = []
    i = []
    j = []
    k = []
    global c
    c = 0
    
    
    def parse(self, response):
        start_urls = ['https://internshala.com/']
        url = ''.join(start_urls) + 'internships/'
        yield scrapy.Request(url, callback=self.parse2)

        
    def parse2(self, response):
        global c
        start_urls = ['https://internshala.com']
        links = response.xpath('//*[@class="view_detail_button"]/@href').extract()
        for link in links:
            sleep(1)
            if(c<100):
                c = c + 1
                detail_link = ''.join(start_urls) + link
                yield scrapy.Request(detail_link, callback=self.parse3, meta={'Internship_details_page_link': detail_link})
        if(c<100):
            next_page = response.xpath('//*[@rel="next"]/@href').extract_first()
            next_page_url = ''.join(start_urls) + next_page
            yield scrapy.Request(next_page_url, callback=self.parse2)


    def parse3(self,response,a=a,b=b,d=d,e=e,f=f,g=g,h=h,i=i,j=j,k=k,l=l):
        sleep(0.5)
        details_link = response.meta['Internship_details_page_link']
        job_role = response.xpath('//*[@class="profile_on_detail_page"]/text()').extract_first()
        l.append(job_role)
        company_name = response.xpath('//*[@class="link_display_like_text"]/text()').extract_first()
        regex = re.compile(r'[\n\r\t]')
        company_name = regex.sub(" ", company_name)
        company_name = re.sub(' +', ' ', company_name)
        company_name = company_name.strip(' ')
        a.append(company_name)
        company_link = response.xpath('//*[@id="details_container"]/div[3]/div[2]/div[2]/a/@href').extract_first()
        b.append(company_link)
        location = response.xpath('//*[@class="location_link"]/text()').extract_first()
        d.append(location)
        start_date = response.xpath('//*[@id="start-date-first"]/text()').extract_first()
        start_date = regex.sub(" ", start_date)
        start_date = re.sub(' +', ' ', start_date)
        start_date = start_date.replace("' ", " 20")
        start_date = start_date.strip(' ')
        if(start_date == ''):
            start_date = response.xpath('//*[@class="start_immediately_mobile"]/text()').extract_first()
            start_date = re.sub('[^ -~]',' ', start_date)
        e.append(start_date)    
        Durations = response.xpath('//div/*[@class="item_body"]/text()').extract()
        if(Durations!=[]):
            Duration = Durations[1]
            Duration = regex.sub(" ", Duration)
            Duration = re.sub(' +', ' ', Duration)
            Duration = Duration.strip(' ')
            if(Duration == ''):
                Duration = Durations[2]
                Duration = regex.sub(" ", Duration)
                Duration = re.sub(' +', ' ', Duration)
                Duration = Duration.strip(' ')
        f.append(Duration)
        applicants = response.xpath('//*[@class="applications_message"]/text()').extract_first()
        if(applicants == 'Be an early applicant'):
            applicants = 'NULL'
        g.append(applicants)
        openings = response.xpath('//div/*[@class="text-container"]/text()').extract()
        if(openings!=[]):
            openings = openings[-1]
            opening = re.sub('[^ -~]','', openings)
            opening = re.sub(' +', ' ', opening)
        h.append(opening)
        deadline = response.xpath('//div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/text()').extract_first()
        deadline = regex.sub(" ", deadline)
        deadline = re.sub(' +', ' ', deadline)
        deadline = deadline.replace("' ", " 20")
        deadline = str(datetime.strptime(deadline, '%d %b %Y'))
        deadline = deadline.rstrip('  00:00:00')
        lst_date = deadline.split("-")
        deadline = lst_date[2]+"-"+lst_date[1]+"-"+lst_date[0]
        i.append(deadline)
        stipend = response.xpath('//div[2]/div[1]/div[2]/span/text()').extract_first()
        Stipend = stipend.strip(' ')
        j.append(Stipend)
        k.append(details_link)
        df = pd.DataFrame({'Internship name': l, 'Internship details page link': k, 'Internship organization': a, 'Internship organization page link': b, 'Location of internship': d, 'Start date of internship': e, 'Duration': f, 'Stipend': j, 'deadline': i, 'Number of applicants': g, 'Number of openings': h})
        df.to_excel('internships.xlsx', index=False)     
        



        
