
var connection = (function () {
    var ws, apidef, api, server;

    apidef =  {
        'game_state': ['state'], 
        'raise_error': ['msg'], 
        'after_login': ['status'], 
        'player_registered': ['game_id', 'player_id', 'player_type'], 
        'register_player': ['player_type'], 
        'game_created': ['game_id'], 
        'login': ['api_token'], 
        'games_list': ['games_list'],
        'set_api':['api'],
        'move':['player_id'],
        'set_board':['board'],
    }

    api = {};

    for (var method in apidef) {
        api[method] = (function (method) {
            return function (data) {
                console.log("calling", method, data);
            }
        }(method));
    }

    api.set_api = function (api) {
        console.log("setting api", api);

        for (method in api) {
            server[method] = (function (method, arg_names) {
                return function () {
                    var args, kwargs;
                    // turn args into kwargs
                    args = Array.prototype.slice.call(arguments);

                    kwargs = {};
                    for (i=0; i<args.length; i++) {
                        kwargs[arg_names[i]] = args[i];
                    }
                    kwargs.method = method;
                    console.log('calling', method, kwargs);

                    ws.send(JSON.stringify(kwargs) + "\0");
                    
                };
            }(method, api[method]));
        }
        server.onstart();

    };

    ws = new WebSocket('ws://dxtr.be:8888', 'binary');

    reader_onloadend = function (e) {
        var json_strings, method, data, args, i, j, key;

        // this might not be the complete message, if there is no terminator string, we've got to wait.
        if (/\0/.test(e.target.result)) {
            json_strings = reader_onloadend.__queue.join('');
            reader_onloadend.__queue = []; // empty the queue

            json_strings += e.target.result;
            json_strings = json_strings.split('\0'); // empty the queue and split on the terminators
            for (i=0; i<json_strings.length; i++) {
                if (json_strings[i]) {

                    data = JSON.parse(json_strings[i]);

                    method = data.method;
                    delete data.method;

                    args = [];
                    for (j=0; j<apidef[method].length; j++) {
                        key = apidef[method][j];
                        args.push(data[key]);
                    }
                    api[method].apply(self, args);
                }
            }
        } else {
            reader_onloadend.__queue.push(e.target.result);
        }

    };
    reader_onloadend.__queue = [];

    ws.onmessage = function (e, b) {
        console.log("Got msg");
        var reader = new FileReader();
        reader.onloadend = reader_onloadend;
        reader.readAsText(e.data)
    };
    ws.onopen = function (e) {
        ws.send(JSON.stringify({
            method : 'set_api',
            api : apidef
        }) + '\0');
    };

    server = {
        onstart : function () {}
    }

    return {
        api:api,
        server:server
    };
}());
