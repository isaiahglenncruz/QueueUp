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
        change_first_name: "",
        change_first_name_status: false,
        change_last_name: "",
        change_last_name_status: false,
        change_region: "",
        change_region_status: false,
        mic: "",
        change_mic_status: false,
        add_bio: "",
        add_bio_status: false,
        rows: [],
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
            first_name: app.vue.change_first_name,
            last_name: app.vue.change_last_name,
            region: app.vue.change_region,
            mic: app.vue.mic,
            bio: app.vue.add_bio,
        }).then(function (response) {
        app.vue.profile.push({
            id: response.data.id,
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

    app.set_add_bio_status = function (new_status) {
        app.vue.add_bio_status = new_status;
    };

    app.set_first_name_status = function (new_status) {
        app.vue.change_first_name_status = new_status;
    };

    app.set_last_name_status = function (new_status) {
        app.vue.change_last_name_status = new_status;
    };

    app.set_region_status = function (new_status) {
        app.vue.change_region_status = new_status;
    };

    app.set_mic_status = function (new_status) {
        app.vue.change_mic_status = new_status;
    };


    app.add_game = function () {
        console.log("adding a game");
        axios.post(add_game_url, {
            game: app.vue.add_game_name,
            gamertag: app.vue.add_gamertag,
            rank: app.vue.add_game_rank,
        }).then(function (response) {
        app.vue.rows.push({
            id: response.data.id,
            game: app.vue.add_game_name,
            gamertag: app.vue.add_gamertag,
            rank: app.vue.add_game_rank,
        });
            app.enumerate(app.vue.rows);
        });
        app.set_add_game_status(false);
        app.delete_dupe(app.vue.add_game_name);
    };

    app.delete_dupe = function (game) {
        for (let i = 0; i < app.vue.rows.length; i++) {
            if (app.vue.rows[i].game == game) {
                app.vue.rows.splice(i, 1);
                app.enumerate(app.vue.rows);
                break;
            }
        }
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        change_profile: app.change_profile,
        set_add_game_status: app.set_add_game_status,
        set_add_bio_status: app.set_add_bio_status,
        set_first_name_status: app.set_first_name_status,
        set_last_name_status: app.set_last_name_status,
        set_region_status: app.set_region_status,
        set_mic_status: app.set_mic_status,
        add_game: app.add_game,
        delete_dupe: app.delete_dupe,
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
        axios.get(load_games_url).then((result) => {
            let rows = result.data.rows;
            app.enumerate(rows);
            app.vue.rows = rows;
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);