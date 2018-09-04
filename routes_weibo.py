from utils import log
from utils import template
from utils import redirect
from utils import http_response

from models import User
from models import Tweet
from models import Comment

session = {}


def current_user(request):
    session_id = request.cookies.get('user', '')
    # log('session_id', session_id)
    user_id = int(session.get(session_id, '-1'))
    return user_id


def login_required(route_function):
    def func(request):
        # u = current_user(request)
        uid = current_user(request)
        log('user_id ', uid)
        # log('session in Tweet', session)
        if uid == -1:
            return redirect('/login')
        else:
            return route_function(request)
    return func


def index(request):
    tweets = Tweet.all()
    user = User
    body = template('tweet_index.html', tweets=tweets, User=User)
    return http_response(body)


def route_add(request):
    form = request.form()
    t = Tweet(form)
    t.user_id = int(current_user(request))
    t.save()
    return redirect('/')


def route_edit(request):
    id = int(request.query.get('id', -1))
    t = Tweet.find_by(id=id)
    body = template('tweet_edit.html', t=t)
    return http_response(body)


def route_update(request):
    id = int(request.query.get('id', -1))
    t = Tweet.find_by(id=id)
    form = request.form()
    t.content = form.get('content', '')
    t.save()
    return redirect('/')

def route_delete(request):
    id = int(request.query.get('id', -1))
    Tweet.delete(id)
    return redirect('/')




def route_comment(request):
    id = int(request.query.get('id', -1))
    body = template('tweet_comment.html', id=id)
    return http_response(body)

def route_comment_add(request):
    t_id = int(request.query.get('id', -1))
    form = request.form()
    c = Comment(form)
    c.user_id = current_user(request)
    c.tweet_id = t_id
    c.save()
    return redirect('/')


route_dict = {
    '/': login_required(index),
    '/add': login_required(route_add),
    '/edit': login_required(route_edit),
    '/comment': login_required(route_comment),
    '/update': login_required(route_update),
    '/delete': login_required(route_delete),
    '/comment/add': login_required(route_comment_add),
}