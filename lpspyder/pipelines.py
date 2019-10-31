# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker

from lpspyder.db_settings import HeadHunterVacancy, create_tables, db_connect
from scrapy.exceptions import DropItem
import json
from scrapy import Selector
import re
from langdetect import detect


task_list = ['Обязанности', 'Должностные обязанности', 'Основные задачи', 'Что нужно будет делать', 'Задачи', 'Вам предстоит', 'Что именно вам предстоит делать', 'Вы будете',
             'Вам доверим', 'Что нужно делать', 'Задачи, которыми предстоит заниматься', 'Задачи внутри команды', 'Ваши задачи', 'Основные обязанности',
             'Вам предстоит', 'Содержание работы', 'Ключевые задачи сотрудника', 'Что будем делать', 'ЗАДАЧИ', 'Что нужно делать',
             'Чем тебе предстоит заниматься', 'Основные задачи, которые предстоит выполнять', 'Что нужно будет делать', 'Какие задачи необходимо будет решать',
             'Чем предстоит заниматься', 'Вам предстоит', 'Чем нужно будет заниматься', 'Тебе предстоит', 'Круг задач', 'Планируемые задачи',
             'Что ты будешь делать', 'Как часть команды, ты будешь вовлечен в', 'ОБЯЗАННОСТИ', 'Чем Вам придется заниматься', 'Основные обязанности',
             'Кандидату хотим поручить следующий фронт работ', 'Ваши задачи', 'Профиль работы']
requirements_list = ['Требования', 'Что мы ожидаем от вас', 'Мы ожидаем от вас', 'От Вас ждем', 'Что потребуется от вас', 'Вы нам подходите, если у вас есть',
                     'Необходимый опыт', 'Мы ожидаем, что вы', 'Мы ищем нового члена нашей команды', 'Мы ищем', 'Что нужно знать и уметь', 'Наши ожидания от вас',
                     'МЫ ОЖИДАЕМ ОТ КАНДИДАТОВ', 'Чего мы ждем от вас', 'Нам нужен', 'От тебя', 'ТРЕБОВАНИЯ', 'Мы ждём от наших будущих коллег', 'Из требований нам важно',
                     'Что мы хотим видеть в кандидате', 'Мы ожидаем от Вас', 'От вас', 'Мы ожидаем что вы', 'Необходимые навыки', 'Ключевые навыки', 'Наши ожидания от Вас', 'Мы ожидаем, что у Вас есть',
                     'Какой опыт и знания нам нужны', 'Мы ждем от тебя', 'Обязательны', 'Что мы хотим видеть у Вас', 'Мы ожидаем от успешного кандидата',
                     'Нам важно, чтобы у Вас было', 'Рассматриваем кандидата имеющего', 'Обязательно', 'Необходимо', 'Что хотим видеть у кандидата', 'Опыт и навыки, на который мы рассчитываем',
                     'Что ты уже умеешь', 'Что мы ждем от тебя', 'Что мы ждем от кандидата', 'Наши ожидания']
company_offer_list = ['Мы предлагаем', 'Почему с нами круто', 'Наше предложение', 'У нас', 'Что предлагаем взамен', 'Также мы предлагаем', 'Что мы готовы предложить',
                      'Условия', 'Что мы за это предлагаем', 'Своим сотрудникам мы предлагаем', 'Что предлагаем мы', ' Дополнительно учитывается, но не обязательно',
                      'От компании', 'В свою очередь компания предлагает следующие условия', 'УСЛОВИЯ', 'Преимущества работы у нас',
                      'Работа у нас — это', 'Что мы предлагаем', 'От нас', 'вы получите', 'Работа в Аркадии — это']
will_plus_list = ['Будет плюсом', 'Желательно', 'Приветствуются',
                  'Будет плюсом, если вы', 'Плюсом будет', 'Приветствуется', 'Очень приветствуется', 'Плюсами будут знания', 'будет большим плюсом', 'Преимуществом будет',
                  'Дополнительно', 'Большим плюсом будет']

common_list = task_list + requirements_list + company_offer_list + will_plus_list


class MysqlInsertHeadHunterVacancyPipline(object):

    """
    Initializes database connection and sessionmaker.
    Creates tables.
    """

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        vacancy = HeadHunterVacancy(**item)
        vacancy_exist = session.query(HeadHunterVacancy).filter_by(
            vacancy_url=item['vacancy_url'], vacancy_name=item['vacancy_name'], vacancy_published_at=item['vacancy_published_at']).first()
        if vacancy_exist:
            raise DropItem(f"Dublicate found: {item['vacancy_url']}")
            session.close()
        else:
            try:
                session.add(vacancy)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item


