import matplotlib
from dotenv import load_dotenv
from flask import Blueprint, render_template, request,redirect, session, url_for
from src.controller.MySQLControllerFlask import MySQLManager
from src.middlewares.encode import Encode
from src.utils.Security import Security
from src.utils.files import Files
from src.model.view_model.nav.users.index.endpoint.root import Nav
from src.model.view_model.cards.users.index.endpoint.root import Cards

THEMES = list(matplotlib.colors.CSS4_COLORS.keys())
file='index'

# Load variables from .env
load_dotenv(dotenv_path='../config/view.env')
file_path="src/view/static"
pictures_path=Files().get_all_files(file_path)

def loads_cards(users)->dict:
    cards={
        'mission':Cards().get_cards_data(file='1',user=users)
    }
    return cards

def base_static():
    base={
        "themes":THEMES,
        "theme" :session.get('theme'),
        "css"   :Files().get_css_links(file_path),
        "js"    :Files().get_js_links(file_path),
        "layout":"base/Layout_3.html",
    }
    return base

index = Blueprint('index_view',
                  __name__,template_folder='../templates'
                  ,static_folder='../static'         # Relative to index.py
                  ,static_url_path='/static' )

db = MySQLManager()


@index.route('/team', methods=['GET', 'POST'])
def team_handler():
    db = MySQLManager()
    TABLE_NAME = "team"
    user = request.form.get("username", "system_user")

    if request.method == "POST":
        action = request.form.get("action")
        full_name = request.form.get("full_name")
        role = request.form.get("role")
        member_id = request.form.get("id")

        # INSERT
        if action == "add":
            row_data = {
                "full_name": full_name,
                "role": role
            }
            db.manage_table(
                table_name=TABLE_NAME,
                row_data=row_data,
                query="insert",
                user=user
            )

        # UPDATE
        elif action == "update" and member_id:
            row_data = {
                "full_name": full_name,
                "role": role
            }
            where = {"id": int(member_id)}
            db.manage_table(
                table_name=TABLE_NAME,
                row_data=row_data,
                query="update",
                where=where,
                user=user
            )

        # SOFT DELETE
        elif action == "delete" and member_id:
            where = {"id": int(member_id)}
            db.manage_table(
                table_name=TABLE_NAME,
                query="delete",
                where=where,
                user=user
            )

        return redirect("/team")

    # SELECT
    rows = db.manage_table(
        table_name=TABLE_NAME,
        query="select"
    )
    return render_template("team.html", team=rows)


@index.route('/themes/<theme>',methods=['GET', 'POST'])
def set_theme(theme):
    session['theme'] = theme
    session.permanent = True
    return redirect(session.get('last_url') or url_for('index_view.index_view'))

@index.route("/contact")
def contact():
    return render_template('endpoints/index/contact.html',)

@index.route("/")
def index_view():
    rights={"fetch":f'user_{file}',
             "user":session.get('user')}
    form=[]
    return render_template('index.html',
                           base=base_static(),
                           pic=Encode().base64Encode(pictures_path),
                           usr_id_rights=Security().usr_id_rights(rights=rights),
                           role_rights=Security().role_rights(rights=rights),
                           nav=Nav().index_py()['/'],
                           form=form,
                           )
