#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import requests
import unidecode
import json
import time  # Added for simulating progress

# Terminal colors
if os.environ.get('LS_COLORS') is not None:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    TEAL = '\033[96m'
    DEFAULT = '\033[0m'
else:
    RED = GREEN = YELLOW = BLUE = PURPLE = TEAL = DEFAULT = ''

OBJECT_TYPES = {'v': 'video', 'l': 'live', 'p': 'photos', 'c': 'channel'}

def get_repr(item):
    return '%s %s "%s%s"' % (
        OBJECT_TYPES[item['oid'][0]],
        item['oid'],
        item['title'][:40],
        ('...' if len(item['title']) > 40 else '')
    )

def get_prefix(item):
    return unidecode.unidecode(item['title'][:57].strip()).replace('/', '|') + ' - ' + item['oid']

def get_download_link(msc, item):
    """Retrieve download link and filename for the best quality resource."""
    if item['oid'][0] != 'v':  # Only process videos
        return None
    resources = msc.api('medias/resources-list/', params=dict(oid=item['oid']))['resources']
    resources.sort(key=lambda a: -a['file_size'])
    if not resources:
        return None
    
    best_quality = next((r for r in resources if r['format'] != 'm3u8'), None)
    if not best_quality:
        return None

    url_resource = msc.api(
        'download/',
        method='get',
        params=dict(oid=item['oid'], url=best_quality['file'], redirect='no')
    )['url']
    
    # Return filename and download link as a dictionary
    return {
        "filename": item['title'],
        "download_link": url_resource
    }

def process_channel(msc, channel_info, download_links):
    """Recursively retrieve download links for all videos in a channel and subchannels."""
    print(f'{BLUE}Processing channel: {channel_info["oid"]} - {channel_info["title"]}{DEFAULT}')
    channel_items = msc.api(
        'channels/content/',
        method='get',
        params=dict(parent_oid=channel_info['oid'], content='cvp')
    )

    for entry in channel_items.get('channels', []):
        process_channel(msc, entry, download_links)

    items = channel_items.get('videos', []) + channel_items.get('photos_groups', [])
    for index, entry in enumerate(items, start=1):
        try:
            print(f'{YELLOW}Processing item {index}/{len(items)}: {get_repr(entry)}{DEFAULT}')
            link_info = get_download_link(msc, entry)
            if link_info:
                download_links.append(link_info)  # Append filename and link as object
            time.sleep(0.5)  # Simulate processing time for feedback
        except Exception as e:
            print(f'{RED}Error retrieving link: {e}{DEFAULT}')

def output_download_links(msc, channel_oid):
    print('Starting to gather download links...')
    download_links = []

    try:
        channel_parent = msc.api('channels/get/', method='get', params=dict(oid=channel_oid))
    except Exception as e:
        print(f'Please enter a valid channel oid or check access permissions. Error: {e}')
        return 1

    process_channel(msc, channel_parent['info'], download_links)

    # Save to JSON file
    file_path = os.path.join(os.getcwd(), "download.json")
    with open(file_path, 'w') as f:
        json.dump(download_links, f, indent=2)
    
    print(f'{GREEN}Download links gathered successfully and saved to {file_path}.{DEFAULT}')
    return 0

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ms_client.client import MediaServerClient

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--conf',
        dest='configuration',
        help='Path to the configuration file.',
        required=True,
        type=str
    )

    parser.add_argument(
        '--channel',
        dest='channel_oid',
        help='Channel oid to check.',
        required=True,
        type=str
    )

    args = parser.parse_args()

    if not args.configuration.startswith('unix:') and not os.path.exists(args.configuration):
        print('Invalid path for configuration file.')
        sys.exit(1)

    msc = MediaServerClient(args.configuration)
    msc.check_server()
    msc.conf['TIMEOUT'] = max(120, msc.conf['TIMEOUT'])

    rc = output_download_links(msc, args.channel_oid)
    sys.exit(rc)
