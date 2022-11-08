# Scraping from eBay

For [project_03](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03), I created a python script that scrapes eBay product listings for information like prices and # of items sold. It then saves this data into a `.json` or `.csv` file.

Within this repository, `ebay-dl.py` conducts this entire process. It uses `argparse`, `requests`, and `bs4` libraries for command line and data scraping purposes, along with the `json` and `csv` libraries to create the `.json` and `.csv` files. Each file denotes the `name` of the item listed; its `price`; whether it is pre-owned, refurbished, or new (`status`); `shipping` cost; whether or not it has `free_returns`; and the number of `items_sold`.

There are several ways to run `ebay-dl.py`. It allows you to search for items that are one word or more, specify the number of eBay pages to scrape from, and download the data in `.json` format by default or `.csv`, if you specify.

### Tutorial
Here is a template command line to run the python file:
```
$ python3 ebay-dl.py 'insert query here'
```

If you prefer fewer pages than 10, you can specify in this way (here, any number can substitute for `7`):
```
$ python3 ebay-dl.py 'insert query here' --num_pages=7
```


If you prefer the file in `.csv` format (you do not to need `--num_pages` before `--csv`):
```
$ python3 ebay-dl.py 'insert query here' --num_pages=7 --csv
```

### Retrieve my queries
To retrieve the same queries as I did ('family guy', 'jane jacobs', and 'ishiguro'), you can enter these lines:
```
$ python3 ebay-dl.py 'family guy'
```
```
$ python3 ebay-dl.py 'jane jacobs'
```
```
$ python3 ebay-dl.py 'ishiguro'
```

And, of course, to save these as a `.csv`, for example:
```
$ python3 ebay-dl.py 'ishiguro' --csv
```