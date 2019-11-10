import json

from flask import Flask, render_template, request, Blueprint
from webapp.statistic.funcs_statistic import set_json_statistic, get_words_stat
from ast import literal_eval
from collections import defaultdict

blueprint = Blueprint('statistic', __name__)


@blueprint.route('/statistic', methods=['GET'])
def statistic():
    title = 'Статистика вакансий'

    #url = 'https://hh.ru/vacancy/34309601'

    # statistic = set_json_statistic()
    # update_vacancies = copy_vacancies()
    #words_stat = get_words_stat()

    with open('data/statistic/vacancies_stat.json', mode='r', encoding='utf8') as vs:
        vacstat = json.load(vs)
        languages = vacstat['languages']
        prof_areas = vacstat['profession_vacancies']
        area_exp = vacstat['areas_experience']

    with open('data/statistic/words_stat.json', mode='r', encoding='utf8') as ws:
        words_stat = json.load(ws)

    return render_template('statistic/statistic.html', page_title=title, prof_areas=prof_areas, area_exp=area_exp,
                           languages=languages, words_stat=words_stat)
