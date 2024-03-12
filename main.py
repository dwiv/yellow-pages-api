import constants
import pandas as pd
import yellow_pages_api as yp

def main():
  # TODO: add an input for search type
  location = "Baltimore-MD"
  search_terms = "restaurant"

  page_num = 1
  pages = int(input("how many pages do you want to get? "))
  restaurants_df = pd.DataFrame(columns=constants.HEADERS)

  # TODO: Load data first so that overwrite doesn't get rid of old data when used

  while page_num <= pages:
    print(f"\r{page_num}/{pages}", end="")
    
    page, page_num = yp.get_page(location, search_terms, page_num)
    results = yp.get_results(page)

    for result in results:
      name = yp.get_restaurant_name(result)
      address = yp.get_restaurant_address(result)
      yp_rating = yp.get_restaurant_yp_rating(result)
      ta_rating = yp.get_restaurant_ta_rating(result)
      categories = yp.get_restaurant_categories(result)
      restaurant = {"name": name, "address": address, "yp_rating": yp_rating, "ta_rating": ta_rating, "categories": categories}

      restaurant_df = pd.DataFrame([restaurant], columns=constants.HEADERS)
      restaurants_df = pd.concat([restaurants_df, restaurant_df], ignore_index=True)
    yp.save_restaurants(restaurants_df)
    yp.bot_wait()
  print(restaurants_df.shape)
  # print(test_df)    

if __name__ == "__main__":
    main()