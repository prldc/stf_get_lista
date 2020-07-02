# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import pandas as pd


class ListabotSpider(scrapy.Spider):
    name = 'listabot'
    allowed_domains = ['http://www.stf.jus.br']
    script = '''
                       function main(splash, args)
                           assert(splash:go(args.url))
                           assert(splash:wait(1))
                           splash:set_viewport_full()
                           return splash:html()
                        end
                   '''
    custom_settings = {
        'FEED_URI': 'julgados_lista.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'scrapy.exporters.CsvItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    def start_requests(self):
        # df = pd.read_csv('lista2016+_H.csv')
        df = pd.read_csv('julgamentos_lista_formatados.csv')
        list = df.links.to_list()
        start_urls = list
        for i in range(0, len(start_urls)):
            yield SplashRequest(
                url=start_urls[i],
                callback=self.parse, endpoint="execute", args={
                    'lua_source': self.script
                })

    def parse(self, response):
        out_dict = {}
        processos = response.xpath("//div[@id='topo']/div/div/strong/a/text()")
        for elem in processos:
            out_dict["nome"] = elem.get()
            out_dict["lista"] = True
            out_dict["link"] = response
        yield out_dict
