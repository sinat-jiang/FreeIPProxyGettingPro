# _*_ coding : utf-8 _*_

# 自定义爬虫链

from ProxiesSpider import (
    kuai_proxy_spider,
    seo_proxy_spider,
    zdaye_proxy_spider,
    stock_proxy_spider
)


proxy_spiders = [
    stock_proxy_spider.SpiderStock,
    kuai_proxy_spider.SpiderKuai,
    seo_proxy_spider.SpiderSeo,
    zdaye_proxy_spider.SpiderZdaye
]
