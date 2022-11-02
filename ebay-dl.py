import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_prices(text):
    prices = ''
    if 'see price' in text.lower():
        return None
    else:
        for char in text:
            if char in '1234567890':
                prices += char
        return int(prices)

def parse_statuses(text):
    statuses = ''
    for char in text:
        if char == '·':
            return statuses
        else:
            statuses += char
    return statuses

def parse_shippings(text):
    shippings = ''
    if 'free' in text.lower():
        shipping = 0
        return shipping
    else:
        for char in text:
            if char in '1234567890':
                shippings += char
        return int(shippings)

# this if statement says only run the code below when the python file is run "normally"
# where normally means not in the doctests
if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action = 'store_true')
    args = parser.parse_args()
    print('args.search_terms=', args.search_term)

    # download specified # of pages of specified search term
    items = []
    for page_number in range(1, int(args.num_pages)+1):
        # build the url
        '''
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term
        url += '&_sacat=0&LH_TitleDesc=0&_pgn='
        url += str(page_number)
        '''
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='+ args.search_term +'&_sacat=0&LH_TitleDesc=0&_pgn='+ str(page_number)
        print('url=', url)

        # download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html =  r.text

        # process the html
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            price = None
            tags_prices = tag_item.select('.s-item__price')
            for tag in tags_prices:
                price = parse_prices(tag.text)

            status = None
            tags_statuses = tag_item.select('.SECONDARY_INFO')
            for tag in tags_statuses:
                status = parse_statuses(tag.text)

            shipping = None
            tags_shippings = tag_item.select('.s-item__shipping, .s-item__freeXDays')
            for tag in tags_shippings:
                shipping = parse_shippings(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)
        
        print('len(tags_items)=', len(tags_items))
        print('len(items)=', len(items))



    if args.csv == True:
        # write the CSV to a file
        field_names = list(items[0].keys())
        filename = args.search_term+'.csv'
        with open(filename, 'w', encoding='utf-8') as f:
            w = csv.DictWriter(f, field_names)
            w.writeheader()
            w.writerows(items)
    else:
        # write the JSON to a file
        filename = args.search_term+'.json'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(items))
