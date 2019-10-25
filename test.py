from webapp import create_app
from webapp.model import Skills


def get_skill_list(category):
    app = create_app()
    with app.app_context():
        return Skills.query.filter(Skills.category == category).all()

