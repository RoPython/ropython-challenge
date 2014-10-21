"""
Exercice Resource
~~~~~~~~~~~~~~~~~
Information regarding all the available exercices.
"""
import os
import cherrypy

from solvio.config import PROBLEMS


class Exercise:

    """The representation of the exercices."""

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, exercise=None):
        """View the exercises."""
        response = {"meta": {"status": True, "verbose": "OK"}, "content": None}

        if exercise:
            if ".." in exercise or not exercise.endswith('.py'):
                cherrypy.response.status = 400
                response["meta"]["status"] = False
                response["meta"]["verbose"] = "Invalid exercise name"
            else:
                exercise_path = os.path.join(PROBLEMS, exercise)
                if os.path.isfile(exercise_path):
                    file_handle = open(exercise_path, "r")
                    response["content"] = file_handle.read()
                    file_handle.close()
                else:
                    cherrypy.response.status = 404
                    response["meta"]["status"] = False
                    response["meta"]["verbose"] = "Exercise not found"
        else:
            response["content"] = os.listdir(PROBLEMS)

        return response
