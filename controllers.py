"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses(auth.user, url_signer, db, 'index.html')
def index():
    print("looking good so far")
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

@action('lobbies')
@action.uses(auth.user, db, 'lobbies.html')
def lobbies():
    print("lobby page reached")
    return dict(
        # URLS used for callbacks and HTTP requests
        add_lobby_url = URL('add_lobby', signer=url_signer),
        load_lobbies_url = URL('load_lobbies', signer=url_signer)
    )

@action('add_lobby', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_lobby():
    r = db(db.auth_user.email == get_user_email()).select().first()
    lobby_leader = r.first_name + " " + r.last_name if r is not None else "Unknown"
    members = ["player1", "player2", "player3", "player4"]
    id = db.lobbies.insert(
        game = "Valorant",
        leader = lobby_leader, # get this with get_user probably
        bio = request.json.get('bio'),
        rank = request.json.get('rank'),
        region = request.json.get('region'),
        playstyle = request.json.get('playstyle'),
        player1 = "available",
        player2 = "available",
        player3 = "available",
        player4 = "available",
    )
    lob = db(db.lobbies.id == id).select().as_list()[0] #could this cause errors? not sure
    print("lob evaluates to: ", lob)
    lob['show_url'] = URL('in_lobby', lob['id'], signer=url_signer)
    return dict(
        id=id,
        leader=lobby_leader,
        url=lob['show_url'],
    )

@action('load_lobbies')
@action.uses(url_signer.verify(), db)
def load_lobbies():
    lobbies = db(db.lobbies).select().as_list()
    for r in lobbies:
        r['show_url'] = URL('in_lobby', r['id'], signer=url_signer)
    return dict(lobbies=lobbies)

@action('in_lobby/<lobby_id:int>')
@action.uses(auth.user, url_signer, db, url_signer.verify(), 'in_lobby.html')
def in_lobby(lobby_id=None):
    print("in lobby page")
    lob = db(db.lobbies.id == lobby_id).select().first()
    # print("lob evaluates to: ", lob)
    return dict(
        load_messages_url = URL('load_messages', signer=url_signer),
        add_message_url = URL('add_message', signer=url_signer),
        # probably want to return url for post lobby page here
        # also want to implement a leave_lobby_url that moves pages maybe and removes from lobby
    )

@action('load_messages')
@action.uses(url_signer.verify(), db)
def load_messages():
    messages = db(db.messages).select().as_list() # this eventually needs to be for only messages in a given lobby
    return dict(messages=messages)

@action('add_message', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_message():
    r = db(db.auth_user.email == get_user_email()).select().first()
    name = r.first_name + " " + r.last_name if r is not None else "Unknown"
    print("extracted name is: ", name)
    id = db.messages.insert(
        message=request.json.get('message'),
        name=name,
        # add lobby id
        # add user reference
    )
    # eventually return the name of the user for html usage
    return dict(id=id, name=name)