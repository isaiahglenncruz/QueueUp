![QueueUp](https://drive.google.com/thumbnail?id=1ijZHvfT_vnazSPr7pKlxmTGpYO3KoMxQ)

# Motive
After too many nights of losing with friends, or raging at random teammates who tested our
patience and made us question our will to play, we decided there needs to be a better way
to find teammates to play games with. We wanted a space where you meet other gamers with
similar intentions and take the frustration of randomly assigned incompatable teammates away.  
So we built QueueUp.

# Instructions To Run
To use this application, first follow the link [here](https://github.com/web2py/py4web) and follow the instructions
to install py4web. Once that is downloaded and configured, you can simply download or clone QueueUp, and plce it in the
"apps" directory. From there, run the following in your terminal in the py4web directory:

#### For Linux/MacOS
```bash
./py4web.py run apps
```
#### For Windows
```bash
python ./py4web.py run apps
```

Finally, open the link it presents in your favorite browser, enter your password, and run the QueueUp app.

# Notes on Running and Installation
After the steps mentioned above QueueUp can be run with no other dependencies, non-standard modules, 
or extra setup and installation steps. After hours of mutlitple attempts, we were sadly not able to
deploy our app to Google Appengine and Google Cloud SQL before the project deadline. Thus, it can be run locally 
with the previous steps only for now, but hopefully in the future we can put this website out there, make changes
and additions, and host our very first website. 

# App Flow
The general flow of the app is as follows:

1. Open the index page and follow the prompts to register
2. Fill out the required additional profile information before you can join or create a lobby
    - Include information like region, a bio, do you have a microphone to talk in game?
    - After this is completed, add games to the right to be able to join those games in the lobby page
3. Navigate to the lobby page and either join a lobby or create your own! Creating one will prompt you with the following:
    - The game the lobby revolves around -- where you will end up!
    - The rough rank you wish to play with (what others will see before joining)
    - The region you're in or want to others to be in to play
    - Playstyle you're looking for (casual? competive? etc)
    - A short bio to show other users before joining your lobby
4. Communicate with teammates in the lobby page
    - Users in a lobby will see some extra information about each other, and will have a chat available
    - This chat updates automatically!
    - Here you can really decide if you'd like to play with the other people in your lobby
    - You can also see their ratings from previous users to give a hint of their behavior
    - If so, when you've finally gathered the right amount of people, you can instruct each other to join on the game itself
    - Each users real in game gamertag should be listed in the lobby page for ease transition
    - You will also see if other users have mics, helping you play with others with mics if you're hoping to talk
5. When you're done, or impreressed, leave a rating!
    - Each user has four associated elo fields
        - tiltproof: if the user is calm and composed, give them a bump on this field!
        - leadership: if the user is instructive and a natural leader, give them a bump on this field!
        - fun: did you enjoy playing with this person? were they funny? give them a bump on this field!
        - communicative: did the user communicate with you, with or without a mic? give them a bump on this field!
6. Finally, leave the lobby when your session is done
    - Please ensure the members of the lobby leave first! This will make it easier for the lobby creater to terminate the lobby so others are not mislead
    - Each user can leave individually, and when gone, the leader can close the lobby, and get back to the rest of their day!
7. Next time you're looking for people to play with, make your way back to the lobby page!

# Implementation
Our implementations revolves around a few pages, centered around lobby interaction, and uses 4 databases in the process

## Databases

We have a profiles database that contains a reference to auth_user to keep py4web happy, and then the rest of the basic profile info we felt was key to core of the website. This information is filled when the user navigates to "edit profile", hence why we make it mandatory before finding lobbies to join

Second, we have a game data table, which contains game specific information that is ultimately tied to a profile. This is crucial because we wan the information in each lobby to reflect the real game! This way users can store different information for each game they play, and update it easily in one place. Not everybody has the same rank or name across the games they play.

Most crucially, we have a lobbies data table which acts as a storage contianer for users, and some personal state data. Each lobby is tied to a game, and the leader who created the lobby. From there, the leader fills the initial information, and the lobby can "hold" new users by storing their reference in players one through four. These players fields are updated frequently because users are free to hop between lobbies as they wish, but we ask for leaders to stay in their own lobby until all users have left, upon which they can close the lobby for good.

Finally, we have the messages database, which simply stores all the chat messages sent amongst all the lobbies. Of course we do not want to display messages in incorrect lobbies, so we store the lobby they were sent in, and query with this data when shipping data to the client. 

## Controller Functions 

The mitochondria of our app is the controllers.py file which contains all of our server side python functions that serve requets, load pages, and interact with the databases. Here is a brief explanation of each "segment" of our controllers.py.

### Profile and Index
Users need somewhere to land when they open our app, so the index controller services our home page, and does little more.

The following 4 controller functions are for editing profiles. The first services the actual html page for editing the profiles, and provides the URLs for the next three functions which do not service an HTML file. These functions are to edit elementary profile information, add game data, and load the game data to be displayed to the user.

### Viewing Lobbies
The bulk of our controlling goes in this chunk of functions. The lobbies controller mimics index, and serves the lobbies.html page which displays all of our lobbies. To add a lobby, the form users fill is sent to the add_lobby controller which reads in the json data from the axios request, and fills the lobbies database accordingly.

 To display these new lobbies, the next controller function load_lobbies returns two arrays that are passed to the client. The first is a represenatation of the lobbies database, except it replaces each profile reference with the name of the profile, so the client knows what to display on the screen. It also returns an array of games that the current logged in user has signed up for, so that it can limit the user to joining and creating lobbies for games it has already added to its database. 

 ### In Lobby Function
The next logical progression from viewing lobbies is joining them! We have a function get_players which provides a similar functionality to load_lobbies. The in lobby page requires some more specific information about each user, so we provide it this infomration from this junction. This includes things like game specific data, microphone status, and more.

The in_lobby function loads the html page, and because it is the function that leads users to the in lobby page, it also handles actually adding them into the lobby. Other than this, it just returns a plethora of data other in_lobby functions will need like URLs and current lobby, profile, and leader ids. 

### Messaging, Ratings
The next few functions are used to interact with the client to add messages to the messages table, and update ratings of users by other users. Each are rather simple, and do little more than addiding to or updating the database, and sending the correct messages back to the client

### Leaving
Finally, we don't want users to be stuck in an abyss, so we serviced leaving lobbies by removing them from the database and sending them back to the index page, though that step is done by the client. **Importantly, we really emphasize that lobby leaders should allow all users to leave the lobby before closing it, so the others do not run into problems.** Once lobby leaders remove a lobby, it is gone for good, and they are welcome to create a new one on the next occasion they want to play!

## Client Side
We have three pages that involve reactivity and Vue.js. The first is the edit profiles page, which handles toggling many different fields, displaying user information as they change it, and creating forms for our databases. 

The second page is to display the lobbies, which retrieves the array of lobbies from the server, and displays them along with their information. This page will not upate automatically, so in order to see more lobbies users should refresh the page.

Lastly, and the most reactive page, is the in lobby page. This page uses a simple but clever setInterval for loading the users of the lobby and the messages so that users can emulate a real time chat without the need for sockets or a persistent connection! There may be a better way to implement this, but for our purpose this works just fine. This client side page also handles the ratings of each user, and whenever they are updated it sends them to the server so it can update its databases. 
