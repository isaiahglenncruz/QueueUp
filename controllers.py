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
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    profile_info = db(db.profiles.user == user_info.id).select().first()
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
        profile_info = profile_info,
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
        load_games_url = URL('load_games', signer=url_signer),
    )

@action('change_profile', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def change_profile():
    print("changing the profile apparently")
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    profile_info = db(db.profiles.user == user_info.id).select().first()
    auth_user_id = db.auth_user.update_or_insert(
        db.auth_user.email == get_user_email(),
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

@action('load_games')
@action.uses(url_signer.verify(), db)
def load_games():
    print("loading games for user")
    user_info = db(db.auth_user.email == get_user_email()).select().first()
    profile_info = db(db.profiles.user == user_info.id).select().first()
    rows = db(db.game_data.profile == profile_info.id).select().as_list()
    return dict(
        rows=rows,
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
    )

@action('add_lobby', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_lobby():
    r = db(db.auth_user.email == get_user_email()).select().first()
    lobby_leader = r.first_name + " " + r.last_name if r is not None else "Unknown"
    profile_info = db(db.profiles.user == r.id).select().first()
    # print("r_id is :", r.id)
    game_ = request.json.get('game')
    print("game is: ", game_)
    id = db.lobbies.insert(
        game = game_, # change to a field user can create in form
        leader = r.id, # get this with get_user probably
        bio = request.json.get('bio'),
        rank = request.json.get('rank'),
        region = request.json.get('region'),
        playstyle = request.json.get('playstyle'),
    )
    lob = db(db.lobbies.id == id).select().as_list()[0] #could this cause errors? not sure
    # print("lob evaluates to: ", lob)
    lob['show_url'] = URL('in_lobby', lob['id'], signer=url_signer)
    return dict(
        id=id,
        leader=lobby_leader,
        url=lob['show_url'],
    )

@action('load_lobbies')
@action.uses(auth.user, url_signer.verify() ,db) # removed url signer.verify
def load_lobbies():
    user = db(db.auth_user.email == get_user_email()).select().first() # curr user
    prof = db(db.profiles.user == user.id).select().first() # curr prof
    games = db(db.game_data.profile == prof.id).select().as_list()
    playable = [r['game'] for r in games]
    print("games is: ", games)
    print("playable is: ", playable, "of type", type(playable))

    ####################


    lobbies = db(db.lobbies).select().as_list()
    r_ = db(db.auth_user.email == get_user_email()).select().first()
    lobby_leader = r_.first_name + " " + r_.last_name if r_ is not None else "Unknown"
    # print("lobbies : ", lobbies)
    names = [lobby_leader]
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
        names = [r['leader'], r['player1'], r['player2'], r['player3'], r['player4']]
    print("names: ", names)
    return dict(lobbies=lobbies, playable=playable)

@action('get_players', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def get_players():
    print("------ get players --------")
    lobbies = db(db.lobbies).select().as_list()
    curr_id = request.json.get("id")
    curr_lob = db(db.lobbies.id == curr_id).select().first()
    # print("current lobby: ", curr_lob)
    # print("leader: ", curr_lob.leader)
    p0 = curr_lob.leader
    p1 = curr_lob.player1
    p2 = curr_lob.player2
    p3 = curr_lob.player3
    p4 = curr_lob.player4
    # print("allocation worked")
    member_ids = [p0, p1, p2, p3, p4]
    # print("members id: ", member_ids)
    misc = []

    for i in member_ids:
        # print("made it in loop")
        if i is not None:
            curr = db(db.profiles.id == i).select().first() # getting a profile
            user = db(db.auth_user.id == curr.user).select().first()
            name = user.first_name + " " + user.last_name if user is not None else "no name"
            # print("curr: ", curr)
            choose = db((db.game_data.profile == i) & (curr_lob.game == db.game_data.game)).select().first()
            # print("choose refers to: ", choose)
            # getting a rank from game_data
            d = {
                'tiltproof': curr.tiltproof,
                'leader': curr.leader,
                'fun': curr.fun,
                'communicative': curr.communicative,
                'mic': curr.mic,
                'rank': choose.rank,
                'gamertag': choose.gamertag,
                'name': name,
                'id': curr.id,
            }
            misc.append(d)
        else:
            d = {
                'tiltproof': 0,
                'leader': 0,
                'fun': 0,
                'communicative': 0,
                'mic': False,
                'rank': "",
                'gamertag': "",
                'name': '',
                'id': None,
            }
            misc.append(d) 
    # print("misc is: ", misc)
    return dict(misc=misc)

############################# IN LOBBY FUNCTIONS  ###########################

@action('in_lobby/<lobby_id:int>')
@action.uses(auth.user, url_signer, db, url_signer.verify(), 'in_lobby.html')
def in_lobby(lobby_id=None):
    print("in lobby page")
    lob = db(db.lobbies.id == lobby_id).select().first()
    r = db(db.auth_user.email == get_user_email()).select().first() # get curr user db
    profile_info = db(db.profiles.user == r.id).select().first() # get curr profile db
            

    # print("inserting: ", profile_info.id)
    if r.id == lob.leader:
        print("leader is joining pls do nothing else")
    elif lob.player1 == profile_info.id or lob.player2 == profile_info.id or lob.player3 == profile_info.id or lob.player4 == profile_info.id:
        print("other user in lobby please do nothing")
    elif lob.player1 is None:
        print("-- new player 1 -- ")
        db(db.lobbies.id == lobby_id).update(player1=profile_info.id)
    elif lob.player2 is None:
        print("-- new player 2 -- ")
        db(db.lobbies.id == lobby_id).update(player2=profile_info.id)
    elif lob.player3 is None:
        print("-- new player 3 -- ")
        db(db.lobbies.id == lobby_id).update(player3=profile_info.id)
    elif lob.player4 is None:
        print("-- new player 4 -- ")
        db(db.lobbies.id == lobby_id).update(player4=profile_info.id)
    else:
        print("LOBBY FULL CANNOT JOIN REMOVE BUTTON")
    # print("lob evaluates to: ", lob)
    return dict(
        load_messages_url = URL('load_messages', signer=url_signer),
        add_message_url = URL('add_message', signer=url_signer),
        get_players_url = URL('get_players', signer=url_signer),
        leave_lobby_url = URL('leave_lobby', signer=url_signer),
        close_lobby_url = URL('close_lobby', signer=url_signer),
        add_stats_url = URL('add_stats', signer=url_signer),
        back_to_main_url = URL('index'),
        curr_id = lobby_id,
        prof_id = profile_info.id,
        lead_id = lob.leader,
        # probably want to return url for post lobby page here
        # also want to implement a leave_lobby_url that moves pages maybe and removes from lobby
    )


@action('load_messages', method="POST")
@action.uses(url_signer.verify(), db)
def load_messages():
    lob_id = request.json.get('lob_id')
    messages = db(db.messages.lobby == lob_id).select().as_list() # this eventually needs to be for only messages in a given lobby
    return dict(messages=messages)

@action('add_message', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_message():
    r = db(db.auth_user.email == get_user_email()).select().first()
    name = r.first_name + " " + r.last_name if r is not None else "Unknown"
    print("extracted name is: ", name)
    # from the client side have them send the lobby id so we can acess that db
    id = db.messages.insert(
        message=request.json.get('message'),
        name=name,
        lobby=request.json.get('lob_id'),
        user=request.json.get('prof_id'),
        # add user reference
    )
    # eventually return the name of the user for html usage
    return dict(id=id, name=name)

@action('add_stats', method="POST")
@action.uses(auth.user, url_signer.verify(), db)
def add_stats():
    prof_id = request.json.get('prof_id')
    tilt = request.json.get('tilt')
    lead = request.json.get('lead')
    fun = request.json.get('fun')
    com = request.json.get('com')
    prof = db(db.profiles.id == prof_id).select().first()
    print("profile: is", prof)
    db(db.profiles.id == prof_id).update(tiltproof=tilt)
    db(db.profiles.id == prof_id).update(leader=lead)
    db(db.profiles.id == prof_id).update(fun=fun)
    db(db.profiles.id == prof_id).update(communicative=com)
    return "ok"

@action('leave_lobby')
@action.uses(url_signer.verify(), db, auth.user)
def leave_lobby():
    prof_id = request.params.get('prof_id')
    prof = db(db.profiles.id == prof_id).select().first() # return profile
    lob_id = request.params.get('lob_id')
    curr_lob = db(db.lobbies.id == lob_id).select().first() # should have current lobby
    print("prof_id: ", prof_id, "lob_id: ", lob_id)
    print("curr player1: ", curr_lob.player1)
    print("entire curr lob: ", curr_lob)
    print("result: ", curr_lob.player1 == prof.id)
    if curr_lob.player1 == prof.id:
        print("removed p1")
        db(db.lobbies.id == lob_id).update(player1=None)
    elif curr_lob.player2 == prof.id:
        print("removed p1")
        db(db.lobbies.id == lob_id).update(player2=None)
    elif curr_lob.player3 == prof.id:
        print("removed p1")
        db(db.lobbies.id == lob_id).update(player3=None)
    elif curr_lob.player4 == prof.id:
        print("removed p1")
        db(db.lobbies.id == lob_id).update(player4=None)
    return "ok"

@action('close_lobby')
@action.uses(url_signer.verify(), db, auth.user)
def close_lobby():
    prof_id = request.params.get('prof_id')
    prof = db(db.profiles.id == prof_id).select().first()
    lob_id = request.params.get('lob_id')
    curr_lob = db(db.lobbies.id == lob_id).select().first() # should have current lobby
    if curr_lob.leader == prof.id:
        db(db.lobbies.id == lob_id).delete()
    else:
        print("should not be closing lobby what is this")
    return "ok"
