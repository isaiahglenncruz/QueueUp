// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_new_lobby: false,
        add_rank: "",      // Should be grabbed by default soon
        add_region: "",     // Should be grabbed by default soon
        add_playstyle:  "", 
        add_bio: "",
        lobbies: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.reset_form = function () {
        app.vue.add_rank = "";
        app.vue.add_region = "";
        app.vue.add_playstyle = "";
        app.vue.add_bio = "";
    };

    app.complete = (lobbies) => {
        lobbies.map((lob) => {
            console.log(lob);
            //lob.leader = "no leader";
            // lob.player1 = "available";
            // lob.player2 = "available";
            // lob.player3 = "available";
            // lob.player4 = "available";
        })
    }

    app.set_add_status = function (new_status) {
        app.vue.add_new_lobby = new_status;
    }

    app.add_lobby = function () {
        // submit form data to server
        
        axios.post(add_lobby_url, {
            rank: app.vue.add_rank,
            region: app.vue.add_region,
            playstyle: app.vue.add_playstyle,
            bio: app.vue.add_bio,
        }).then(function (response) {
        console.log(response.data.leader);
        app.vue.lobbies.push({
            // add attributes from server to local array
            id: response.data.id,
            leader: response.data.leader,
            show_url: response.data.url,
            rank: app.vue.add_rank,
            region: app.vue.add_region,
            playstyle: app.vue.add_playstyle,
            bio: app.vue.add_bio,
        });
            app.enumerate(app.vue.lobbies);
            app.reset_form();
            app.set_add_status(false);
            // jump to in lobby page here
            var last = app.vue.lobbies[app.vue.lobbies.length -1]
            console.log("last : ", last.show_url)
            let a = document.createElement('a');
            a.href = last.show_url;
            a.click();
        });
        
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_lobby: app.add_lobby,
        set_add_status: app.set_add_status,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Typically this is a server GET call to load the data.
        axios.get(load_lobbies_url).then(function (response) {
            let lobbies = response.data.lobbies;
            app.enumerate(lobbies);
            app.complete(lobbies);
            app.vue.lobbies = lobbies;
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
