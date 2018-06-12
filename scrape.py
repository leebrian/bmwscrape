#!/usr/local/bin/python

"""
Another mess-around project to learn more pythonTM
I'm thinking about buying or leasing a bmw over the course of the next 12 months, so I want to track things over time on a few models of interest to me:
Money Factor from BMWFinancial
Resididual
Credits
Suggested dealer contribution
Monthly payment

Whenever I talk to the local dealers, they say this never changes. But it's hard to find historical data. So to take a page from the movie Primer, I'll start tracking history and hopefully will be useful around this time next year.

Resources:
config_scrape.json has pages from bmwusa.com that seem to follow a standard pattern of something like this showing up in the html:
"Offer not valid in Puerto Rico. Lease financing available on new 2018 BMW 330i xDrive Gran Turismo models from participating BMW Centers through BMW Financial Services through July 02, 2018, to eligible, qualified customers with excellent credit history who meet BMW Financial Services' credit requirements. Monthly lease payments of $549 per month for 36 months is based on an adjusted capitalized cost of $44,319 (MSRP of $47,445, including destination and handling fee of $995, less $3,000 customer down, $0 security deposit and suggested dealer contribution of $126). Actual MSRP may vary. Dealer contribution may vary and could affect your actual lease payment. Cash due at signing includes $3,000 down payment, $549 first month's payment, $925 acquisition fee and $0 security deposit. Lessee responsible for insurance during the lease term, excess wear and tear as defined in the lease contract, $0.25/mile over 30,000 miles and a disposition fee of $350 at lease end. Not all customers will qualify for security deposit waiver. Tax, title, license and registration fees are additional fees due at signing. Advertised payment does not include applicable taxes. Purchase option at lease end, excluding tax, title and government fees, is $28,941. Offer valid through July 02, 2018 and may be combined with other offers unless otherwise stated. Models pictured may be shown with metallic paint and/or additional accessories. Visit your authorized BMW Center for important details. ©2018 BMW of North America, LLC. The BMW name, model names and logo are registered trademarks. "
The json format should be:
{
    "url":
        "https://www.bmwusa.com/special-offers/lease.2018-320i-Sedan.bmw.html?modal=special-offers-legal", -- url that matches a pattern understood by a handler
    "added": "2018-06-11", -- whenever this config was added
    "active": false, -- will only be processed if true, else skipped
    "handler": "bmw-usa-330i", -- corresponds to a handerl function that knows how to process the html
    "car_check": "2018 BMW 330i" -- processes for a particular model
}

TODO implement scraping
TODO implement logging
TODO update google sheet if different
"""

import requests
import json
import datetime

CONFIG_FILE_NAME = 'config_scrape.json'
HANDLERS = {'bmw-usa': 'process_bmw_usa',
            'bmw-usa-330i': 'process_330i'}


def process_bmw_usa(html, car):
    # scrapes out the relevant info for 330iGT

    EXPIRE_MATCH_STRING = 'Offer valid through '

    scrape_results = {}

    print('in processing, looking for ' + car + ' in: ' + html[:100])
    number_car_in_html = html.count(car)  # should be 3 based on their site
    print(':' + str(number_car_in_html) + ': matches')

    if (number_car_in_html == 3):

        # figure out the expiration date
        position_expire = html.find(EXPIRE_MATCH_STRING)

        expiration_string = html[position_expire +
                                 len(EXPIRE_MATCH_STRING):13+position_expire+len(EXPIRE_MATCH_STRING)]
        print(expiration_string)
        dtExpiration = datetime.datetime.strptime(
            expiration_string, '%B %d, %Y')
        scrape_results["expires"] = dtExpiration.strftime("%Y-%m-%d")

        # figure out the destination fee
        # figure out the MSRP
        # figure out the adjusted capitalized cost (ACC)
        # figure out the residual value
        # figure out the term in months
        # figure out the monthly payment
        # figure out the total miles
        # figure out the disposition fee
        # figure out the credit
        # figure out the suggested dealer contribution
        # figure out the down payment
        # figure out the security deposit

    else:
        print("not three matches, skipping processing")
        raise ValueError(
            'there should be 3 matches in the bmw page for car <' + car + '>, but there are only <' + str(number_car_in_html) + '>, look at your processor, maybe they updated their layout')

    return scrape_results


def process_330i(html):
    # not implemented yet
    raise NotImplementedError('this function isn''t implemented yet')


with open(CONFIG_FILE_NAME, 'r') as file:
    offerPages = json.load(file)


for page in offerPages["bmw_offer"]:
    # print(page)
    if page['active']:
        print('is active with handler:' + page['handler'])
        if page['handler'] in HANDLERS:
            print('I''m in ' + HANDLERS[page['handler']])
            response = requests.get(
                'https://www.bmwusa.com/special-offers/lease.2018-330i-xDrive-Gran-Turismo.bmwatl.html?modal=special-offers-legal')
            response.encoding = "UTF-8"
            print('result for car<' + page['car_check'] + '>: ' + str(globals()[HANDLERS[page['handler']]](
                response.text, page['car_check'])))
        else:
            print("I don't know that handler")
