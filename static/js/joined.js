// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        message: "",
        messages: [],
        misc: [], // think should be a hash -- look into in java
        leader_id: lead_id,
        profile_id: prof_id,
        // user 1: {name: ___ rank: ___ attribute: ___ att2: ___}
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.add_message = function () {
        // TODO;
        axios.post(add_message_url, {
            message: app.vue.message,
            lob_id: curr_id,
            prof_id: prof_id,
        }).then(function (response) {
            app.vue.messages.push({
                id: response.data.id,
                message: app.vue.message,
                name: response.data.name,
                // eventually should have name of user who sent message here
            });
            app.enumerate(app.vue.messages);
            app.reset_form();
        })
    };

    app.reset_form = function () {
        app.vue.message = "";
    };

    app.leave_lobby = function () {
        // prof_id is the profile to remove
        console.log("IN LEAVE LOBBY FUNCTION");
        console.log("prof id: ", prof_id, "lob_id :", curr_id)
        axios.get(leave_lobby_url, {params: {prof_id: prof_id, lob_id: curr_id}}).then(function (response){
            console.log("removed user");
            let a = document.createElement('a');
            a.href = back_to_main_url;
            a.click();
        });
        // leave page or go back to view lobbies page
    }

    app.close_lobby = function () {
        console.log("closing lobby!");
        // implement close lobby in controller 
        axios.get(close_lobby_url, {params: {prof_id: prof_id, lob_id: curr_id}}).then(function (response){
            console.log("deleted lobby");
            let a = document.createElement('a');
            a.href = back_to_main_url;
            a.click();
        });
    }

    app.inc_tp = function(ind) {
        let memb = app.vue.misc[ind];
        if(memb.id == null) return;
        console.log(memb);
        memb.tiltproof += 1;
        axios.post(add_stats_url, {
            prof_id: memb.id,
            tilt: memb.tiltproof,
            lead: memb.leader, 
            fun: memb.fun,
            com: memb.communicative,
        }).then(function (response) {
            app.enumerate(app.vue.misc);
        });
    }

    app.inc_lead = function(ind) {
        let memb = app.vue.misc[ind];
        if(memb.id == null) return;
        console.log(memb);
        memb.leader += 1;
        axios.post(add_stats_url, {
            prof_id: memb.id,
            tilt: memb.tiltproof,
            lead: memb.leader, 
            fun: memb.fun,
            com: memb.communicative,
        }).then(function (response) {
            app.enumerate(app.vue.misc);
        });
    }

    app.inc_fun = function(ind) {
        let memb = app.vue.misc[ind];
        if(memb.id == null) return;
        console.log(memb);
        memb.fun += 1;
        axios.post(add_stats_url, {
            prof_id: memb.id,
            tilt: memb.tiltproof,
            lead: memb.leader, 
            fun: memb.fun,
            com: memb.communicative,
        }).then(function (response) {
            app.enumerate(app.vue.misc);
        });
    }

    app.inc_com = function(ind) {
        let memb = app.vue.misc[ind];
        if(memb.id == null) return;
        console.log(memb);
        memb.communicative += 1;
        axios.post(add_stats_url, {
            prof_id: memb.id,
            tilt: memb.tiltproof,
            lead: memb.leader, 
            fun: memb.fun,
            com: memb.communicative,
        }).then(function (response) {
            app.enumerate(app.vue.misc);
        });
    }


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_message: app.add_message,
        leave_lobby: app.leave_lobby,
        close_lobby: app.close_lobby,
        inc_tp: app.inc_tp,
        inc_lead: app.inc_lead,
        inc_fun: app.inc_fun,
        inc_com: app.inc_com,
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
        setInterval(() => {
            axios.post(load_messages_url, {
                lob_id: curr_id,
            }).then(function (response){
                let messages = response.data.messages;
                app.enumerate(messages);
                // could have complete function here for init values of things
                app.vue.messages = messages;
            });

            axios.post(get_players_url, {
                id: curr_id,
            }).then(function (response) {
                let misc = response.data.misc;
                app.enumerate(misc);
                app.vue.misc = misc;
            });
        }, 2000);
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);