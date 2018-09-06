import vk
import data
import time
# from flask import Flask, render_template
import postgresql

# app = Flask(__name__)
db = postgresql.open(user=data.p_login, host=data.p_host, database=data.p_dbname, password=data.p_pass)
session = vk.AuthSession(data.appid, data.login, data.password)
vk_api = vk.API(session, v='5.84', lang='ru', timeout=10)
group_id = "-126351542"  # streampub id


def data_update():
    values = "INSERT INTO posts VALUES ($1, to_timestamp($2), $3, $4, $5," \
             " $6, $7, $8, $9, $10, $11, $12)"
    set_table = db.prepare(values)
    search_id = 13783
    offset = 0
    while True:
        cur_wall = vk_api.wall.get(owner_id=group_id, count=100, offset=offset)
        cur_wall = cur_wall['items']
        for post in cur_wall:
            post_id = post['id']
            date = post['date']
            marked_as_ads = post['marked_as_ads']
            have_repost = False if hasattr(post, 'copy_history') else True
            post_type = post['post_type']
            text = post['text'].replace("'", r"''")
            signer_id = post['signer_id'] if hasattr(post, 'signer_id') else 0
            comments = post['comments']['count']
            likes = post['likes']['count']
            reposts = post['reposts']['count']
            views = post['views']['count']
            att_types = []
            if hasattr(post, 'attachments'):
                for att in post['attachments']:
                    if att_types.count(att['type']) == 0:
                        att_types.append(att['type'])
                attachments = ', '.join(att_types)          # video, photo, doc, link, audio, poll
            else:
                attachments = ""
            set_table(post_id, date, post_type, text,
                      signer_id, attachments, comments,
                      likes, reposts, views, have_repost, marked_as_ads)
            if post_id == search_id:
                return
        offset += 100
        time.sleep(0.5)


# del_table = db.prepare("DELETE FROM posts")
# print(del_table())
# data_update()
get_table = db.prepare("SELECT * FROM posts")
print(get_table())

# @app.route('/')
# def index():
#
#
#     return render_template("index.html")
#
#
# @app.route('/main')
# def main():
#     return 'Main!'
