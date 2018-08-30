import vk
import data
from flask import Flask, render_template
app = Flask(__name__)

session = vk.AuthSession(data.appid, data.login, data.password)
vk_api = vk.API(session, v='5.35', lang='ru', timeout=10)

group_id = "-169050615"  # timenudge id


@app.route('/')
def index():
    result = vk_api.wall.get(owner_id=group_id, count=10)
    print(result)
    return render_template("index.html")


@app.route('/main')
def main():
    return 'Main!'
