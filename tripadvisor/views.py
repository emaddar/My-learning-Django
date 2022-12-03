from django.shortcuts import render

# Create your views here.



# Import the libraries.
import requests
from bs4 import BeautifulSoup
import pandas as pd




def tripadvisor_scraper():

    # Extract the HTML and create a BeautifulSoup object.
    url = ('https://www.tripadvisor.fr/Hotels-g187178-Lille_Nord_Hauts_de_France-Hotels.html')

    user_agent = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/90.0.4430.212 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    def get_page_contents(url):
        page = requests.get(url, headers = user_agent)
        return BeautifulSoup(page.text, 'html.parser')

    soup = get_page_contents(url)

    # Find and extract the data elements.
    hotels = []
    for name in soup.findAll('div',{'class':'listing_title'}):
        hotels.append(name.text.strip())

    ratings = []
    for rating in soup.findAll('a',{'class':'ui_bubble_rating'}):
        ratings.append(rating['alt'])  

    reviews = []
    for review in soup.findAll('a',{'class':'review_count'}):
        reviews.append(review.text.strip())

    prices = []
    for p in soup.findAll('div',{'class':'price-wrap'}):
        prices.append(p.text.replace('₹','').strip())  

    # links = []
    # adress = []
    # i = 1
    # for l in soup.find_all('a', {'class': 'property_title prominent'}):
    #     url_page = f"https://www.tripadvisor.fr/{l['href']}"
    #     links.append(url_page)

    #     new_soup = get_page_contents(url_page)    
    #     adress.append(new_soup.find('span',{'class':'fHvkI PTrfg'}).text)
    #     # print(f"Adress hotel : {i} : OK")
    #     i += 1

    # Create the dictionary.
    # dict = {'Hotel Names':hotels,'Ratings':ratings,'Number of Reviews':reviews,'Prices':prices, "Adress" : adress , "links": links}
    dict = {'Hotel Names':hotels,'Ratings':ratings,'Number of Reviews':reviews,'Prices':prices}

    # Create the dataframe.
    hotel_list = pd.DataFrame.from_dict(dict)
    return hotel_list
    # hotel_list.head(10)

    pass



# Create your views here.
def tripadvisor(request):
        df = tripadvisor_scraper()
        context = {"df": df.to_html}
        return render(request, 'tripadvisor/tripadvisorScraper.html', context=context)
