// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_game_status: false,
        add_game_name: "",
        add_gamertag: "",
        add_game_rank: "",
        change_email: "",
        change_first_name: "",
        change_last_name: "",
        change_region: "",
        mic: "",
        add_bio: "",
        profile: [],
        game_data: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.change_profile = function () {
        console.log("changing profile");
        axios.post(change_profile_url, {
            email: app.vue.change_email,
            first_name: app.vue.change_first_name,
            last_name: app.vue.change_last_name,
            region: app.vue.change_region,
            mic: app.vue.mic,
            bio: app.vue.add_bio,
        }).then(function (response) {
        app.vue.profile.push({
            id: response.data.id,
            email: app.vue.change_email,
            first_name: app.vue.change_first_name,
            last_name: app.vue.change_last_name,
            region: app.vue.change_region,
            mic: app.vue.mic,
            bio: app.vue.add_bio,
        });
            app.enumerate(app.vue.profile);
        });
    };

    app.set_add_game_status = function (new_status) {
        app.vue.add_game_status = new_status;
    };

    app.add_game = function () {
        console.log("adding a game");
        axios.post(add_game_url, {
            game: app.vue.add_game_name,
            gamertag: app.vue.add_gamertag,
            rank: app.vue.add_game_rank,
        }).then(function (response) {
        app.vue.game_data.push({
            id: response.data.id,
            game: app.vue.add_game_name,
            gamertag: app.vue.add_gamertag,
            rank: app.vue.add_game_rank,
        });
            app.enumerate(app.vue.game_data);
        });
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        change_profile: app.change_profile,
        set_add_game_status: app.set_add_game_status,
        add_game: app.add_game,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);