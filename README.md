QueueUp: ![QueueUp](https://drive.google.com/thumbnail?id=1ijZHvfT_vnazSPr7pKlxmTGpYO3KoMxQ)

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
    Include information like region, a bio, do you have a microphone to talk in game?
    After this is completed, add games to the right to be able to join those games in the lobby page
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

