import vk_api
import data
from flask import Flask, render_template
app = Flask(__name__)
vk = vk_api.VkApi(data.login, data.password)
vk.auth()

group_id = "-169050615"  # timenudge id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/main')
def main():
    return 'Main!'
