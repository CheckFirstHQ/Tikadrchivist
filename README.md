# TikTok Ads Library Search Tool

![Tikadrchivist](https://checkfirst.network/wp-content/uploads/2023/07/repo_card.png) 

This command-line tool is designed to search through TikTok's Ads Library, allowing you to specify a variety of search parameters such as query, region, order, and more. This tool was developed by [CheckFirst](https://checkfirst.network/) and is Open Source.

## Installation

Before running the script, ensure you have Python 3.x installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/). 

This script requires third party Python libraries listed in the file `requirements.txt`. If you don't have them installed, you can do so by using pip:

```bash
pip install -r requirements.txt
```

Note: the command reported above may differ based on your setup.

## Usage

After you cloned this repository and installed the dependencies, all you have to do is just running the Python script with the CLI arguments of your interest. 

### Example

```bash
python tikadrchivist.py --query "your search query" --region "your region"
```

## Parameters

Here follows the list of all the options you can use:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `--query` | String | Search query string (eg : `"funny"`) | ` ` |
| `--query_type` | String | The type of query (not used) | ` ` |
| `--adv_biz_ids` | Array | Search by ID(s) of advertiser business(es) | ` ` |
| `--order` | String | The order in which to return results (can be `impression,asc`, `impression,desc`, `last_shown_date,asc`, `last_shown_date,desc`, `create_time,asc` or `create_time,desc`) | `"impression,desc"` |
| `--offset` | Integer | The number of results to offset (for pagination) | `0` |
| `--search_id` | String | The ID of the search (not used) | ` ` |
| `--limit` | Integer | The maximum number of results to return | `100` |
| `--region` | String | The EU country to search in (or `all` for all countries) | `BE` |
| `--start_time` | Integer | The start time for the search period (in Unix timestamp format) | `1664575200` |
| `--end_time` | Integer | The end time for the search period (in Unix timestamp format) | `1689863218` |
| `--output` | String | The output format (can be `json`, `total_value`, `total_impression`, or `dl_videos`) | `json` |

The script will download a JSON file with the results of your search. The filename will contain your search parameters and the current date-time.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)