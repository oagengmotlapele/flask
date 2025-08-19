import matplotlib
from dotenv import load_dotenv
from flask import Blueprint, render_template, request,redirect, session, url_for
from src.controller.MySQLControllerFlask import MySQLManager
from src.controller.navs.index import MenuGenerator
from src.middlewares.encode import Encode
from src.utils.Security import Security
from src.utils.files import Files
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





@index.route('/themes/<theme>',methods=['GET', 'POST'])
def set_theme(theme):
    session['theme'] = theme
    session.permanent = True
    return redirect(session.get('last_url') or url_for('index_view.index_view'))

@index.route('/about')
def about():
    return render_template('about.html')

@index.route('/team')
def team():
    return render_template('team.html')

@index.route('/contact')
def contact():
    return render_template('contact.html')

@index.route('/services')
def services():
    return render_template('services.html')

@index.route('/projects')
def portfolio():
    return render_template('portfolio.html')

@index.route('/blog')
def blog():
    return render_template('blog.html')

@index.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@index.route('/faq')
def faq():
    return render_template('faq.html')

@index.route('/newsletter')
def newsletter():
    return render_template('newsletter.html')

@index.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@index.route("/")
def index_view():
    files=f"{file}_root"
    session.permanent= True
    session['last_url'] = request.url
    rights={"fetch":f'user_{files}',
             "user":session.get('user')}
    form=[]
    return render_template('index.html',
                           base=base_static(),
                           pic=Encode().base64Encode(pictures_path),
                           usr_id_rights=Security().usr_id_rights(rights=rights),
                           role_rights=Security().role_rights(rights=rights),
                           nav=MenuGenerator().get_full_menu(),
                           form=form,
                           )

