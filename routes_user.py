from utils import log
from utils import template
from utils import redirect
from utils import http_response

from routes_weibo import session as session

from models import User

import random


def random_str():
    seed = 'jfqueuxnhard'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def route_login(request):
    """
    登录页面
    """
    headers = {}
    log('login, cookies', request.cookies)

    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            # 设置 session
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            log('headers response', headers)
            log('session', session)
            # 登录后定向到 /
            return redirect('/', headers)
    # 显示登录页面
    body = template('login.html')
    return http_response(body, headers=headers)


def route_register(request):
    """
    注册页面
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            # on success
            return redirect('/login')
        else:
            # if failed
            return redirect('/register')
    body = template('register.html')
    return http_response(body)


route_dict = {
    '/login': route_login,
    '/register': route_register,
}
