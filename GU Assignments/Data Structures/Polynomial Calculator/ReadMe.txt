************************************************************
*                                                          *
*                 Polynomial Calculator                    *
*                   By Nick Chapman                        *
*              nlc35 at georgetown dot edu                 *
*                 Last Modified 9/22/15                    *
*                                                          *
************************************************************

----------------------------------
		Running the program
----------------------------------
From the command line type the following:
	python poly_calc.py -i <input_file>

An input file is required and the input file must be in the form:
2 4 13 3 -2 2 4 1 -3 0
3 4 2 3 13 2 1 1 5 0
2 1 1 0
*
+

Which is equivalent to

(3x^4 + 2x^3 + 13x^2 + x + 5)*(2x + 1) + (2x^4 + 13x^3 - 2x^2 + 4x - 3)

An optional output file my be specified by using the -o flag 
followed by the name of the file

This information can be found from the command line by using the -h flag

----------------------------------
		Implementation
----------------------------------
The Polynomial class is at its core a collection of Terms stored in a Vector. 
The Term class is simply a pair used to represent a term in a polynomial.
The Vector class runs off of a circularly and doubly linked list. 
The Stack class is for the most part a wrapper around the Vector class

----------------------------------
		Knowledge Gained
----------------------------------
 - Arithmetic operator overloading in Python
 - Creating an iterable class in Python
 - Implentation of a stack
 - Basic file operations in Python

 






 This project was created for Georgetown's COSC-160: Data Structures, Fall 2015