"""
Exercice Resource
~~~~~~~~~~~~~~~~~
Information regarding all the available exercices.
"""


class Exercise:

    """The representation of the exercices."""

    exposed = True

    def GET(self, *args, **kwargs):
        """View the exercises."""
        if args:
            # TODO: View a specific exercise
            pass
        else:
            # TODO: View all the exercises
            pass
