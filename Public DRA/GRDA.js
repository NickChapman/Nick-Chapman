/**
 * Created by Nick on 7/17/14.
 */

function draw_all(){
    draw_1();
    draw_2();
}

function draw_1(){
    //Basic Setup
    var canvas = document.getElementById("canvas1");
    draw_grid(canvas, 10, 10);
}

function draw_2(){
    var canvas = document.getElementById("canvas2");
    draw_grid(canvas, 10, 10);
    var data = {};
    data.sets = [];
    var x_coords = [0, 10, 20, 30, 40, 50];
    var y_coords = [0, 50, 200, 450];
    data.sets.push({"x_coords":x_coords, "y_coords":y_coords});
    graph_linear_chart(canvas, data);

}

/**
 * Draws a grid onto the canvas
 *
 * @param canvas    Canvas to be drawn onto
 * @param x_spacing Spacing between the x axis grid lines
 * @param y_spacing Spacing between the y axis grid lines
 * @param color     The color of the lines to be drawn. Default is #eee, Takes hex or RGB values.
 */


function graph_bar_chart(canvas, data){

}

function graph_linear_chart(canvas, data){
    if(canvas.getContext){
        var context = canvas.getContext("2d");
    }
    x_coords = data.sets[0].x_coords;
    y_coords = data.sets[0].y_coords;
    if(x_coords.length != y_coords.length){
        throw Error("Data set length mismatch");
    }
}