import turtle

def draw_tree(size, angle, min_size, scale_factor):
    if size > min_size:
        turtle.forward(size)
        turtle.right(angle)
        draw_tree(size * scale_factor, angle, min_size, scale_factor)
        turtle.left(angle*2)
        draw_tree(size * scale_factor, angle, min_size, scale_factor)
        turtle.right(angle)
        turtle.back(size)
