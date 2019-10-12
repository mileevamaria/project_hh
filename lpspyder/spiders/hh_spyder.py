# -*- coding: utf-8 -*-
import json
import os
import scrapy
from lpspyder.items import HeadHunterVacancy
from datetime import date, timedelta

# scrapy crawl hh_spyder -t csv -o test_vacancies_hh.csv


class HeadHunterSpyder(scrapy.Spider):

    name = 'hh_spyder'
    custom_settings = {
        'ITEM_PIPELINES':  {
            'lpspyder.pipelines.CleanDescriptionPipline': 300,
            'lpspyder.pipelines.LangDetectionPipline': 301,
            'lpspyder.pipelines.SortCleanTextPipline': 302,
            'lpspyder.pipelines.MysqlInsertHeadHunterVacancyPipline': 313,
        },
        'LOG_FILE': 'hh_log.txt',
        'LOG_LEVEL': 'INFO',
        'COOKIES_DEBUG': 'False',
        'AUTOTHROTTLE_DEBUG': 'False',
        'DUPEFILTER_DEBUG': 'True'
    }
    allowed_domains = ['hh.ru']

    # search period: month
    start_urls = [
        'https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&items_on_page=100&no_magic=true&enable_snippets=true&salary=&st=searchVacancy&text=python'
    ]

    # search period: last 7 days
    # start_urls = [
    #     'https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&items_on_page=100&no_magic=true&enable_snippets=true&search_period=7&salary=&st=searchVacancy&text=python'
    # ]

    # search period: last 24 hours
    # start_urls = [
    #     'https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&items_on_page=100&no_magic=true&enable_snippets=true&search_period=1&salary=&st=searchVacancy&text=python'
    # ]

    def parse(self, response):

        self.logger.debug('PARSE: Parse function called on %s', response.url)

        areas_urls = response.xpath(
            '//div[@data-qa="serp__clusters"]/div[@data-qa="serp__cluster-group"][1]//a[@class="clusters-value"]/@href').getall()
        for url in areas_urls:
            find_capitals = url.split('&')[5]
            """
                'area=1' - Москва
                Так как ограничение выдачи - 2000 вакансий, а в Москве их больше, то по ним дополнительная фильтрафия по станциям метро.
                Актуально в случае сбора данных за месяц.
                """
            if find_capitals == 'area=1':
                yield response.follow(url, callback=self.capital)
            else:
                yield response.follow(url, callback=self.cluster)

    def capital(self, response):

        self.logger.debug(
            'CAPITAL: Parse function called on %s', response.url)

        capital_urls = response.xpath(
            '//div[@data-qa="serp__clusters"]/div[@data-qa="serp__cluster-group"][3]//a[@class="clusters-value"]/@href').getall()

        for url in capital_urls:
            yield response.follow(url, callback=self.cluster)

    def cluster(self, response):

        self.logger.debug('CLUSTER: Parse function called on %s', response.url)

        vacancy_urls = response.xpath(
            '//div[@data-qa="vacancy-serp__results"]//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()

        for url in vacancy_urls:
            clean_url = url.split('?', maxsplit=1)[0]
            yield response.follow(clean_url, callback=self.vacancy)

        next_page = response.xpath(
            '//div[@data-qa="pager-block"]//a[@data-qa="pager-next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.cluster)

    def vacancy(self, response):

        self.logger.debug(
            f'VACANCY: Parse function called on {response.url}')

        employment_type = response.xpath(
            '//p[@data-qa="vacancy-view-employment-mode"]/text()').get() + response.xpath('//p[@data-qa="vacancy-view-employment-mode"]/span[@itemprop="workHours"]/text()').get()

        # for vacancy in response:
        v = HeadHunterVacancy()
        v['vacancy_url'] = response.url
        v['vacancy_name'] = response.xpath(
            '//h1[@data-qa="vacancy-title"]/text()').get()
        if response.xpath(
                '//meta[@itemprop="addressLocality"]/@content') is not None:
            v['vacancy_city'] = response.xpath(
                '//meta[@itemprop="addressLocality"]/@content').get()
        elif response.xpath(
                '//meta[@itemprop="addressRegion"]/@content') is not None:
            v['vacancy_city'] = response.xpath(
                '//meta[@itemprop="addressRegion"]/@content').get()
        else:
            v['vacancy_city'] = None
        v['vacancy_country'] = response.xpath(
            '//meta[@itemprop="addressCountry"]/@content').get()
        if response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="value"]/@content') is not None:
            v['vacancy_salary_value'] = response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="value"]/@content').get()
        if response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="minValue"]/@content') is not None:
            v['vacancy_salary_min'] = response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="minValue"]/@content').get()
        if response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="maxValue"]/@content') is not None:
            v['vacancy_salary_max'] = response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="maxValue"]/@content').get()
        if response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="currency"]/@content') is not None:
            v['vacancy_salary_currency'] = response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="currency"]/@content').get()
        if response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="unitText"]/@content') is not None:
            v['vacancy_salary_period'] = response.xpath(
                '//span[@itemprop="baseSalary"]//meta[@itemprop="unitText"]/@content').get()
        v['company_name'] = response.xpath(
            '//div[@data-qa="vacancy-company"]//meta[@itemprop="name"]/@content').get()
        v['company_url'] = response.xpath(
            '//div[@data-qa="vacancy-company"]//a[@itemprop="hiringOrganization"]/@href').get()
        v['vacancy_adress'] = response.xpath(
            '//div[@data-qa="vacancy-company"]//span[@data-qa="vacancy-view-raw-address"]/text()').get()
        v['vacancy_expirience'] = response.xpath(
            '//span[@data-qa="vacancy-experience"]/text()').get()
        v['vacancy_employment_type'] = employment_type
        v['vacancy_text_dirty'] = response.xpath(
            '//div[@data-qa="vacancy-description"]').get()
        if response.xpath('//span[@data-qa="skills-element"]//span[@data-qa="bloko-tag__text"]/text()') is not None:
            key_skills = response.xpath(
                '//span[@data-qa="skills-element"]//span[@data-qa="bloko-tag__text"]/text()').getall()
            v['vacancy_key_skills'] = str(key_skills)
        v['industry'] = response.xpath(
            '//meta[@itemprop="industry"]/@content').get()
        v['vacancy_published_at'] = response.xpath(
            '//meta[@itemprop="datePosted"]/@content').get()
        yield v
