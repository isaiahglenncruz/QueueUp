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

############################# HOME AND PROFILE FUNCTIONS ###########################
@action('index')
@action.uses(auth.user, url_signer, db, 'index.html')
def index():
    print("looking good so far")
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

@action('profile')
@action.uses(auth.user, url_signer, db, 'profile.html')
def profile():
    print("profile page reached")
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    
    if not db(db.profiles.user == user_info.id).select().first():
        db.profiles.insert(
            user=user_info.id,
            region=db.profiles.region.default,
            bio=db.profiles.bio.default,
            mic=db.profiles.mic.default,
            tiltproof=db.profiles.tiltproof.default,
            leader=db.profiles.leader.default,
            fun=db.profiles.fun.default,
            communicative=db.profiles.communicative.default,
            )      
    
    profile_info = db(db.profiles.user == user_info.id).select().first()

    return dict(
        user_info=user_info,
        profile_info=profile_info,
        change_profile_url = URL('change_profile', signer=url_signer),
        add_game_url = URL('add_game', signer=url_signer),
    )

@action('change_profile', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def change_profile():
    print("changing the profile apparently")
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    profile_info = db(db.profiles.user == user_info.id).select().first()
    auth_user_id = db.auth_user.update_or_insert(
        db.auth_user.email == get_user_email(),
        email = request.json.get('email') if request.json.get('email') != "" else user_info.email,
        first_name = request.json.get('first_name') if request.json.get('first_name') != "" else user_info.first_name,
        last_name = request.json.get('last_name') if request.json.get('last_name') != "" else user_info.last_name,
    )
    profile_id = db.profiles.update_or_insert(
        db.profiles.user == user_info.id,
        region = request.json.get('region') if request.json.get('region') != "" else profile_info.region,
        bio = request.json.get('bio') if request.json.get('bio') != "" else profile_info.bio,
        mic = request.json.get('mic') if request.json.get('mic') is not None else profile_info.mic,
    )
    return dict(
        auth_user_id=auth_user_id,
        profile_id=profile_id,
    )

@action('add_game', method="POST")
@action.uses(db, auth.user, url_signer.verify())
def add_game():
    print("adding some game data")
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    profile_info = db(db.profiles.user == user_info.id).select().first()
    game_to_add = request.json.get('game')
    print(game_to_add)

    game_data = db.game_data.update_or_insert(
        (db.game_data.profile == profile_info.id) & (db.game_data.game == game_to_add),
        profile = profile_info.id,
        game = game_to_add,
        gamertag = request.json.get('gamertag'),
        rank = request.json.get('rank'),
    )

    return dict(
        game_data=game_data,
    )

############################# BEGINNING OF LOBBY FUNCTIONS ###########################

@action('lobbies')
@action.uses(auth.user, db, 'lobbies.html')
def lobbies():
    print("lobby page reached")
    return dict(
        # URLS used for callbacks and HTTP requests
        add_lobby_url = URL('add_lobby', signer=url_signer),
        load_lobbies_url = URL('load_lobbies', signer=url_signer),
        get_players_url = URL('get_players', signer=url_signer),
    )

@action('add_lobby', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_lobby():
    r = db(db.auth_user.email == get_user_email()).select().first()
    lobby_leader = r.first_name + " " + r.last_name if r is not None else "Unknown"
    profile_info = db(db.profiles.user == r.id).select().first()
    print("r_id is :", r.id)
    id = db.lobbies.insert(
        game = "Valorant",
        leader = r.id, # get this with get_user probably
        bio = request.json.get('bio'),
        rank = request.json.get('rank'),
        region = request.json.get('region'),
        playstyle = request.json.get('playstyle'),
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
    r = db(db.auth_user.email == get_user_email()).select().first()
    lobby_leader = r.first_name + " " + r.last_name if r is not None else "Unknown"
    print("lobbies : ", lobbies)
    for r in lobbies:
        r['show_url'] = URL('in_lobby', r['id'], signer=url_signer)
        lead_id = r['leader']
        lead_user = db(db.auth_user.id == lead_id).select().first()
        lead_name = lead_user.first_name + " " + lead_user.last_name if lead_user is not None else "Unknown"
        r['leader'] = lead_name
        if r['player1']:
            curr = r['player1']
            prof = db(db.profiles.id == curr).select().first()
            user = db(db.auth_user.id == prof.user).select().first()
            name = user.first_name + " " + user.last_name if user is not None else "available"
            print("name extracted is 1: ", name)
            r['player1'] = name
        if r['player2']:
            curr = r['player2']
            prof = db(db.profiles.id == curr).select().first()
            user = db(db.auth_user.id == prof.user).select().first()
            name = user.first_name + " " + user.last_name if user is not None else "available"
            print("name extracted is 2: ", name)
            r['player2'] = name
        if r['player3']:
            curr = r['player3']
            prof = db(db.profiles.id == curr).select().first()
            user = db(db.auth_user.id == prof.user).select().first()
            name = user.first_name + " " + user.last_name if user is not None else "available"
            print("name extracted is 3: ", name)
            r['player3'] = name
        if r['player4']:
            curr = r['player4']
            prof = db(db.profiles.id == curr).select().first()
            user = db(db.auth_user.id == prof.user).select().first()
            name = user.first_name + " " + user.last_name if user is not None else "available"
            print("name extracted is: ", name)
            r['player4'] = name
    return dict(lobbies=lobbies)

# @action('get_players')
# @action.uses(url_signer.verify(), db)
# def get_players():
#     lobbies = db(db.lobbies).select().as_list()
#     return dict()

############################# IN LOBBY FUNCTIONS  ###########################

@action('in_lobby/<lobby_id:int>')
@action.uses(auth.user, url_signer, db, url_signer.verify(), 'in_lobby.html')
def in_lobby(lobby_id=None):
    print("in lobby page")
    lob = db(db.lobbies.id == lobby_id).select().first()
    r = db(db.auth_user.email == get_user_email()).select().first() # get curr user db
    profile_info = db(db.profiles.user == r.id).select().first() # get curr profile db

    print("inserting: ", profile_info.id)
    if r.id == lob.leader:
        print("leader is joining pls do nothing else")
    elif lob.player1 is None:
        db(db.lobbies.id == lobby_id).update(player1=profile_info.id)
    elif lob.player2 is None:
        db(db.lobbies.id == lobby_id).update(player2=profile_info.id)
    elif lob.player3 is None:
        db(db.lobbies.id == lobby_id).update(player3=profile_info.id)
    elif lob.player4 is None:
        db(db.lobbies.id == lobby_id).update(player4=profile_info.id)
    else:
        print("LOBBY FULL CANNOT JOIN REMOVE BUTTON")
    print("lob evaluates to: ", lob)
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