# WebCrawler
## Overview

This crawler scrapes job postings from Workday-powered career sites. Job
descriptions are saved under a directory named after each posting ID and include
labels extracted from the listing such as title, location and posted date.

Once all posting URLs are collected, the crawler fetches each job description in
parallel (see options below). It has been successfully tested with several
Workday sites.

## Contents

- `crawler.py` – main logic for scraping job postings
- `util.py` – helper functions used by the crawler

## Usage

```
python3 crawler.py [options]
```

### Examples

- `python3 crawler.py -u "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers" -d "./mastercard"`
  - retrieves all Mastercard postings and stores them under `mastercard`
- `python3 crawler.py -u "https://symantec.wd1.myworkdayjobs.com/careers" -d "./symantec"`
  - retrieve all Symantec postings
- `python3 crawler.py -u "https://pvh.wd1.myworkdayjobs.com/PVH_Careers" -d "./pvh" -t 8 --verbose`
  - retrieve all PVH postings using 8 threads with verbose output

### Options

- `-h, --help` – show help message
- `-u MAIN_LINK, --url MAIN_LINK` – Job Posting URL (default:
  `https://mastercard.wd1.myworkdayjobs.com/CorporateCareers`)
- `-d DEST_DIR, --dest DEST_DIR` – Destination directory (default: `./test`)
- `-t THREAD_COUNT, --threads THREAD_COUNT` – Number of parallel threads (default: `4`)
- `-v, --verbose` – Verbose output to stdout

## License

This project is licensed under the [MIT License](LICENSE).
