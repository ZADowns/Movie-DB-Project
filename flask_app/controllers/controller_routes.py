from flask import render_template, redirect, request, session, flash
from flask_app import app
# from flask_app.models.model import model_class


@app.route('/')
def index():

    return render_template('dashboard.html')