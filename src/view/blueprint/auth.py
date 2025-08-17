
import os
from dotenv import load_dotenv
import os
from flask import Blueprint, render_template

# Load variables from .env
load_dotenv(dotenv_path='../config/view.env')
auth = Blueprint('auth', __name__,template_folder='../templates', static_folder='../static')
@auth.route("/")
def index_view():
    layout = os.getenv('base_template')
    return render_template('index_view.html',
                           layout=layout,
                           )
