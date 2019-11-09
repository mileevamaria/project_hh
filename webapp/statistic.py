from webapp.model import db, Vacancy, Statistic, ProfessionalArea, VacancyGrade, SpyderVacancies
from sqlalchemy import func, and_
import pandas as pd
import numpy as np
import json
from datetime import datetime
from ast import literal_eval
from collections import defaultdict

""" todays_datetime = datetime(datetime.today().year,
                           datetime.today().month, datetime.today().day) """
todays_datetime = "2019-11-8"
cutoff_value = 0.5


def copy_vacancies():
    vacancies_urls = SpyderVacancies.query.with_entities(
        SpyderVacancies.vacancy_url).filter(SpyderVacancies.created_at >= todays_datetime).all()

    for url in vacancies_urls:
        check_url = Vacancy.query.filter(
            Vacancy.vacancy_url == url[0]).first()

        if check_url is None:
            get_new_vacancy = SpyderVacancies.query.filter(
                SpyderVacancies.vacancy_url == url[0]).first()


            set_new_vacancy = Vacancy(
                vacancy_url=get_new_vacancy.vacancy_url,
                vacancy_name=get_new_vacancy.vacancy_name,
                vacancy_city=get_new_vacancy.vacancy_city,
                vacancy_country=get_new_vacancy.vacancy_country,
                vacancy_salary_value=get_new_vacancy.vacancy_salary_value,
                vacancy_salary_min=get_new_vacancy.vacancy_salary_min,
                vacancy_salary_max=get_new_vacancy.vacancy_salary_max,
                vacancy_salary_currency=get_new_vacancy.vacancy_salary_currency,
                vacancy_salary_period=get_new_vacancy.vacancy_salary_period,
                company_name=get_new_vacancy.company_name,
                vacancy_expirience=get_new_vacancy.vacancy_expirience,
                vacancy_employment_type=get_new_vacancy.vacancy_employment_type,
                vacancy_text_clean=get_new_vacancy.vacancy_text_clean,
                vacancy_key_skills=get_new_vacancy.vacancy_key_skills,
                industry=get_new_vacancy.industry,
                language=get_new_vacancy.language,
                vacancy_published_at=get_new_vacancy.vacancy_published_at
            )
            db.session.add(set_new_vacancy)
            db.session.commit()


def set_json_statistic():
    data = {}
    # дата
    data['date'] = todays_datetime

    # количество вакансий
    data['vacancy_count'] = Vacancy.query.count()

    # языки
    # языки вакансий
    languages = db.session.query(Vacancy.language, db.func.count(
        Vacancy.language)).group_by(Vacancy.language).all()

    lang_stat = defaultdict(list)
    for k, v in languages:
        lang_stat[k].append(v)
    lang_stat = dict(lang_stat)

    data['languages'] = lang_stat

    # профессии
    professions = ProfessionalArea.query.all()
    professions_count = ProfessionalArea.query.count()

    profession_vacancy = []
    expirience_dict = {}
    no_exp = []
    one_three_year = []
    three_six_year = []
    more_six_year = []
    for profession in professions:
        prof_dict = {}

        prof_dict['prof_id'] = profession.id
        prof_dict['prof_name'] = profession.area_name

        prof_graded_vacancies = VacancyGrade.query.with_entities(VacancyGrade.vacancy_id).filter(
            VacancyGrade.prof_area_id == profession.id, VacancyGrade.grade >= cutoff_value).all()

        ids = []
        for id_ins in prof_graded_vacancies:
            ids.append(id_ins[0])

        prof_dict['vacancies_array'] = ids

        count = VacancyGrade.query.filter(
            VacancyGrade.prof_area_id == profession.id, VacancyGrade.grade >= cutoff_value).count()

        prof_dict['count'] = count

        expiriense = VacancyGrade.query.with_entities(
            Vacancy.vacancy_expirience, db.func.count(Vacancy.vacancy_expirience)).join(Vacancy.vacancy_grades).filter(VacancyGrade.prof_area_id == profession.id, VacancyGrade.grade >= cutoff_value).group_by(Vacancy.vacancy_expirience).all()

        exp_list = []

        for k, v in expiriense:
            exp_dict = {}
            if k == 'не требуется':
                exp_dict['no_exp'] = [v]
                exp_list.append(exp_dict)
                no_exp.append(v)
            if k == '1–3 года':
                exp_dict['one_three_year'] = [v]
                exp_list.append(exp_dict)
                one_three_year.append(v)
            if k == '3–6 лет':
                exp_dict['three_six_year'] = [v]
                exp_list.append(exp_dict)
                three_six_year.append(v)
            if k == 'более 6 лет':
                exp_dict['more_six_year'] = [v]
                exp_list.append(exp_dict)
                more_six_year.append(v)

        prof_dict['expiriense'] = exp_list

        profession_vacancy.append(prof_dict)

    expirience_dict['no_exp'] = no_exp
    expirience_dict['one_three_year'] = one_three_year
    expirience_dict['three_six_year'] = three_six_year
    expirience_dict['more_six_year'] = more_six_year

    ungraded_dict = {}
    ungraded_dict['prof_id'] = professions_count + 1
    ungraded_dict['prof_name'] = 'Unknown'

    search_ungrades = db.session.query(VacancyGrade.vacancy_id, db.func.count(
        VacancyGrade.vacancy_id)).filter(VacancyGrade.grade < 0.5).group_by(VacancyGrade.vacancy_id).all()

    ungraded_vacancies_ids = []
    ungraded_count = 0
    for ungraded in search_ungrades:
        if ungraded[1] == professions_count:
            ungraded_vacancies_ids.append(ungraded[0])
            ungraded_count += 1

    ungraded_dict['vacancies_array'] = ungraded_vacancies_ids
    ungraded_dict['count'] = ungraded_count
    profession_vacancy.append(ungraded_dict)

    data['profession_vacancies'] = profession_vacancy
    data['areas_experience'] = [expirience_dict]

    with open('vacancies_stat.json', mode='w+', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False,)


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


def get_grades():
    grades_stat = Statistic.query.with_entities(
        Statistic.grades).filter(Statistic.created_at >= todays_datetime).first()

    grade_string = ''
    for grade in grades_stat:
        grade_string = grade

    grade_string = grade_string.replace("'", "\"")
    grade_stat = json.loads(grade_string)

    df_grades = pd.DataFrame.from_dict(grade_stat)

    grade_labels = list(df_grades.columns)
    x_data = df_grades.to_numpy()

    grade_values = []
    for data in x_data:
        data = str(data).strip('[]').split(' ')
        for x in data:
            if x != '':
                grade_values.append(int(x))

    return grade_labels, grade_values
