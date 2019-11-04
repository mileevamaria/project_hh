from webapp.model import Vacancy
from sqlalchemy import func
from webapp.model import db


import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json


def vacancy_count():
    vacancies_count = Vacancy.query.count()
    return vacancies_count


def languages():
    languages = db.session.query(Vacancy.language, db.func.count(
        Vacancy.language)).group_by(Vacancy.language).all()
    languages = dict(languages)


    return languages
