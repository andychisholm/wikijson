wikijson - Wikipedia to JSON
============================

Convert wikipedia dumps into a simple json representation without all the cruft.

<!---Detailed documentation is available via: [wikijson.readthedocs.org](http://wikijson.readthedocs.org/en/latest/).-->

## Quick Start

### Install
```bash
virtualenv ve
. ve/bin/activate
pip install git+http://git@github.com/wikilinks/wikijson.git
```

### Process Wikipedia
```bash
# download the latest partitioned wikipedia dump
# see available dumps: http://dumps.wikimedia.org/enwiki/
wkdl latest

# process the dump under 'latest', store the result under 'latest_js'
wkjs process-dump latest_raw latest_js
```

## Spark

__wikijson__ uses Spark to process the Wikipedia dump in parallel.

If you'd like to make use of an existing Spark cluster, ensure the `SPARK_HOME` environment variable is set.

If not, `wkjs` will prompt you to download and run Spark locally in standalone mode.

## Performance

On a cluster of 4 machines with 64 worker cores, it takes around 15 minutes to process a complete Wikipedia dump and map article links via redirects.

## Output Schema

```javascript
{
    "title": string,
    "text": string,
    "links": [{
        "target": string,
        "start": number,
        "stop": number
    }]
}
```
