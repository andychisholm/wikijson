import os
import shutil
import ujson as json
import wikispark

from pyspark import SparkContext, SparkConf

import logging
log = logging.getLogger()

class ProcessDump(object):
    """ Extra a simple json representation for each article in a wikipedia dump """
    def __init__(self, wk_dump_path, output_path, redirect_links):
        self.wk_dump_path = wk_dump_path
        self.output_path = output_path
        self.redirect_links = redirect_links

    def __call__(self):
        log.info('Processing wiki dump: %s ...', self.wk_dump_path)
        c = SparkConf().setAppName('Wikijson')

        log.info('Using spark master: %s', c.get('spark.master'))
        sc = SparkContext(conf=c)

        if os.path.isdir(self.output_path):
            log.warn('Writing over output path: %s', self.output_path)
            shutil.rmtree(self.output_path)

        # rdd of tuples: (title, namespace, id, redirect, content)
        pages = wikispark.get_pages_from_wikidump(sc, self.wk_dump_path)
        pages.cache()

        articles = wikispark.get_articles_from_pages(pages)
        redirects = wikispark.get_redirects_from_pages(pages)

        if self.redirect_links:
            articles = wikispark.redirect_article_links(articles, redirects)

        articles.map(self.article_to_json)\
                .map(json.dumps)\
                .saveAsTextFile(self.output_path, 'org.apache.hadoop.io.compress.GzipCodec')

        log.info('Done.')

    @staticmethod
    def article_to_json(article):
        title, (text, links) = article
        return {
            'title': title,
            'text': text,
            'links': [{
                'target': target,
                'start': span.start,
                'stop': span.stop
            } for target, span in links]
        }

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('wk_dump_path', metavar='WK_DUMP_PATH')
        p.add_argument('output_path', metavar='OUTPUT_PATH')
        p.add_argument('--no-redirect', dest='redirect_links', action='store_false')
        p.set_defaults(redirect_links=True, cls=cls)
        return p
