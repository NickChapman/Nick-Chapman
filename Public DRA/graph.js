/**
 * Created by Nick on 7/19/14.
 */

function Graph(x_size, y_size){
    this.canvas = document.createElement("canvas");
    this.canvas.width = x_size;
    this.canvas.height = y_size;
    this.context = this.canvas.getContext("2d");
    this.final = this.canvas;
}

/**
 * @param   percentage  int
 * @returns {number}
 */
Graph.prototype.x_prcnt = function(percentage){
    var width = this.canvas.width;
    var percent = percentage/100;
    return percent*width;
};

/**
 * @param percentage    int
 * @returns {number}
 */
Graph.prototype.y_prcnt = function(percentage){
    var height = this.canvas.height;
    var percent = percentage/100;
    return percent*height;
};

/**
 * //TODO: REFACTOR TO BE OO SYNTAX
 * Draws a grid onto the canvas
 *
 * @param x_spacing     Spacing between the x axis grid lines
 * @param y_spacing     Spacing between the y axis grid lines
 * @param color         The color of the lines to be drawn. Default is #eee, Takes hex or RGB values.
 */
Graph.prototype.add_grid = function(x_spacing, y_spacing, color){
    //Defaults
    color = (typeof color === "undefined") ? "#eee" : color;

    var canvas = this.canvas;
    if(canvas.getContext){
        var context = canvas.getContext("2d");
    }
    context.beginPath();
    var width = canvas.width;
    var height = canvas.height;
    var x = 0.5, y = height - 0.5;

    //Drawing
    context.beginPath();
    for(x; x <= width; x += x_spacing){
        context.moveTo(x, 0);
        context.lineTo(x, height);
    }
    for(y; y >= 0; y -= y_spacing){
        context.moveTo(0, y);
        context.lineTo(width,y);
    }
    context.strokeStyle = color;
    context.stroke();
};

/**
 * Adds axes to the given Graph
 *
 * @param x_padding     Integer percentage
 * @param y_padding     Integer percentage
 * @param color         Color of the axes, hex or RGB allowed
 */
Graph.prototype.add_axes = function(x_padding, y_padding, color){
    if(x_padding > 50 || x_padding < 0){
        throw Error("The padding percentage on the x axis is not allowed");
    }
    if(y_padding > 50 || y_padding < 0){
        throw Error("The padding percentage on the y axis is not allowed")
    }
    this.context.beginPath();
    this.context.strokeStyle = (typeof color === "undefined") ? "#000" : color;
    //Vertical axis
    this.context.moveTo(this.x_prcnt(x_padding), this.y_prcnt(y_padding));
    this.context.lineTo(this.x_prcnt(x_padding), this.y_prcnt(100 - y_padding));
    //Arrow at the end of the line
    this.context.moveTo(this.x_prcnt(x_padding - 1), this.y_prcnt(y_padding + 2));
    this.context.lineTo(this.x_prcnt(x_padding), this.y_prcnt(y_padding));
    this.context.moveTo(this.x_prcnt(x_padding + 1), this.y_prcnt(y_padding + 2));
    this.context.lineTo(this.x_prcnt(x_padding), this.y_prcnt(y_padding));
    //Horizontal axis
    this.context.moveTo(this.x_prcnt(x_padding), this.y_prcnt(100 - y_padding));
    this.context.lineTo(this.x_prcnt(100 - x_padding), this.y_prcnt(100 - y_padding));
    //Arrow at the end of the line
    this.context.moveTo(this.x_prcnt(100 - 2 - x_padding), this.y_prcnt(100 - 1 - y_padding));
    this.context.lineTo(this.x_prcnt(100 - x_padding), this.y_prcnt(100 - y_padding));
    this.context.moveTo(this.x_prcnt(100 - 2 - x_padding), this.y_prcnt(100 + 1 - y_padding));
    this.context.lineTo(this.x_prcnt(100 - x_padding), this.y_prcnt(100 - y_padding));
    //Ink it
    this.context.stroke();
};

/**
 * Draws the minor axes onto the canvas
 *
 * @param x_spacing     The spacing between the lines. Either px or use Graph.x_prcnt()
 * @param y_spacing     The spacing between the lines. Either px or use Graph.y_prcnt()
 * @param x_padding     The spacing between the edge of the canvas and the Graph area. Between 0 and 50
 * @param y_padding     The spacing between the edge of the canvas and the Graph area. Between 0 and 50
 * @param color         Optional, the color of the axes being drawn on.
 */
Graph.prototype.add_minor_axes = function( x_spacing, y_spacing, x_padding, y_padding, color ){
    if ( x_padding > 50 || x_padding < 0 ){
        throw Error("The padding percentage on the x axis is not allowed");
    }
    if( y_padding > 50 || y_padding < 0 ){
        throw Error("The padding percentage on the y axis is not allowed")
    }
    x_padding = this.x_prcnt( x_padding );
    y_padding = this.y_prcnt( y_padding );

    //Drawing begins
    this.context.beginPath();
    var x = x_padding;
    for( x; x <= ( this.canvas.width - x_padding ); x += x_spacing ){
        this.context.moveTo( x, ( this.canvas.height - y_padding ) );
        this.context.lineTo( x, y_padding );
    }
    var y = y_padding;
    for( y; y <= ( this.canvas.height - y_padding ); y += y_spacing ){
        this.context.moveTo( x_padding, y );
        this.context.lineTo( ( this.canvas.width - x_padding ), y );
    }
    this.context.strokeStyle = ( typeof color === "undefined" ) ? "#eee" : color;
    this.context.stroke();
};

