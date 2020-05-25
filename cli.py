import json
import requests
import time
from notify_run import Notify
import logging
import datetime
import sys
import html
import click

logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

logger = logging.getLogger(__name__)
notify = Notify() # this needs to be setup outside of this script
wait_time_s = 60
url = "https://www.cafebesalu.com/app/store/api/v8/editor/users/125614995/sites/725420366501505624/store-locations/11e97377b326f4d1a5ad0cc47a2b63e4/products?page=1&per_page=200&has_categories=1"
# Default items to track
watched_names = ['Ham & Swiss Pastry', 'Fruit Danish', 'Pain au Chocolat', 'Onion & Gruyere', 'Almond Croissant']
notify_threshold = 0.5

@click.group()
def cli():
    pass

@cli.command()
def list_items():
    response = requests.get(url)
    data = response.json()['data']
    for item in data:
        short_desc = item['short_description'] or ''
        print(f"{item['name']}: {item['inventory']['total']}, {html.unescape(short_desc)}")

@cli.command()
def watch():
    while True:
        do_check()
        time.sleep(wait_time_s)

# latch for only sending push notification when becomes true
last_success = False
def do_check():
    global last_success
    response = requests.get(url)
    data = response.json()['data']
    item_counts = {item['name']: item['inventory']['total'] for item in data}
    watched_item_counts = {key: value for key, value in item_counts.items() if key in watched_names}
    available_items = {key: value for key, value in watched_item_counts.items() if value > 0}
    available_ratio = len(available_items) / len(watched_names)
    if available_ratio > notify_threshold:
        logger.info("Success! " + json.dumps(watched_item_counts))
        if not last_success:
            notify.send('Time to order besalu! ' + json.dumps(watched_item_counts))
        last_success = True
    else:
        logger.info("No dice. " + json.dumps(watched_item_counts))
        last_success = False

if __name__ == '__main__':
    cli()