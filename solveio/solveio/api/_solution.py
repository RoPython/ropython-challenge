"""
Solution Resource
~~~~~~~~~~~~~~~~~
Information regarding all the available exercices.
"""
import os
import cherrypy

from solvio.util import RedisConnection
from solvio.config import SOLUTIONS


class Solution:

    """The representation of the solution proposed by us."""

    exposed = True

    def __init__(self):
        """Setup the new instance."""
        self._rcon = RedisConnection()

    @cherrypy.tools.user_required()
    def GET(self, exercise=None, api_key=None, status=True, verbose='OK'):
        """View the solutions."""
        response = {"meta": {"status": status, "verbose": verbose},
                    "content": None}

        if not response["status"]:
            cherrypy.response.status = 400
            return response

        if exercise:
            if ".." in exercise or not exercise.endswith('.py'):
                cherrypy.response.status = 400
                response["meta"]["status"] = False
                response["meta"]["verbose"] = "Invalid solution name"
            else:
                exercise_path = os.path.join(SOLUTIONS, exercise)
                if os.path.isfile(exercise_path):
                    # Lock this exercise
                    self._rcon.add_exercise_lock(api_key, exercise)

                    file_handle = open(exercise_path, "r")
                    response["content"] = file_handle.read()
                    file_handle.close()
                else:
                    cherrypy.response.status = 404
                    response["meta"]["status"] = False
                    response["meta"]["verbose"] = "Exercise not found"
        else:
            response["content"] = os.listdir(SOLUTIONS)

        return response
