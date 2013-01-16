


var board = (function () {
    var svg, scaled, o;
    var scale_size = 2;

    o = document.querySelector('object');

    var load_stops_handling = (function stops_handling() {
        function increase_size(el) {
            var scale;

            if (!scaled) {
                scale = svg.rootElement.createSVGTransform();
                scale.setScale(scale_size, scale_size);
                el.transform.baseVal.appendItem(scale);
                scaled = el;
            } else if (el !== scaled) {
                decrease_size(el);
                increase_size(el);
            } 
        }
        function decrease_size(el) {
            if (el === scaled) {
                el.transform.baseVal.removeItem(el.transform.baseVal.numberOfItems - 1);
                scaled = undefined;
            } else {
                console.log("Error, scaling wrong element");
                debugger;
            }
        }
        function get_stop(el) {
            while (el.className && el.className.baseVal !== 'stop') {
                el = el.parentNode;
            }
            if (el.className) {
                return el
            }
        }
        function load() {
            svg.onclick = function (e) {
                var el;
                el = get_stop(e.target);
                if (el) {
                    color_stop(el.id, "#FF0000");
                    console.log("clicked on", el.id);
                }
            };

            svg.onmouseover = function (e) {
                var trans, scale, el;
                el = get_stop(e.target);
                if (el) {
                    increase_size(el);
                } 
            };

            svg.onmouseout = function (e) {
                var el;
                el = get_stop(e.target);
                if (el) {
                    decrease_size(el);
                }
            }
        }
        return load;
    }());


    function color_stop(id, color) {
        var el = svg.querySelector(".stop[id='" + id + "']");
        var path = el.querySelector("path");
        var rect = el.querySelector("rect");

        path.style.fill = color;
        rect.style.fill = color;
    }


    o.onload = function () {
        svg = o.getSVGDocument();

        load_stops_handling();
        
    }


    function start(color) {
        var i=0, l = [126, 115, 102, 84, 103, 86, 69, 53, 54, 41, 28, 15, 14, 13, 23, 22, 34, 47, 46, 61, 62, 79, 98, 110, 111, 130, 139, 153, 154, 140, 71, 70, 40, 52, 39, 25, 24, 38, 51, 68, 85, 67, 50, 37, 36, 35, 48, 63, 64, 66, 49, 65, 82, 81, 99, 80, 112, 100, 101, 83, 114, 113, 125, 131, 132, 109, 96, 97, 77, 78, 76, 60, 59, 45, 58, 44, 32, 33, 21, 10, 11, 12, 4, 3, 26, 27, 16, 5, 6, 29, 55, 2, 20, 9, 1, 8, 19, 18, 31, 43, 57, 73, 74, 92, 93, 94, 95, 120, 121, 122, 75, 123, 124, 138, 150, 149, 148, 137, 147, 146, 163, 145, 144, 177, 176, 189, 190, 191, 178, 164, 179, 165, 180, 193, 194, 192, 197, 195, 182, 181, 166, 151, 152, 167, 183, 196, 168, 184, 169, 155, 156, 87, 88, 104, 89, 105, 90, 72, 42, 7, 17, 30, 56, 91, 107, 106, 119, 136, 162, 175, 174, 161, 160, 128, 172, 187, 198, 199, 188, 173, 171, 186, 185, 170, 159, 157, 158, 133, 141, 127, 134, 116, 118, 117, 129, 135, 108, 143, 142];
        function next() {
            color_stop(l[i], color);
            i ++;
        }
        function go() {
            while (true)
                next();
        }



        return {
            'next' : next,
            'go' : go
        };

    }
    
    return start;
}());




/**
 * Registers a connections to the server so that it can push messages to the client.
 *
 */
var url = 'http://dxtr.be:8888/game';
var connection = (function () {
    var request, session_id;


    function on_statechange(e) {
        if (request.readyState === 4) {
            data = JSON.parse(request.response);
            console.log("Done sending -> ", data);
            session_id = data.session_id;

            debugger;

            request.open('POST', url, true);
            request.send();
        }
    }

    request = new XMLHttpRequest();
    request.onreadystatechange = on_statechange;

    request.open('GET', url, true);
    request.send(null);

    return {
        send : undefined,
        receive : undefined,
    }
}());
