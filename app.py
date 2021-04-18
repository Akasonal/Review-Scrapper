import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import pandas as pd
import numpy as np
product=input("Enter the product name \n") #enter the product name whose review you want to scrap
url="https://www.flipkart.com/search?q="+product.replace(" ","")
uClient=uReq(url)  #requesting the url
url=uClient.read() #reading the url
uClient.close()    #closing the connection
soup=BeautifulSoup(url,"html.parser") #parsing the html page
data_class=soup.find_all("div",{"class":"_1AtVbE col-12-12"})
data=data_class[2]
# here are the following things we are going to scrap
ratings = []
comment_headings = []
user_comments = []
user_names = []
number_of_likes = []
locations = []
for page in range(1,41):    #prininting the reviews of first 30 pages
    url = "https://www.flipkart.com" + data.div.div.div.a["href"].format(page)  # link
    req = requests.get(url)  # setting the connection with given website
    soup_updated = BeautifulSoup(req.text, "html.parser")  # parse the data
    comments = soup_updated.find_all("div", {"class": "col _2wzgFH"})
    # upper code will print all the data present in comment class
    for comment in comments:
        rating = comment.find("div", class_="_3LWZlK _1BLPMq")
        if rating is not None:
            ratings.append(rating.text)
        else:
            ratings.append(np.nan)
        comment_heading = comment.find("p", class_="_2-N8zT")
        if rating is not None:
            comment_headings.append(comment_heading.text)
        else:
            comment_headings.append(np.nan)
        user_comment = comment.find("div", class_="t-ZTKy")
        if user_comment is not None:
            user_comments.append(user_comment.text)
        else:
            user_comments.append(np.nan)
        user_name = comment.find("p", class_="_2sc7ZR _2V5EHH")
        if user_name is not None:
            user_names.append(user_name.text)
        else:
            user_names.append(np.nan)
        location = comment.find("p", class_="_2mcZGG")
        if location is not None:
            locations.append(location.text)
        else:
            locations.append(np.nan)
        likes_count = comment.find("span", class_="_3c3Px5")
        if likes_count is not None:
            number_of_likes.append(likes_count.text)
        else:
            number_of_likes.append(np.nan)
#taking all these scrapped information into dictionary format
dict1={"users":user_names,"ratings":ratings,    "heading":comment_headings,"reviews":user_comments, "location":locations,"likes count":number_of_likes}
#converting all the scrapped data into dataframe
df_scrapped=pd.DataFrame(dict1)
print(df_scrapped.head())
df_scrapped.to_csv("scrapped_df.csv")
