
# coding: utf-8

# In[3]:


import requests


# In[4]:


page = requests.get('https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/released-in-2017')


# In[5]:


from bs4 import BeautifulSoup as BS
soup = BS(page.content, 'html.parser')
soup


# In[6]:


app_soup = BS(page.content, 'html.parser')


# In[7]:


links = []
for item in app_soup.find_all('a'):
    links.append(item.get('href'))


# In[8]:


links_2017 = links[78:178] 


# In[9]:


base = 'https://www.the-numbers.com'


# In[10]:


links_2017_list = []
for item in links_2017:
    links_2017_list.append(base + item)


# In[1]:


def movie_scrape(url, year1):
    movie = requests.get(url)
    movie1 = BS(movie.content, 'html.parser')
    name1 = movie1.find(itemprop='name').get_text()
    #finding movie name in website
    name2 = name1.replace(" (" + str(year1) + ")", "")
    #removing the year from the string
    name3 = name2.replace("'", '')
    #removing apostrophes as we will use the titles to webscrape Rotten Tomatoes later
    if 'â\x80\x99' in name3:
        name3 = name3.replace("â\x80\x99", "")
    elif 'â\x80\x94' in name3:
        name3 = name3.replace("â\x80\x94", " ")
        #removing apostrophes that appear this way in Python
    mf = movie1.find(id='movie_finances')
    #finding movie table with info on domestic box office and`this  
    dbo1 = mf.find_all(class_='data')[0].get_text()
    dbo2 = dbo1.replace(',', '')
    dbo = int(dbo2.replace('$', ''))
    # removing $ and commas to convert Domestic Box Office numbers into integers
    if len(mf.find_all(class_='data')) >= 6:
        dvs1 = mf.find_all(class_='data')[5].get_text()
        dvs2 = dvs1.replace(',', '')
        dvs = int(dvs2.replace('$', ''))
    else:
        dvs = None
    #removing $ and commas to convert Domestic Video Sales into integers. Using conditional statement as a few movies don't have that info. 
    md = movie1.find_all('table')
    pb1 = md[3].find_all('td')[1].get_text()
    pb2 = pb1.replace(',', '')
    pb = int(pb2.replace('$', ''))
    #finding the table with production budget and removing commas and $ to convert to integer
    md = movie1.find_all('table')
    rt = md[3].find_all('a')
    rating = None 
    for a in rt:
        if "mpaa-rating" in a.get('href'):
            rating = a.get_text()
    #webscraping rating
    year = str(year1)
    return {'id': url, 'name': name3, 'domestic_gross': dbo, 'est_dvd_sales': dvs, 'production_budget': pb, 'rating': rating, 'year': year}


# In[12]:


Movies_SQL = []
for url in links_2017_list:
    Movies_SQL.append(movie_scrape(url, 2017))


# In[13]:


def pull_movies_list(url):
    page1 = requests.get(url)
    soup = BS(page1.content, 'html.parser')
    links = []
    for item in soup.find_all('a'):
        links.append(item.get('href'))
    links_year = links[77:177] 
    base = 'https://www.the-numbers.com'
    links_year_list = []
    for item in links_year:
        links_year_list.append(base + item)
    return links_year_list


# In[14]:


links_2018_list = pull_movies_list('https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/released-in-2018')


# In[15]:


for url in links_2018_list:
    Movies_SQL.append(movie_scrape(url, 2018))

