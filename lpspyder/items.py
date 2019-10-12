# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeadHunterVacancy(scrapy.Item):

    vacancy_url = scrapy.Field()
    vacancy_name = scrapy.Field()
    vacancy_city = scrapy.Field()
    vacancy_country = scrapy.Field()
    vacancy_salary_value = scrapy.Field()
    vacancy_salary_min = scrapy.Field()
    vacancy_salary_max = scrapy.Field()
    vacancy_salary_currency = scrapy.Field()
    vacancy_salary_period = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    vacancy_adress = scrapy.Field()
    vacancy_expirience = scrapy.Field()
    vacancy_employment_type = scrapy.Field()
    vacancy_text_dirty = scrapy.Field()
    vacancy_text_clean = scrapy.Field()
    vacancy_key_skills = scrapy.Field()
    industry = scrapy.Field()
    lang = scrapy.Field()
    task_idx = scrapy.Field()
    requirements_idx = scrapy.Field()
    company_offer_idx = scrapy.Field()
    will_plus_idx = scrapy.Field()
    common_idx = scrapy.Field()
    task_text = scrapy.Field()
    task_text_value = scrapy.Field()
    requirements_text = scrapy.Field()
    requirements_text_value = scrapy.Field()
    company_offer_text = scrapy.Field()
    company_offer_text_value = scrapy.Field()
    will_plus_text = scrapy.Field()
    will_plus_text_value = scrapy.Field()
    vacancy_published_at = scrapy.Field()
