from flask import Flask,render_template
from flask import request
from project import priceSearch
from project import test2
import json



myApp = Flask(__name__)

@myApp.route("/")
def home():
    return render_template("index2.html")

#@myApp.errorhandler(Exception)
#def handleError(e):
#    return render_template("errorPage.html")
@myApp.route("/error", methods=['get'])
def error():
    return render_template("errorPage.html")

@myApp.route("/selectProduct", methods=['get'])
def selectProduct():
    return render_template("selectProduct.html")

@myApp.route("/Product", methods=['POST'])
def Product():
    
    data=request.json
    key_word_obj=priceSearch.Product(data['product'])
    
    
    if(data['site']=='ebay'):
        data1=test2.get_proxy_send_request(key_word_obj.keyword_ebay)
        temp=key_word_obj.parse_stuff_ebay(data1)
        json_new=json.dumps(temp)
        return json_new
    elif(data['site']=='amzn'):
        data1=test2.get_proxy_send_request(key_word_obj.keyword_ebay)
        
        temp=key_word_obj.parse_stuff_amazon(data1)
        

        json_new=json.dumps(temp)
        
        return json_new
    elif(data['site']=='etsy'):
        data1=test2.get_proxy_send_request(key_word_obj.keyword_etsy)
        
        temp=key_word_obj.parse_etsy(data1)
        print(temp)
        json_new=json.dumps(temp)
        return json_new
    else:
        data1=test2.get_proxy_send_request(key_word_obj.keyword_amazon)
        data2=test2.get_proxy_send_request(key_word_obj.keyword_ebay)
        data3=test2.get_proxy_send_request(key_word_obj.keyword_etsy)
        key_word_obj.parse_stuff_amazon(data1)
        key_word_obj.parse_stuff_ebay(data2)
        key_word_obj.parse_etsy(data3)
        key_word_obj.remove_dups()

        json_new=json.dumps(key_word_obj.all_products)
        return json_new

if __name__=='__main__':
    myApp.run()
