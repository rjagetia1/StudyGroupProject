# -------------------------------------------------------------------------------
# routes.py
# -------------------------------------------------------------------------------

from flask import render_template, request, make_response, redirect, url_for, session, send_from_directory, send_file

from studygroup import app, DEBUG
import studygroup.db as db