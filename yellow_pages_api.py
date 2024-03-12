from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import time
import random
import constants

def get_page(location, search_terms, page_num=1):
  '''get a page from Yellow Pages given a search term and location
  return:
      page (bs): beautiful soup object for parsing
  '''
  # TODO: Clean this up
  # TODO: let users start in a different page
  search_URL = constants.URL + constants.TERMS + search_terms + '&' + constants.LOCATION + location + '&page=' + str(page_num)
  res = requests.get(search_URL)
  # print(search_URL)

  if res.status_code != 200:
      print(str(res.status_code) + ' failed to get data from yellow pages from ' + search_URL)
      return

  else:
      page = BeautifulSoup(res.content, 'html.parser') #.find_all("div", {"class:" : "result"})
      page_num += 1
      return [page, page_num]

def get_results(page):
  '''turn a page BS object into a list of results from the page
  return:
      resutls [bs]: list of BS tags that correspond to each result on a page
  '''
  results = page.find_all("div", class_="result")
  return results


def get_restaurant_name(result):
  '''gets the restaurant name from a BS object
  return:
      name (str): name of the restaurant
  '''
  name = result.find("a", class_="business-name").get_text()

  return name

def get_restaurant_address(result):
  '''gets the restaurant address from a BS object
  return:
      address (str): address of the restaurant
  '''

  # Some restaurants don't have addresses??? DOG WTF IS THAT!?
  street_address = ""
  if result.find("div", class_="street-address") is not None:
    street_address = result.find("div", class_="street-address").get_text()
  locality = result.find("div", class_="locality").get_text()
  address = street_address + ", " + locality

  return address

def get_restaurant_yp_rating(result):
  '''gets the restaurant Yellow Pages rating from a BS object
  return:
      rating (float): Yellow Pages rating of the restaurant
  '''
  rating = -1.0
  partial_rating = 0.0
  result_rating_str = str(result.find("div", class_="ratings"))
  yp_rating_ls = re.findall('result-rating (\w*(?: half)?)', result_rating_str)

  if len(yp_rating_ls) > 0:
      yp_rating_str = yp_rating_ls[0]
      if 'half' in yp_rating_str:
          yp_rating_str = yp_rating_str.replace(' half', '')
          partial_rating = 0.5
      rating = constants.RATINGS_KEY.index(yp_rating_str) + partial_rating

  return rating

def get_restaurant_ta_rating(result):
  '''gets the restaurant Trip Advisor rating from a BS object
  return:
      rating (float): Trip Advisor rating of the restaurant
  '''
  rating = -1.0
  ta_rating_str = result.find("div", class_="ratings").get("data-tripadvisor")
  if ta_rating_str is not None:
      rating_obj = json.loads(ta_rating_str)
      rating = float(rating_obj['rating'])

  return rating

def get_restaurant_categories(result):
  '''gets the restaurant categories from a BS object
  return:
      categories [str]: categories of the restaurant
  '''
  categories = []
  categories_str = result.find("div", class_="categories").find_all("a")
  for j, cat in enumerate(categories_str):
      if j == 0:
          continue
      categories.append(cat.getText())
  return categories

def load_restaurants(restaurant_csv):
  '''loads a csv into dataframe for manipulation
  return:
      restaurant_df (DataFrame): pandas object containing restaurant data
  '''
  restaurant_df = pd.read_csv(restaurant_csv)
  return restaurant_df

def save_restaurants(restaurant_df):
  '''saves restaurant dataframe to CSV
  side effects:
      saves 'restaurants_df.csv' to current directory. WILL OVERWRITE IF ALREADY EXIST
  '''
  restaurant_df.to_csv("restaurants_df.csv", index=False)
  # TODO: add backup functionality

def bot_wait():
  '''waits a random amount of time so YP doesn't catch on to this being a bot
  side effects:
      stops program for waiting for a bit
  '''
  time.sleep(random.randint(5, 30))