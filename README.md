wikijson - Wikipedia to JSON
============================

Convert wikipedia dumps into a simple json representation without all the cruft.

### Getting Started

Detailed documentation is available via: [wikijson.readthedocs.org](http://wikijson.readthedocs.org/en/latest/).

## Usage

```bash
# download the latest wikipedia dump (~12GB)
wget http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# extract articles from wiki markup into a compressed file with one json encoded article per line (~6GB)
wikijson process-dump enwiki-latest-pages-articles.xml.bz2 wikipedia.js.gz
```

## Processing Output

```python
import json
import gzip
with gzip.open('wikipedia.js.gz', 'r') as f:
    for line in f:
        article = json.loads(line)
```

## Article Schema

```javascript
{
    "id": number,
    "title": string,
    "text": string,
    "categories": [string],
    "links": [{
        "target": string,
        "start": number,
        "stop": number
    }]
}
```

### Credits

This project is based on the Wiki processing [script](https://github.com/attardi/wikiextractor) by Giuseppe Attardi and inherits its GPL licence.
