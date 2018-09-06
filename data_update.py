import vk
import data
import postgresql

db = postgresql.open(user=data.p_login, host=data.p_host, database=data.p_dbname, password=data.p_pass)
session = vk.AuthSession(data.appid, data.login, data.password)
vk_api = vk.API(session, v='5.84', lang='ru', timeout=10)
group_id = "-126351542"  # streampub id


def data_insert(post):
    insert_post_query = db.prepare("INSERT INTO posts VALUES ($1, to_timestamp($2), $3, $4, $5,"
                                   " $6, $7, $8, $9, $10, $11, $12)")
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
        attachments = ', '.join(att_types)  # video, photo, doc, link, audio, poll
    else:
        attachments = ""
    insert_post_query(post_id, date, post_type, text,
                      signer_id, attachments, comments,
                      likes, reposts, views, have_repost, marked_as_ads)


def data_update():
    get_last_id = db.prepare("SELECT id FROM posts ORDER BY id DESC LIMIT 1;")
    last_id = get_last_id()[0][0]
    wall = vk_api.wall.get(owner_id=group_id, count=50)['items']
    count = 0
    for post in wall:
        post_id = post['id']
        if int(post_id) <= int(last_id):
            break
        data_insert(post)
        count += 1
    return count


data_update()
