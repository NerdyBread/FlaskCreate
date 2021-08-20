import os
import subprocess
from sys import platform
from time import sleep

import click

@click.command()
@click.option("--dir", "-d", default=".", help="Directory to create flask application")
@click.option("--app_name", "-n", default="newApp", help="Name of application")
@click.option("--venv_name", "-v", default="venv", help="Name of virtual environment")
def create_app(dir, app_name, venv_name):
	# Navigate to dir
	os.chdir(dir)
	# Create the venv and activate it
	subprocess.Popen(["python", "-m", "venv", venv_name])
	sleep(10)
	click.echo("Creating virtual environment...")
	if platform == "win32":
		subprocess.Popen([venv_name + r"\Scripts\activate.bat"])
	else:
		subprocess.Popen(f". {venv_name}/bin/activate.sh") # In theory this should work | I got the ". instead of source" thing from stack overflow
	# Install packages
	subprocess.Popen(["pip", "install", "flask", "python-dotenv", "flask-wtf"])
	# Make requirements.txt
	subprocess.Popen(["pip", "freeze", ">", "requirements.txt"])
	# Create the other top level files
	main = open(f"{app_name}.py", 'w')
	main.write("from app import app")
	main.close()

	config = open("config.py", "w")
	config.write("class Config(object):\npass\n#SECRET_KEY='secret'")
	config.close()

	flaskenv = open(".flaskenv", "w")
	flaskenv.write(f"FLASK_APP={app_name}.py")
	flaskenv.close()
	# Make app folder and all the stuff inside
	os.mkdir("app")
	os.chdir("app")
	os.mkdir("templates")

	init = open("__init__.py", "w")
	init.write("""from flask import Flask\nfrom config import Config\n
app=Flask(__name__)\napp.config.from_object(Config)\n
from app import routes""")
	init.close()
	
	routes = open("routes.py", "w")
	routes.write("""from flask import render_template\n
from app import app\n
@app.route('/')
def index():\n\treturn render_template("index.html", title="home")""")
	routes.close()

	os.chdir("templates")

	base = open("base.html", "w")
	base.write("<!DOCTYPE html>\n<html>\n<head>\n{% if title %}" + f"<title>{app_name} - " + r"{{ title }}</title>\n" +
	"{% else %}" + f"<title>{app_name}</title>" + "{% endif %}\n</head>\n<body>\n<h1>Maybe put a navbar here</h1><hr>\n{% block content %}{% endblock %}\n<body>\n</html>") # This was horrible to write
	base.close()

	index = open(f"index.html", "w")
	index.write('{% extends "base.html" %}\n{% block content %}\n\t<h1>Home page</h1>\n{% endblock %}')

if __name__ == "__main__":
	create_app()