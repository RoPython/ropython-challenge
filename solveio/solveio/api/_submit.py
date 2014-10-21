"""
Submit Resource
~~~~~~~~~~~~~~~
The resource which provides to users the possibility to submit a solution.
"""
import cherrypy

from solvio.util import RedisConnection
from solvio.check import save_user_problem


class Submit:

    """The representation of users solutions."""

    def __init__(self):
        """Setup the new instance."""
        self._rcon = RedisConnection()

    @cherrypy.tools.json_out()
    @cherrypy.tools.user_required()
    def POST(self, api_key, exercise, content, **kwargs):
        """Submit solution."""
        response = {"meta": {"status": kwargs.pop('status'),
                             "verbose": kwargs.pop('verbose')},
                    "content": None}

        if not response["meta"]["status"]:
            cherrypy.response.status = 400
            return response

        if self._rcon.get_exercise_lock(api_key, exercise):
            response["meta"]["status"] = False
            response["meta"]["verbose"] = ""
            cherrypy.response.status = 403

        save_user_problem(api_key, exercise, content)
        # TODO: Notify Evaluator
