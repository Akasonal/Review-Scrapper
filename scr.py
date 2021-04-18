import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
search_product=input()
url="https://www.flipkart.com/search?q="+search_product.replace(" ","")
uClient=uReq(url)   #opening the url
url=uClient.read() #reading the url
uClient.close()          #closing the connection this is must needed thing when we are doing scrapping
soup=BeautifulSoup(url,"html.parser") #parsing the html file for given product page
ratings=[]
headings=[]
user_comments=[]
names=[]
likes_count=[]
n_data=soup.find_all("div",class_="_1AtVbE col-12-12")   #finding all the product present on requested page
data=n_data[2]
for page in range(1, 22):
    click_data = "https://www.flipkart.com" + data.div.div.div.a["href"].format(page)  # clicking on that particular bject link
    req = requests.get(click_data)
    soup_next = BeautifulSoup(req.text, "html.parser")
    comment_boxes = soup_next.find_all("div", class_="col _2wzgFH")
    for comment in comment_boxes:
        rating = comment.find("div", {"class": "_3LWZlK _1BLPMq"})
        if rating is not None:  # if there will be some ratings
            ratings.append(float(rating.text))
        else:  # if the rating will be missing then will add null values
            ratings.append(np.nan)
        heading = comment.find("p", class_="_2-N8zT")
        if heading is not None:
            headings.append(heading.text)
        else:
            headings.append(np.nan)
        user_comment = comment.find("div", class_="t-ZTKy")
        if user_comment is not None:
            user_comments.append(user_comment.text)
        else:
            user_comments.append(np.nan)
        name = comment.find("p", class_="_2sc7ZR _2V5EHH")
        if name is not None:
            names.append(name.text)
        else:
            names.append(np.nan)
        like_count = comment.find("span", class_="_3c3Px5")
        if like_count is not None:
            likes_count.append(like_count.text)
        else:
            likes_count.append(np.nan)

dict1={"ratings":ratings,"header":headings,"comments":user_comments,"user name":names,"number of likes":likes_count} #saving all these data into dictionary file
df=pd.DataFrame(dict1)
df.to_csv("final_result1.csv")


