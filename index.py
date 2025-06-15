from flask import Flask, request, jsonify
from views import views
app = Flask(__name__, static_folder="static", template_folder="templates")

app.register_blueprint(views, url_prefix='/')


if __name__ == '__main__':
    app.run()
