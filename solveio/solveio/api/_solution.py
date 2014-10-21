"""
Solution Resource
~~~~~~~~~~~~~~~~~
Information regarding all the available exercices.
"""
import cherrypy


class Solution:

    """The representation of the solution proposed by us."""

    exposed = True

    def __init__(self):
        """Setup the new instance."""

    @cherrypy.tools.user_required()
    def GET(self, *args, **kwargs):
        """View the solutions."""
        if args:
            # TODO: View a specific solution
            pass
        else:
            # TODO: View a list with all the available solutions
            pass
