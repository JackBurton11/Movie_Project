from bs4 import BeautifulSoup
import requests

# html = requests.get('https://www.rottentomatoes.com/m/black_panther_2018')
# soup = BeautifulSoup(html.content, 'html.parser')
#
# name = soup.find(class_="mop-ratings-wrap__title mop-ratings-wrap__title--top")
# name_txt = name.get_text(strip=True)
#
# critic_rtg = soup.find_all(class_="mop-ratings-wrap__percentage")[0]
# critic_rtg_txt = critic_rtg.get_text(strip=True)
# critic_rtg_txt
#
# num_critic_reviews = soup.find_all(class_="mop-ratings-wrap__text--small")[1]
# num_critic_reviews_txt = num_critic_reviews.get_text(strip=True)
# num_critic_reviews_txt
#
# audience_rtg = soup.find_all(class_="mop-ratings-wrap__percentage")[1]
# audience_rtg_txt = audience_rtg.get_text(strip=True)
# audience_rtg_txt
#
# num_audience_reviews = soup.find_all(class_="mop-ratings-wrap__text--small")[2]
# num_audience_reviews_txt = num_audience_reviews.get_text(strip=True)
# num_audience_reviews_txt = num_audience_reviews_txt.split(' ')[2]
#
# studio = soup.find(class_= 'content-meta info')
# studio.find_all(class_= 'meta-value')[-1].get_text(strip=True)
#
# genre = soup.find(class_= 'content-meta info')
# genre_list = genre.find_all('a')
# genre_list
# genres = []
# for item in genre_list:
#     if 'genre' in item.get('href'):
#         genres.append(item.get_text())
# ', '.join(genres)

def rotten_scrape(movie_name, year=None):
### Function to scrape relevant movie information from Rotten Tomatoes website. Returns a dictionary with movie title, year, critc rating, audience rating, number of critic reviews, number of audience reviews, studio, and url of the source of the data. The function accepts 2 arguements: the first is a string (all lower case) containing the movie title and the second is the year (integer) that the movie was released###

#Create url string to be requested using movie name and year
    base_url = 'https://www.rottentomatoes.com/m/'
    movie_name = movie_name.replace(" ", "_")
    if year != None:
        movie_chain = base_url + movie_name + "_" + str(year)
    else:
        movie_chain = base_url + movie_name

#Request information and parse using BeautifulSoup
    html = requests.get(movie_chain)
    soup = BeautifulSoup(html.content, 'html.parser')

# Find relevant items by class in HTML. Parse objects of interests and coerce into target type for dictionary
    name = soup.find(class_="mop-ratings-wrap__title mop-ratings-wrap__title--top")
    name_txt = name.get_text(strip=True)


    critic_rtg = soup.find_all(class_="mop-ratings-wrap__percentage")[0]
    critic_rtg_txt = critic_rtg.get_text(strip=True)
    critic_rtg_txt = int(critic_rtg_txt[:-1])

    audience_rtg = soup.find_all(class_="mop-ratings-wrap__percentage")[1]
    audience_rtg_txt = audience_rtg.get_text(strip=True)
    audience_rtg_txt = int(audience_rtg_txt[:-1])

    num_critic_reviews = soup.find_all(class_="mop-ratings-wrap__text--small")[1]
    num_critic_reviews_txt = num_critic_reviews.get_text(strip=True)
    num_critic_reviews_txt = int(num_critic_reviews_txt.replace(",", ""))

    num_audience_reviews = soup.find_all(class_="mop-ratings-wrap__text--small")[2]
    num_audience_reviews_txt = num_audience_reviews.get_text(strip=True)
    num_audience_reviews_txt = num_audience_reviews_txt.split(' ')[2]
    num_audience_reviews_txt = int(num_audience_reviews_txt.replace(",", ""))

    studio = soup.find(class_= 'content-meta info')
    studio_txt = studio.find_all(class_= 'meta-value')[-1].get_text(strip=True)

    genre = soup.find(class_= 'content-meta info')
    genre_list = genre.find_all('a')
    genre_list
    genres = []
    for item in genre_list:
        if 'genre' in item.get('href'):
            genres.append(item.get_text())
    genre = ', '.join(genres)

    ###ADD WAY TO GET GENRE

# Create dictionary
    dict_ = {'url': movie_chain,
            'name': name_txt,
            'critic_rating': critic_rtg_txt,
            'audience_rating': audience_rtg_txt,
            'num_critic_reviews': num_critic_reviews_txt,
            'num_audience_reviews': num_audience_reviews_txt,
            'studio': studio_txt,
            'genre': genre


    }

    return dict_

rotten_scrape('a star is born', 2018)
rotten_scrape('12 strong')
