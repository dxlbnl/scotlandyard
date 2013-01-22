
(function () {
    var server, api, game, next_player, board_def;
    server = connection.server;
    api = connection.api;

    game = {
        id : undefined,
        players : {}
    }

    api.game_created = function (game_id) {
        console.log("game created", game_id);

        server.game_register_player(game_id, 'mrX');
        server.game_register_player(game_id, 'detective');
        server.game_register_player(game_id, 'detective');
        server.game_register_player(game_id, 'detective');
        // server.game_register_player(game_id, 'detective');
        // server.game_register_player(game_id, 'detective');
        // server.game_register_player(game_id, 'detective');
        // server.game_register_player(game_id, 'detective');

        server.game_start(game_id);

        game.id = game_id;
    };
    api.player_registered = function (game_id, player_id, player_type) {
        console.log("Player registered", game_id, player_id, player_type);
        game.players[player_id] = {
            type : player_type,
            id : player_id
        }
    };
    api.game_state = function (state) {
        var colors = ["#DE1841", "#F5861A", "#F5DE1A", "#5DD517", "#1680CA", "#6016CA", "#F6451A", "#F6B41A", "#D6EB19", "#15CA7F", "#152ACA", "#CA16BD", "#FFFFFF"];
        console.log("Got state:", state)

        board.clear();

        // color mrX.
        board.color_stop(state.MrX.location, colors.pop());
        game.players[state.MrX.id].location = state.MrX.location;

        // color the detectives
        for (var i=0; i<state.detectives.length; i++) {
            board.color_stop(state.detectives[i].location, colors.pop());
            game.players[state.detectives[i].id].location = state.detectives[i].location;
        }
    };
    api.move.last_scaled = [];
    api.move = function (player_id) {
        var stop, scalestop, connected, transport, i;

        scalestop = function (id, scale) {board.setscale(board.getstop(id), scale);};

        // set the scale of the last next_player to 1.
        if (api.move.last_scaled) {
            for (i=0; i<api.move.last_scaled.length; i++)
            scalestop(api.move.last_scaled[i], 1);
        }
        api.move.last_scaled = [];

        // next click is the move.
        next_player = game.players[player_id];
        // current location
        scalestop(next_player.location, 2);
        api.move.last_scaled.push(next_player.location);

        console.log("Moving", player_id);  
        // finding connected locations.
        connected = board_def.connections[next_player.location];

        for (transport in connected) {
            for (i=0; i<connected[transport].length; i++) {
                api.move.last_scaled.push(connected[transport][i]);
                scalestop(connected[transport][i], 1.5);
                board.color_stop(connected[transport][i], "#CCCCCC");
            }
        }

        console.log("Connected::", connected);
    };
    api.set_board = function (b) {
        console.log("setting new board", b);

        board_def = b;
    };

    board.onclick = function (el) {
        var id, connections, transport;
        id = el.id;
        connections = board_def.connections[next_player.location];
        for (transport in connections) {
            if (connections[transport].indexOf(id) !== -1) {
                break;
            }
        }
        console.log(next_player.id, 'used', transport, 'to', id);
        server.player_moved(game.id, next_player.id, id, transport);
        board.setscale(el, 1);
    };


    server.onstart = function () {
        server.login("Hello world");
        server.create_game();

        server.list_games();


        server.send_board();
    };
    
}());
