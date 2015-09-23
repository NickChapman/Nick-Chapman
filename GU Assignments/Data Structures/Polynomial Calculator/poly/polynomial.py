from vector.vector import Vector
from poly.term import Term

class Polynomial:
    """Represents a polynomial as a collection of terms and stores in a Vector"""

    def __init__(self, poly_string=""):
        """Builds a polynomial
            If a string is given in the right format it will split it to build the polynomial"""
        self.terms = Vector()
        if poly_string != "":
            poly_pieces = Vector()
            poly_pieces.build_from_list(poly_string.split(" "))
            for i in range(0, len(poly_pieces), 2):
                coef = poly_pieces[i]
                exponent = poly_pieces[i + 1]
                self.terms.insert_rear(Term(int(coef), int(exponent)))
            #condense similar terms
            self.combine_like_terms()
            # Sort the terms
            self.sort_terms()

    def __add__(self, other): 
        """Overloaded addition operator"""
        temp = Vector()
        for term in self.terms:
            temp.append(term)
        for term in other.terms:
            temp.append(term)
        new_poly = Polynomial()
        new_poly.terms = temp
        new_poly.combine_like_terms()
        new_poly.sort_terms()
        return new_poly

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """Overlaoded subtraction operator"""
        p = Polynomial("-1 0")
        return (self + (p * other))

    def __mul__(self, other):
        """Overloaded multiplication operator"""
        temp = Vector()
        for term in self.terms:
            for item in other.terms:
                new_coef = term.coef * item.coef
                new_exp = term.exponent + item.exponent
                temp.append(Term(new_coef, new_exp))
        new_poly = Polynomial()
        new_poly.terms = temp
        new_poly.combine_like_terms()
        new_poly.sort_terms()
        return new_poly

    def __rmul__(self, other):
        return self.__mul__(other)

    def sort_terms(self):
        """Sorts the terms of the polynomial in O(n^2) time"""
        temp = Vector()
        for i in range(len(self.terms)):
            max_exp = self.terms[0].exponent
            max_exp_index = 0
            for index, term in enumerate(self.terms):
                if term.exponent > max_exp:
                    max_exp = term.exponent
                    max_exp_index = index
            temp.append(self.terms[max_exp_index])
            self.terms.erase(max_exp_index)
        self.terms = temp

    def combine_like_terms(self):
        max_exponent = 0
        temp = Vector()
        for term in self.terms:
            max_exponent = max(max_exponent, term.exponent)
        for exponent in range(max_exponent + 1):
            new_coef = 0
            for term in self.terms:
                if term.exponent == exponent:
                    new_coef += term.coef
            if (new_coef != 0):
                temp.append(Term(new_coef, exponent))
        self.terms = temp
        self.sort_terms
                
    def __str__(self):
        """Returns a string representation of the polynomial"""
        temp = ""
        if len(self.terms) > 0:
            if self.terms[0].coef < 0:
                temp += "-"
            temp += str(abs(self.terms[0].coef))
            if self.terms[0].exponent != 0:
                temp += "x^" + str(self.terms[0].exponent)
            for i in range(1, len(self.terms)):
                if self.terms[i].coef > 0:
                    temp += " + "
                else:
                    temp += " - "
                temp += str(abs(self.terms[i].coef))
                if self.terms[i].exponent != 0:
                    temp += "x^" + str(self.terms[i].exponent)
        return temp

