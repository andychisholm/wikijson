import wikicorpus

PAGE_DELIMITER = "\n  </page>\n"
PAGE_START = '<page>\n'
PAGE_END = '</page>'

# extract page element data from a wikipedia dump
def get_pages_from_wikidump(sc, path):
    # dodgy yet effective text delimiter to split xml elements for the input rdd
    wikidump = sc.newAPIHadoopFile(
        path,
        "org.apache.hadoop.mapreduce.lib.input.TextInputFormat",
        "org.apache.hadoop.io.LongWritable",
        "org.apache.hadoop.io.Text",
        conf = { "textinputformat.record.delimiter": PAGE_DELIMITER })

    return wikidump\
        .map(lambda (_, part): (part.find(PAGE_START), part))\
        .filter(lambda (offset, _): offset >= 0)\
        .map(lambda (offset, content): content[offset:]+PAGE_END)\
        .map(wikicorpus.extract_page)

# extract redirects from wiki pages
def get_redirects_from_pages(pages):
    pfx = wikicorpus.wikilink_prefix
    return pages.filter(lambda info: info[3] != None)\
                .map(lambda info: (info[0], info[3]))\
                .mapValues(wikicorpus.normalise_wikilink)\
                .map(lambda (s, t): (pfx+s, pfx+t))

# extract article plaintext and links from wiki pages
def get_articles_from_pages(pages):
    return pages.filter(lambda info: info[1] == '0' and info[3] == None and info[4])\
                .map(lambda info: (info[0], info[4]))\
                .mapValues(wikicorpus.remove_markup)\
                .mapValues(wikicorpus.extract_links)

# maps links to their ultimate destination for a redirect set
def redirect_article_links(articles, redirects):
    return articles\
        .flatMap(lambda (pid, (text, links)): ((t, (pid, span)) for t, span in links))\
        .leftOuterJoin(redirects)\
        .map(lambda (t, ((pid, span), r )): (pid, (r if r else t, span)))\
        .groupByKey()\
        .mapValues(list)\
        .join(articles)\
        .map(lambda (pid, ( links, (text, _) )): (pid, (text, links)))
