"""
Submit Resource
~~~~~~~~~~~~~~~
The resource which provides to users the possibility to submit a solution.
"""
import cherrypy


class Submit:

    """The representation of users solutions."""

    def __init__(self):
        """Setup the new instance."""

    @cherrypy.tools.user_required()
    def GET(self):
        """View all the submited solutions."""

    @cherrypy.tools.user_required()
    def POST(self):
        """Submit solution."""
