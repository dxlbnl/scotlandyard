


var board = (function () {
    var svg, scaled, o;
    var board;

    board = {
        color_stop : color_stop,
        /**
         * Removes all formatting from the board, cleans it.
         *
         */
        clear : function() {
            var i, stops, path, rect;
            stops = svg.querySelectorAll(".stop");

            for (i=0; i<stops.length; i++) {
                path = stops[i].querySelector("path");
                rect = stops[i].querySelector("rect");
                path.style.fill = '';
                rect.style.fill = '';
            }
        },
        setscale : function (el, scale_size) {
            var scale, i, scale_type = 3;

            // if scale is already set:
            if (el.transform) {

                for (i=0; i<el.transform.baseVal.numberOfItems; i++) {
                    if (scale_type == el.transform.baseVal.getItem(i).type) {
                        scale = el.transform.baseVal.getItem(i);
                    }
                }
            }
            // else, create the scale.
            if (!scale) {
                scale = svg.rootElement.createSVGTransform();
                el.transform.baseVal.appendItem(scale);
            }


            scale.setScale(scale_size, scale_size);
        },
        getstop : function (id) {
            return svg.querySelector(".stop[id='"+id+"']");
        },
        onmouseover : function (){},
        onmouseout  : function (){},
        onclick     : function (){},
    }

    o = document.querySelector('object');

    var load_stops_handling = (function stops_handling() {
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
                    board.onclick(el);
                }
            };

            svg.onmouseover = function (e) {
                var trans, scale, el;
                el = get_stop(e.target);
                if (el) {
                    board.onmouseover(el);
                } 
            };

            svg.onmouseout = function (e) {
                var el;
                el = get_stop(e.target);
                if (el) {
                    board.onmouseout(el);
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

    return board;

}());
