class Term:
    """A single term in a polynomial"""

    def __init__(self, coef, exponent):
        self.coef = coef
        self.exponent = exponent

    # TODO: define a comparison between these guys so sorting can be used