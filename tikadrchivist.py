#!/usr/bin/env python

import argparse
import requests
import json
import datetime
import os
import shutil
import urllib.parse

from tqdm import tqdm

# Set default values for variables
defaults = {
	"query": "",
	"query_type": "",
	"adv_biz_ids": "",
	"order": "impression,desc",
	"offset": 0,
	"search_id": "",
	"limit": 100,
	"region": "BE",
	"start_time": 1664575200,
	"end_time": 1689863218,
	"output": "json"
}

# Create the top-level parser
parser = argparse.ArgumentParser(description="A command-line tool to search TikTok Ads Library.")
parser.add_argument("--query", default=defaults["query"])
parser.add_argument("--query_type", default=defaults["query_type"])
parser.add_argument("--adv_biz_ids", default=defaults["adv_biz_ids"])
parser.add_argument("--order", default=defaults["order"])
parser.add_argument("--offset", type=int, default=defaults["offset"])
parser.add_argument("--search_id", default=defaults["search_id"])
parser.add_argument("--limit", type=int, default=defaults["limit"])
parser.add_argument("--region", default=defaults["region"])
parser.add_argument("--start_time", type=int, default=defaults["start_time"])
parser.add_argument("--end_time", type=int, default=defaults["end_time"])
parser.add_argument("--output", default=defaults["output"])
args = parser.parse_args()

# Define the data payload
data = {
	"query": args.query,
	"query_type": args.query_type,
	"adv_biz_ids": args.adv_biz_ids,
	"order": args.order,
	"offset": args.offset,
	"search_id": args.search_id,
	"limit": args.limit
}

# Get the current date and time
datetime_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Define the output file
output_file = f"{args.region}_{args.query}_{args.search_id}_{datetime_now}.json"

# Inform user about the download process
print("[+] Downloading JSON files...")

# Perform the request and write the response to the output file
headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
	"Accept": "application/json, text/plain, */*",
	"Content-Type": "application/json"
}

response = requests.post(
	f"https://library.tiktok.com/api/v1/search?region={args.region}&type=1&start_time={args.start_time}&end_time={args.end_time}",
	headers=headers,
	data=json.dumps(data)
)
if response.status_code != 200:
	print(f"[x] Exiting, response with status: {response.status_code}")
	exit()
json_data = response.json()

if args.output == "json":
	with open(output_file, "w") as f:
		json.dump(json_data, f)
	print(f"[+] JSON file is available : {output_file}")
elif args.output == "total_value":
	total_value = 0
	for item in json_data["data"]:
		try:
			total_value += int(item["spent"])
		except KeyError:
			pass
	print(f"[+] The total value of \"spent\" is: {total_value}")
elif args.output == "total_impression":
	total_impression = 0
	for item in json_data["data"]:
		try:
			total_impression += int(item["impression"])
		except KeyError:
			pass
	print(f"The total value of 'impression' is: {total_impression}")
elif args.output == "dl_videos":
	# Create directory for videos
	video_dir = os.path.join(os.getcwd(), "videos")
	os.makedirs(video_dir, exist_ok=True)
	
	# Download videos
	with tqdm(total=len(json_data["data"]), desc="Downloading video of the ads") as pbar:
		for ad in json_data["data"]:
			if "videos" in ad:
				for i, video in enumerate(ad["videos"], 1):
					url = video["video_url"]
					res = requests.get(url, stream=True)
					res.raise_for_status()

					# Get the original file name from the URL
					url_parsed = urllib.parse.urlparse(url)
					paths = url_parsed.path.split("/")

					# If the video filename is empty, get the first value after the "/"
					if paths:
						video_filename = paths[1] + ".mp4"

					# If the video filename is not empty, write the video to a file
					if video_filename:
						video_file = os.path.join(video_dir, video_filename)
						with open(video_file, "wb") as f:
							shutil.copyfileobj(res.raw, f)
					else:
						print(f"[x] No filename found in URL: {url}")
			pbar.update()
	print(f"[+] Videos downloaded to directory : {video_dir}")
