import cherrypy

from solveio.util import UserManager

from ._exercise import Exercise
from ._plugins import Evaluator
from ._solution import Solution
from ._submit import Submit
from ._top import Top

cherrypy.tools.user_required = UserManager()
evaluator = Evaluator(cherrypy.engine)
evaluator.subscribe()