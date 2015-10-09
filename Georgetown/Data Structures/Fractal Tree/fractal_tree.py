from draw_tree import draw_tree
import sys
import getopt
import turtle

def main(argv):
    # First we attempt to get the options from the command line
    try:
        options, args = getopt.getopt(argv, "s:a:m:f:d:h")
    except getopt.GetoptError:
        print("""Call via `python fractal_tree.py`\n
                Use `python fractal_tree.py -h` for help""")
        # exit status 2 for command line error
        sys.exit(2)
    # Preset options to default values
    starting_size = 100
    angle = 50
    minimum_size = 10
    scale_factor = 2.0/3.0
    draw_speed = 8
    # Check if there are any option changes
    for option, argument in options:
        if option == "-h":
            print("The following flags are available:")
            print("  -s Size: Length of initial branch")
            print("     Default: 100")
            print("  -a Angle: Deviation to each side of the branch (degrees)")
            print("     Default: 50")
            print("  -m Min: Smallest branch size")
            print("     Default: 10")
            print("  -f Scale Factor: How much each branch should shrink by")
            print("     !!!!! MUST BE LESS THAN 1 !!!!!")
            print("     Default: 2/3")
            print("  -d Draw speed: How fast the pen will move.")
            print("     Values of 0 to 10 are accepted. 0 means no animation.")
            print("     Default: 5")
            sys.exit(0)
        elif option == "-s":
            if float(argument) > 0:
                starting_size = float(argument)
            else:
                raise RuntimeError("The starting size was less than or equal to 0")
        elif option == "-a":
            angle = float(argument)
        elif option == "-m":
            if float(minimum_size) > 0:
                minimum_size = float(argument)
            else:
                raise RuntimeError("Minimum size must be greater than 0")
        elif option == "-f":
            if float(argument) < 1 and float(argument) > 0:
                scale_factor = float(argument)
            else:
                raise RuntimeError("The scale factor passed in was not less than 1")
        elif option == "-d":
            # No checking is needed because the turtle.speed() takes care of the range
            draw_speed = float(argument)
    
    # Begin by prepositioning the turtle
    # We can begin drawing by simply calling turtle's methods
    # Set the drawing speed
    turtle.speed(draw_speed)
    # Turn left 90 degrees so the tree draws right way up
    turtle.left(90)
    # Lift the pen so it doesn't draw right away
    turtle.penup()
    # Move back from the middle to create room for the tree
    # Height of the tree = starting size / (1 - scale factor)
        # This is just the sum of a geometric series
    # We center on half the height
    turtle.back(.5*(starting_size/(1-scale_factor)))
    # Place the pen back down
    turtle.pendown()
    # Now we just draw the tree
    draw_tree(starting_size, angle, minimum_size, scale_factor)

    input("Press Enter to close the window")

if __name__ == "__main__":
    # Split because argv[0] is simply the program name
    main(sys.argv[1:]) 