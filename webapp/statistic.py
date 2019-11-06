from webapp.model import db, Vacancy, Statistic, ProfessionalArea, VacancyGrade
from sqlalchemy import func, and_
import pandas as pd
import numpy as np
import json
from datetime import datetime
from ast import literal_eval
from collections import defaultdict

""" todays_datetime = datetime(datetime.today().year,
                           datetime.today().month, datetime.today().day) """
todays_datetime = "2019-11-4"


def set_statistic():

    # количество вакансий
    vacancy_count = Vacancy.query.count()

    # языки вакансий
    languages = db.session.query(Vacancy.language, db.func.count(
        Vacancy.language)).group_by(Vacancy.language).all()

    lang_stat = defaultdict(list)
    for k, v in languages:
        lang_stat[k].append(v)
    lang_stat = str(dict(lang_stat))

    # специализация вакансий
    search_grades = db.session.query(VacancyGrade.prof_area_id, db.func.count(
        VacancyGrade.prof_area_id)).filter(VacancyGrade.grade >= 0.5).group_by(VacancyGrade.prof_area_id).all()

    search_ungrades = db.session.query(VacancyGrade.vacancy_id, db.func.count(
        VacancyGrade.vacancy_id)).filter(VacancyGrade.grade < 0.5).group_by(VacancyGrade.vacancy_id).all()

    ungraded_vacancies_ids = []

    ungraded_count = 0

    for ungraded in search_ungrades:
        if ungraded[1] == 7:
            ungraded_vacancies_ids.append(ungraded[0])
            ungraded_count += 1

    grades_stat = defaultdict(list)
    for k, v in search_grades:
        prof_name = ProfessionalArea.query.with_entities(
            ProfessionalArea.area_name).filter(ProfessionalArea.id == k).first()
        grades_stat[prof_name[0]].append(v)
    grades_stat['Ungraded'].append(ungraded_count)
    grades_stat = str(dict(grades_stat))

    ungraded_vacancies_ids = str(ungraded_vacancies_ids)

    set_languages = Statistic(
        vacancy_count=vacancy_count, languages=lang_stat, grades=grades_stat, ungraded_vacancies=ungraded_vacancies_ids)
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
