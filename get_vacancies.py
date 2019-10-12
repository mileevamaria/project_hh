from scrapy.crawler import CrawlerProcess

from lpspyder.spiders.hh_spyder import HeadHunterSpyder
from lpspyder.db_settings import *


def get_vacancies():
    """ Write here call for crawl """

    process = CrawlerProcess(get_project_settings())
    process.crawl(HeadHunterSpyder)
    process.start()

    return False


if __name__ == '__main__':
    get_vacancies()
