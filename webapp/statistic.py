from webapp.model import Vacancy, Statistic
from sqlalchemy import func
from webapp.model import db
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json


def set_statistic():

    vacancy_count = Vacancy.query.count()

    languages = db.session.query(Vacancy.language, db.func.count(
        Vacancy.language)).group_by(Vacancy.language).all()
    languages = dict(languages)
    languages = json.dumps(languages, ensure_ascii=False).encode('utf8')
    languages = languages.decode('utf8')

    set_languages = Statistic(vacancy_count=vacancy_count, languages=languages)
    db.session.add(set_languages)
    db.session.commit()

    return languages


def get_languages():
    pass
