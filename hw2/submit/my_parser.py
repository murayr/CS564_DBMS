
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
I was having trouble with the quotes resulting in dropped users so I had to make a clean function
"""
def clean_string(s):
    if s is None:
        return "NULL"
    s = s.replace('"', ' ').replace('|', ' ')
    s = s.replace('\n', ' ').replace('\r', ' ')
    s = ' '.join(s.split())
    return s


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    # Kept dropping users who had both placed bids and sold items so had to use hasattr()
    if not hasattr(parseJson, "seen_users"):
        parseJson.seen_users = set()

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']

    # Fixed: Open all output files once
    with open('users.dat', 'a', encoding='utf-8') as users_file, \
         open('items.dat', 'a', encoding='utf-8') as items_file, \
         open('categories.dat', 'a', encoding='utf-8') as categories_file, \
         open('bids.dat', 'a', encoding='utf-8') as bids_file:

        for item in items:
            # Process seller
            seller = item['Seller']
            seller_id = clean_string(seller['UserID'])
            location = clean_string(item['Location'])
            country = clean_string(item['Country'])

            # Add seller to users.dat if not seen before
            if seller_id not in parseJson.seen_users:
                parseJson.seen_users.add(seller_id)
                users_file.write(f"{seller_id}|{seller['Rating']}|{location}|{country}\n")

            # Process item
            item_id = item['ItemID']
            name = clean_string(item['Name'])
            currently = transformDollar(item['Currently'])
            buy_price = transformDollar(item.get('Buy_Price', 'NULL'))
            first_bid = transformDollar(item['First_Bid'])
            number_bids = item['Number_of_Bids']
            started = transformDttm(item['Started'])
            ends = transformDttm(item['Ends'])
            description = clean_string(item.get('Description', ''))

            items_file.write(f"{item_id}|{name}|{currently}|{buy_price}|{first_bid}|"
                             f"{number_bids}|{location}|{country}|{started}|{ends}|"
                             f"{seller_id}|{description}\n")

            # Process categories
            for category in set(item['Category']):
                categories_file.write(f"{item_id}|{clean_string(category)}\n")

            # Process bids
            if item['Bids']:
                for bid in item['Bids']:
                    bid_data = bid['Bid']
                    bidder = bid_data['Bidder']
                    bidder_id = clean_string(bidder['UserID'])

                    # Add bidder to users.dat if not seen before
                    if bidder_id not in parseJson.seen_users:
                        parseJson.seen_users.add(bidder_id)
                        bidder_location = clean_string(bidder.get('Location', 'NULL'))
                        bidder_country = clean_string(bidder.get('Country', 'NULL'))
                        users_file.write(f"{bidder_id}|{bidder['Rating']}|{bidder_location}|{bidder_country}\n")

                    bid_time = transformDttm(bid_data['Time'])
                    bid_amount = transformDollar(bid_data['Amount'])
                    bids_file.write(f"{item_id}|{bidder_id}|{bid_time}|{bid_amount}\n")


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
