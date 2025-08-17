# errors.py
import os

from flask import Blueprint, render_template

css_dir = 'static/css'

def get_css_links():
    """Generates a list of paths to all CSS files in the static/css directory."""
    css_files = []
    for root, dirs, files in os.walk(css_dir):
        for file in files:
            if file.endswith(".css"):
                # Construct the relative path for the file within the static folder
                file_path = os.path.join(root, file).replace('\\', '/')
                file_path = file_path.replace('static/', '')  # Remove 'static/' from the path
                css_files.append(file_path)
    return css_files

# Create blueprint for error handling
errors = Blueprint('errors', __name__,template_folder='../templates', static_folder='../static')

# Handle 404 errors (Page not found)
@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/error.html',
                           css=get_css_links(),
                           error_code=404,
                           error_message="Page Not Found",
                           error_description="The page you are looking for does not exist."), 404

# Handle 500 errors (Internal server error)
@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/error.html',
                           css=get_css_links(),
                           error_code=500,
                           error_message="Internal Server Error",
                           error_description="An unexpected error occurred on the server."), 500

# Handle 401 errors (Unauthorized)
@errors.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/error.html',
                           css=get_css_links(),
                           error_code=401,
                           error_message="Unauthorized",
                           error_description="You are not authorized to view this page."), 401

# Handle 403 errors (Forbidden)
@errors.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/error.html',
                           css=get_css_links(),
                           error_code=403,
                           error_message="Forbidden",
                           error_description="You do not have permission to access this resource."), 403

# Handle other errors generically
@errors.app_errorhandler(Exception)
def handle_http_exception(error):
    error_code = getattr(error, 'code', 500)
    error_message = getattr(error, 'name', 'Unknown Error')
    error_description = str(error)
    return render_template('errors/error.html',
                           css=get_css_links(),
                           error_code=error_code,
                           error_message=error_message,
                           error_description=error_description), error_code
