# Website-Extractor
A python script, [extract.py](https://github.com/danicychao/Website-Extractor/blob/main/extract.py), to extract logo and phone numbers given a website url.

## How to use
```python extract.py <url>```

## Required libraries
[requests](https://requests.readthedocs.io/en/latest/), [bs4 (beautifulsoup4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers).

### To install requests:
```pip install requests```

### To install bs4:
```pip install bs4```

Installing bs4 is a bit tricky. If you use anaconda, you probably already have a library/package called bs4, and nothing will execute by running **pip install beautifulsoup4**. Just **import bs4**, and run with **bs4.BeautifulSoup**.

### To install phonenumbers:
```pip install phonenumbers```



