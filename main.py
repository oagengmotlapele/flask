import sys
import os
from dotenv import load_dotenv
from flask import request, session, redirect, render_template

from src.controller.MySQLControllerFlask import MySQLManager
from src.view import create_app  # Absolute import

load_dotenv()
app = create_app()

@app.before_request
def save_last_visited_url():
    session.permanent=True
    if not session.get('theme'):
        session['theme'] = 'skyblue'

@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' ;"
        "style-src 'self' ; "
        "img-src 'self' data:; "
        "font-src 'self'; "
    )
    return response

@app.route("/<string:route>", methods=["GET", "POST"])
def form(route):
    db = MySQLManager()
    data=db.manage_table("route", query="select",where={"route":route})
    if len(data)>=1:
        action = data[0]['action']
        if request.method == "POST":
            if action == 'update':
                form_data = request.form.to_dict()
                #db.manage_table(data[0]['table'], query="update", where={"id": form_data.get("id")}, row_data=form_data)
                return redirect(request.referrer or '/')

            elif action == 'insert':
                form_data = request.form.to_dict()
                #db.manage_table(data[0]['table_name'], query="insert", row_data=form_data)

                return redirect(request.referrer or '/')

        if action == 'delete' and request.method != "POST":
            form_data = request.form.to_dict()
            #db.manage_table(data[0]['table'], query="delete", where=data[0]['where'])
            return redirect(request.referrer or '/')
        return render_template("form.html", name="form_name", data=[])
    else:return redirect("/")


if __name__ == "__main__":
    debug=False
    if os.getenv("production")==False:debug=True
    app.run(debug=True,host="0.0.0.0",port=6526)
