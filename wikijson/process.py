import gzip
import ujson as json

from wikijson import extractor
from time import time

import logging
log = logging.getLogger()

class ProcessDump(object):
    """ Extra a simple json representation for each article in a wikipedia dump """
    def __init__(self, wk_dump_path, output_path):
        self.wk_dump_path = wk_dump_path
        self.output_path = output_path

    def __call__(self):
        log.info('Processing wiki dump: %s ...', self.wk_dump_path)
        with gzip.open(self.output_path, 'w') as f:
            t = time()
            for i, (id, title, text, links, categories) in enumerate(extractor.iter_items(self.wk_dump_path)):
                if i % 100000 == 0 or i == 1000 or i == 10000:
                    log.info('Processed %i articles, %.1fs...', i, time() - t)
                    t = time()

                f.write(json.dumps({
                    'id': id,
                    'title': title.replace(' ', '_'),
                    'text': text,
                    'categories': categories,
                    'links': [{
                        'target': target,
                        'start': span.start,
                        'stop': span.stop
                    } for target, span in links]
                }) + '\n')

        log.info('Done.')

    @classmethod
    def add_arguments(cls, p):
        p.add_argument('wk_dump_path', metavar='WK_DUMP_PATH')
        p.add_argument('output_path', metavar='OUTPUT_PATH')
        p.set_defaults(cls=cls)
        return p
