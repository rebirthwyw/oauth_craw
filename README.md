# oauth_craw

craw top 100000 website,judge if it use oauth for login

## top-100000.csv 
download from http://s3.amazonaws.com/alexa-static/top-1m.csv.zip  
timestamp is 2018-10-02-19:45  
```head -n 100000 top-1m.csv > top-100000.csv```  

## mysql
db OauthCraw  
table target(id,url)  
table result(id,url,isUse,oauthService,oauthLink,loginLink)  

## oauthService
base on https://en.wikipedia.org/wiki/List_of_OAuth_providers  
result in oauthService_collect.csv

## login
judge a link as a login link  
use words to identify
["login","signin","oauth"]  

## proxy
use mitmproxy to capture the 302  

## result.csv
in data folder  