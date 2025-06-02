
from apiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import numpy as np
#import test2


class Product:
    def __init__(self,prod):
        
        self.prod=prod
        self.api_key=''
        self.keyword_ebay=f"https://www.ebay.com/sch/i.html?_nkw={prod}&LH_Complete=1&LH_Sold=1&_pgn=1"
        self.keyword_amazon=f"https://www.amazon.com/s?k={prod}&page=1"
        self.keyword_etsy=f"https://www.etsy.com/search?q={prod}&ref=search_bar"
        self.all_products=[]
        
        
        

    def data_fetch(self,URL):
        header={
            "Accept":" */*",
            "Accept-Encoding":" gzip, deflate, br",
            "Accept-Language":" en-US,en;q=0.9",
            "Connection":" keep-alive",
            "Content-Length":"204",
            "Content-Type":" application/json",
            "Origin":" https",
            "Referer":" https",
            "sec-ch-ua-mobile":" ?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest":" empty",
            "Sec-Fetch-Mode":" cors",
            "Sec-Fetch-Site":" cross-site",
            "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            }
        r=requests.get(url=URL,headers=header)
        
        print(r)
        data_d=BeautifulSoup(r.text,'html.parser')
        
        return data_d

    def parse_stuff_ebay(self,data_d):
        
        parsed = data_d.find_all('div', {'class': 's-item__wrapper clearfix'})
        
        for record in parsed:
                price_container = record.find('span', {'class': 's-item__price'})
                positive_price = price_container.find('span', {'class': 'POSITIVE'}) if price_container else None
                title_tag = record.find('span', {'role': 'heading'})
                tagblock = record.find('div', {'class': 's-item__title--tagblock'})
                positive_date = tagblock.find('span', {'class': 'POSITIVE'}) if tagblock else None
                bids_tag = record.find('span', {'class': 's-item__bids s-item__bidCount'})
                link_tag = record.find('a', {'class': 's-item__link'})
                image_tag = record.find('div', {'class': 's-item__image-wrapper image-treatment'})
                img = image_tag.find('img') if image_tag else None

                print("price cont",price_container)
                print("title:",title_tag)
                print("pos date:",positive_date)
                
                print("link",link_tag)
                print("image_tag",image_tag)
               
                print("pos_price:",positive_price)

                if positive_price and title_tag  and link_tag and img:
                    product = {
                        'website': 'Ebay',
                        'title': title_tag.text.strip(),
                        'sold_price': positive_price.text.strip().replace('$', '').replace(',', ''),
                        #@'soldDate': positive_date.text.strip(),
                        'bids': str(bids_tag) if bids_tag else '',
                        'links': link_tag['href'],
                        'image': img['src']
                    }
                    print(product)
                    self.all_products.append(product)

        return self.all_products

    def parse_stuff_amazon(self,data_d):
        data_d_stuff={}
        parsed=data_d.find_all('div',{'class':'s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis s-latency-cf-section s-card-border'})
        
        if parsed == []:
            parsed=data_d.select('div[class*="s-card-container s-overflow-hidden aok-relative puis"]')
        print(parsed) 
        self.route_amazon_request(parsed,data_d_stuff)
       
                       
                       
                        
                    
                    
        return self.all_products
    def parse_etsy(self,data_d):
        parsed=data_d.find_all('div',{'class':'wt-height-full'})
        print(parsed)
        for record in parsed:
            if record.select_one('h3[class*="wt-text-caption v2-listing-card"]'):
                product={
                        'website':'Etsy',
                        'title': record.select_one('h3[class*="wt-text-caption v2-listing-card"]').get_text().replace("\n","").strip(),
                        'sold_price':record.find('span',{'class':'currency-value'}).text,
                        'soldDate':'not available',
                        'bids':'not available',
                        'links':record.select_one('a[class*="listing-link wt-display-inline-block"]')['href'],
                        'image':record.find('div',{'class':"height-placeholder"}).find('img')['src']
                    }
                
                self.all_products.append(product)
        
        
        return self.all_products

    def route_amazon_request(self,parsed,data_d_stuff):
        for record in parsed:
            
             if record.find('span',{'class':'a-price-whole'})!=None:
                    sold_price=str(record.find('span',{'class':'a-price-whole'}))
                    decimal=str(record.find('span',{'class':'a-price-fraction'}))
                    index_price_g=sold_price.index('>')
                    index_price_l=sold_price[1:].index('<')
                    index_price_g_dec=decimal.index('>')
                    index_price_l_dec=decimal[1:].index('<')
                    s_price=sold_price[index_price_g+1:index_price_l+1]+'.'+decimal[index_price_g_dec+1:index_price_l_dec+1]
                    s_price=s_price.replace(",","")    
                    product={
                        'website':'Amazon',
                        'title': str(record.select_one('span[class*="a-color-base a-text-normal"]').get_text()),
                        'sold_price':s_price,
                        'soldDate':"no data",
                        'bids':"no data",
                        'links':"https://www.amazon.com"+record.find('a', {'class':'a-link-normal s-no-outline'})['href'],
                        'image':record.find('img')['src']
                        }
                    if data_d_stuff.get(product["title"])==None:
                        self.all_products.append(product)
                        data_d_stuff[product["title"]]=1
                    
        return self.all_products
    
    def remove_dups(self):
        prodList=self.all_products
        seen = set()
        new_l = []
        for d in prodList:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)
        self.all_products=new_l

        
        
#keyWordObj=Product("hats") 
#data1=test2.getProxySendRequest(keyWordObj.keyword_etsy)
#temp=keyWordObj.parseEtsy(data1)
#print(temp)          
                
        

