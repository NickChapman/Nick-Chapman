from poly.polynomial import Polynomial
from vector.vector import Vector
from stack import Stack
import sys, getopt

def main(argv):
    input_file = ""
    output_file = ""
    # First we attempt to get the options from the command line
    try:
        options, args = getopt.getopt(argv, "i:o:h")
    except getopt.GetoptError:
        print("""Call via `python poly_calc.py -i <input_file> -o <output_file>`\n
                Use `python poly_calc.py -h` for help""")
        # exit status 2 for command line error
        sys.exit(2)
    # Now we check what options were entered and act appropriately
    for option, argument in options:
        if option == "-h":
            print("Call the script using:")
            print("  python poly_calc.py -i <input_file> -o <output_file>")
            print("The following flags are used:")
            print("  -i must be by the input file name")
            print("  -o can be followed by the output file name if desired")
        if option == "-i":
            input_file = argument
        if option == "-o":
            output_file = argument
    # Ensure that there is input data
    if input_file == "":
        print("An input file must be specified")
    else:
        data = Vector() # Holds all of the lines out of the input file
        stack = Stack() # Used to store the Polynomials and perform operations
        # Read all of the lines out of the file
        with open(input_file) as f:
            for line in f:
                data.append(line.strip())
        for line in data:
            if line == "+":
                p1 = stack.top()
                stack.pop()
                p2 = stack.top()
                stack.pop()
                stack.push(p1 + p2)
            elif line == "-":
                p1 = stack.top()
                stack.pop()
                p2 = stack.top()
                stack.pop()
                stack.push(p1 - p2)
            elif line == "*":
                p1 = stack.top()
                stack.pop()
                p2 = stack.top()
                stack.pop()
                stack.push(p1 * p2)
            else:
                stack.push(Polynomial(line))
        if output_file != "":
            with open(output_file, 'w+') as f:
                print(stack.top(), file=f)
        else:
            print(stack.top())

if __name__ == "__main__":
    # Split because argv[0] is simply the program name
    main(sys.argv[1:]) 