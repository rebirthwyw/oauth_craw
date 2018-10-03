###oauth_craw

craw top 100000 website,judge if it use oauth for login

###top-100000.csv 
download from http://s3.amazonaws.com/alexa-static/top-1m.csv.zip
timestamp is 2018-10-02-19:45
```head -n 100000 top-1m.csv > top-100000.csv```

###mysql
db oauth_craw
table target(id,url)
table result(id,url,isUse,oauthService,oauthLink,loginLink)

###oauthService
base on https://en.wikipedia.org/wiki/List_of_OAuth_providers
