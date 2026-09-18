# Medium Article Scraper

A small Python tool for Machine Learning I (Task 1). Given the URL of a Medium article, it downloads the page, pulls out the paragraph text, and saves it to a `.txt` file.

Example article used for this task:
https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

## Files

| Path | Description |
| --- | --- |
| `Task1_Python_script.py` | The scraper as a command-line script |
| `Task 1.ipynb` | The same code as a Jupyter notebook, one cell per function |
| `scraped_articles/` | Output folder, created automatically on the first run |

## Requirements

- Python 3
- [`requests`](https://pypi.org/project/requests/)
- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)
- [`cloudscraper`](https://pypi.org/project/cloudscraper/) (optional, see [Notes](#notes))

```bash
pip install requests beautifulsoup4 cloudscraper
```

## Usage

### Script

```bash
python Task1_Python_script.py
```

Paste the article URL when prompted:

```
Enter url of a medium article: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
```

### Notebook

Open `Task 1.ipynb`, then run the cells from top to bottom. The last cell asks for the URL, the same as the script does.

## Output

The text is saved to `scraped_articles/<article-slug>.txt`, where the slug is the last part of the URL. For the example above:

```
scraped_articles/papa-what-is-a-neural-network-c5e5cc427c7.txt
```

The file starts with a `url:` line, followed by each paragraph of the article separated by a blank line.

## How it works

1. `get_page()` asks for the URL, checks it, downloads the page and parses it with BeautifulSoup.
2. `collect_text()` gathers the text of every `<p>` tag into one string.
3. `save_file()` writes that string to `scraped_articles/`.

`clean()` strips leftover HTML tags from a string. It is defined but the main flow does not call it, because BeautifulSoup's `.text` already returns plain text.

## Notes

- **URL check:** only URLs that start with `http://medium.com/` or `https://medium.com/` are accepted. Anything else prints an error and exits. Publication subdomains such as `something.medium.com` are rejected.
- **Cloudflare:** Medium can answer plain `requests` calls with a 403. If `cloudscraper` is installed the script uses it, since it can get past that check. Without it, the script falls back to a normal `requests` call, which may fail.