class CleanDescriptionPipline(object):
    def process_item(self, item, spider):
        if item['vacancy_text_dirty']:
            item['vacancy_text_clean'] = re.sub(
                r'(</li>)', ';', item['vacancy_text_dirty'])
            item['vacancy_text_clean'] = re.sub(
                r'(</br>)', ';', item['vacancy_text_clean'])
            item['vacancy_text_clean'] = re.sub(
                r'(<br>)', ';', item['vacancy_text_clean'])
            item['vacancy_text_clean'] = re.sub(
                r'<[^>]+>', '', item['vacancy_text_clean'])
            item['vacancy_text_clean'] = re.sub(
                '•', ';', item['vacancy_text_clean'])
            item['vacancy_text_clean'] = re.sub(
                ';;', ';', item['vacancy_text_clean'])
            item['vacancy_text_clean'] = str(item['vacancy_text_clean'])
            return item


class CleanDatetimePipline(object):
    def process_item(self, item, spider):
        if item['vacancy_published_at']:
            item['vacancy_published_at'] = re.sub(
                r'T', ' ', item['vacancy_published_at'])
            item['vacancy_published_at'] = item['vacancy_published_at'][:(len(item['vacancy_published_at'])-10)]
            return item



class LangDetectionPipline(object):
    def process_item(self, item, spyder):
        if item['vacancy_text_clean']:
            item['lang'] = detect(item['vacancy_text_clean'])
            return item


class SortCleanTextPipline(object):
    def process_item(self, item, spyder):
        if item['vacancy_text_clean']:
            task_idx = []
            task_value = []
            requirements_idx = []
            requirements_value = []
            company_offer_idx = []
            company_offer_value = []
            will_plus_idx = []
            will_plus_value = []

            for hh_mean in common_list:
                if hh_mean in item['vacancy_text_clean']:

                    if hh_mean in task_list:
                        task_idx.append(
                            item['vacancy_text_clean'].find(hh_mean))
                        task_value.append(hh_mean)
                    elif hh_mean in requirements_list:
                        requirements_idx.append(
                            item['vacancy_text_clean'].find(hh_mean))
                        requirements_value.append(hh_mean)
                    elif hh_mean in company_offer_list:
                        company_offer_idx.append(
                            item['vacancy_text_clean'].find(hh_mean))
                        company_offer_value.append(hh_mean)
                    elif hh_mean in will_plus_list:
                        will_plus_idx.append(
                            item['vacancy_text_clean'].find(hh_mean))
                        will_plus_value.append(hh_mean)

            if task_idx != []:
                item['task_idx'] = str(task_idx)
                item['task_text_value'] = str(task_value)

            if requirements_idx != []:
                item['requirements_idx'] = str(requirements_idx)
                item['requirements_text_value'] = str(requirements_value)

            if company_offer_idx != []:
                item['company_offer_idx'] = str(company_offer_idx)
                item['company_offer_text_value'] = str(company_offer_value)

            if will_plus_idx != []:
                item['will_plus_idx'] = str(will_plus_idx)
                item['will_plus_text_value'] = str(will_plus_value)

            if task_idx != [] or requirements_idx != [] or company_offer_idx != [] or will_plus_idx != []:

                common = sorted(task_idx + requirements_idx +
                                company_offer_idx + will_plus_idx)

                common_idx = []

                # clean dublicates
                for num in common:
                    if num not in common_idx:
                        common_idx.append(num)

                item['common_idx'] = str(common_idx)

                matrix = []
                list = common_idx

                task_text = []
                requirements_text = []
                company_offer_text = []
                will_plus_text = []

                while list != []:
                    matrix.append(list[:2])
                    list = list[1:]

                for index, value in enumerate(matrix):
                    if len(value) == 2:
                        clean_string = item['vacancy_text_clean'][value[0]:value[1]]

                    if len(value) == 1:
                        clean_string = item['vacancy_text_clean'][value[0]:]

                    if value[0] in task_idx:
                        task_text.append(clean_string)

                    if value[0] in requirements_idx:
                        requirements_text.append(clean_string)

                    if value[0] in company_offer_idx:
                        company_offer_text.append(clean_string)

                    if value[0] in will_plus_idx:
                        will_plus_text.append(clean_string)

                item['task_text'] = str(task_text)
                item['requirements_text'] = str(requirements_text)
                item['company_offer_text'] = str(company_offer_text)
                item['will_plus_text'] = str(will_plus_text)

            return item
