# _*_ coding : utf-8 _*_

# 自定义爬虫链

from ProxiesSpider import (
    eightnine_proxy_spider,
    kaixin_proxy_spider,
    kuai_proxy_spider,
    proxyhub_proxy_spider,
    seo_proxy_spider,
    sixsix_proxy_spider,
    yun_proxy_spider,
    zdaye_proxy_spider,
    stock_proxy_spider
)


proxy_spiders = [
    stock_proxy_spider.SpiderStock,
    eightnine_proxy_spider.Spider89,
    kaixin_proxy_spider.SpiderKaixin,
    kuai_proxy_spider.SpiderKuai,
    proxyhub_proxy_spider.SpiderPH,
    seo_proxy_spider.SpiderSeo,
    sixsix_proxy_spider.Spider66,
    yun_proxy_spider.SpiderYun,
    zdaye_proxy_spider.SpiderZdaye
]
