# Yellow Pages API

This tool is meant to allow users to scrape Yellow Pages for a given city and search term.

The API scrapes any number of pages the user specifies and outputs them to a csv for later use

## How to use

From you preferred CLI execute the following:

```bash
$ python main.py
```

When prompted tell how many pages you want to scrape

```bash
how many pages do you want to get? 5
1/5
```

The program will iterate until it reaches the last page then print the shape of the array for confirmation

The program will prouce a CSV file called `restaurants_df.csv` for later use

## CSV feature

The CSV is produced with the following header:
   * `name`
   * `address`
   * `yp_ratings`
   * `ta_ratings`
   * `categories`
   * `geocode` *(coming soon)*