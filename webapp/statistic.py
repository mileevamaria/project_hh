from webapp.model import Vacancy, Statistic
from sqlalchemy import func, and_
from webapp.model import db
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from datetime import datetime
from ast import literal_eval
from collections import defaultdict

todays_datetime = datetime(datetime.today().year,
                           datetime.today().month, datetime.today().day)


def set_statistic():

    vacancy_count = Vacancy.query.count()

    languages = db.session.query(Vacancy.language, db.func.count(
        Vacancy.language)).group_by(Vacancy.language).all()

    lang_stat = defaultdict(list)
    for k, v in languages:
        lang_stat[k].append(v)
    lang_stat = str(dict(lang_stat))

    set_languages = Statistic(vacancy_count=vacancy_count, languages=lang_stat)
    db.session.add(set_languages)
    db.session.commit()


def get_vacancies_count():
    vacancies_count = Statistic.query.with_entities(
        Statistic.vacancy_count).filter(Statistic.created_at >= todays_datetime).first()

    vac_count = 0
    for count in vacancies_count:
        vac_count = int(count)

    return vac_count


def get_languages():
    languages_stat = Statistic.query.with_entities(
        Statistic.languages).filter(Statistic.created_at >= todays_datetime).first()

    lang_string = ''
    for lang in languages_stat:
        lang_string = lang

    lang_string = lang_string.replace("'", "\"")
    lang_stat = json.loads(lang_string)

    df_langs = pd.DataFrame.from_dict(lang_stat)

    lang_labels = list(df_langs.columns)
    x_data = df_langs.to_numpy()

    lang_values = []
    for data in x_data:
        data = str(data).strip('[]').split(' ')
        for x in data:
            if x != '':
                lang_values.append(int(x))

    return lang_labels, lang_values