/**
 *
 * @param title
 * @param y_padding
 * @param font
 * @param color
 */
Graph.prototype.add_title = function ( title, y_padding, font, color ){
    y_padding = this.y_prcnt( y_padding );

    this.context.beginPath();
    this.context.textAlign = "center";
    this.context.textBaseline = "middle";
    font = ( typeof font === "undefined" ) ? "Verdana" : font;
    this.context.font = "normal " + y_padding/1.5 + "px " + font;
    this.context.fillStyle = ( typeof color === "undefined" ) ? "#000" : color;
    this.context.fillText( title, ( this.canvas.width/2 ), ( y_padding/2 ) );
};

/**
 *
 * @param label
 * @param y_padding
 * @param font
 * @param color
 */
Graph.prototype.add_x_axis_label = function ( label, y_padding, font, color ){
    y_padding = this.y_prcnt( y_padding );

    this.context.beginPath();
    font = ( typeof font === "undefined" ) ? "Verdana" : font;
    this.context.font = "normal " + y_padding/3 + "px " + font;
    this.context.fillStyle = ( typeof color === "undefined" ) ? "#000" : color;
    this.context.textAlign = "center";
    this.context.textBaseline = "middle";
    this.context.fillText( label, this.x_prcnt( 50 ), this.canvas.height - y_padding/3 );
};

/**
 *
 * @param label
 * @param x_padding
 * @param font
 * @param color
 */
Graph.prototype.add_y_axis_label = function ( label, x_padding, font, color ){
    x_padding = this.x_prcnt( x_padding );

    this.context.beginPath();
    //Setup
    this.context.save();
    this.context.translate( 0, this.y_prcnt( 100 ) );
    this.context.rotate( -Math.PI/2 );

    font = ( typeof font === "undefined" ) ? "Verdana" : font;
    this.context.font = "normal " + x_padding/3 + "px " + font;
    this.context.fillStyle = ( typeof color === "undefined" ) ? "#000" : color;
    this.context.textAlign = "center";
    this.context.textBaseline = "middle";
    this.context.fillText( label, this.y_prcnt( 50 ), x_padding/3 );

    //Restore to normal
    this.context.restore();
};

/**
 *
 * @param data
 * @param x_padding
 * @param y_padding
 * @param show_points
 * @param color
 */
Graph.prototype.graph_linear = function ( data, x_padding, y_padding, show_points , color , number_of_axes_labels){
    //TODO: Implement plotting the points not just the line

    x_padding = this.x_prcnt( x_padding );
    y_padding = this.y_prcnt( y_padding );
    var x_set = data.x_data;
    var y_set = data.y_data;
    var min_x = Math.min.apply( null, x_set );
    var max_x = Math.max.apply( null, x_set );
    var min_y = Math.min.apply( null, y_set );
    var max_y = Math.max.apply( null, y_set );
    var x_range = ( min_x < 0) ? max_x - min_x : max_x;
    var y_range = ( min_y < 0) ? max_y - min_y : max_y;
    if ( x_set.length != y_set.length ){
        throw Error("Data length mismatch")
    }

    this.context.beginPath();
    var x = x_padding + ( ( ( min_x < 0 ) ? Math.abs(min_x) : 0 ) + x_set[0] ) / x_range * ( this.canvas.width - 2 * x_padding );
    var y = this.canvas.height - y_padding - ( ( ( min_y < 0 ) ? Math.abs( min_y ) : 0 ) + y_set[0] ) / y_range * ( this.canvas.height - 2 * y_padding );
    this.context.moveTo( x, y );
    for ( var i = 1; i < x_set.length; i++ ){
        x = x_padding + ( ( ( min_x < 0 ) ? Math.abs(min_x) : 0 ) + x_set[i] ) / x_range * ( this.canvas.width - 2 * x_padding );
        y = this.canvas.height - y_padding - ( ( ( min_y < 0 ) ? Math.abs( min_y ) : 0 ) + y_set[i] ) / y_range * ( this.canvas.height - 2 * y_padding );
        this.context.lineTo( x, y );
    }
    this.context.strokeStyle = color || "#000";
    this.context.stroke();

    //Axes numbers
    this.context.beginPath();
    number_of_axes_labels = number_of_axes_labels || 10;
    var x_axis_increment = x_range/number_of_axes_labels;
    console.log(x_range);
    var y_axis_increment = y_range/number_of_axes_labels;
    this.context.textAlign = "center";
    this.context.textBaseline = "top";
    this.context.font = "normal " + (x_padding + y_padding)/10 + "px Verdana";
    for ( i = 1; i <= number_of_axes_labels + 1; i++ ){
        this.context.fillText((Math.round((min_x + (i-1)*x_axis_increment)*100)/100).toString(), x_padding + (i - 1) * (this.canvas.width - 2 * x_padding)/number_of_axes_labels, this.canvas.height - y_padding);
    }
};