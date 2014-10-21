import cherrypy

from solveio.util import UserManager

from ._exercise import Exercise
from ._plugins import Evaluator
from ._solution import Solution
from ._submit import Submit

cherrypy.tools.user_required = UserManager()
evaluator = Evaluator(cherrypy.engine)
evaluator.subscribe()


class API:

    exercise = Exercise()
    solution = Solution()
    submit = Submit()

    exposed = True

    _cp_config = {'tools.staticdir.on': False}

    @cherrypy.tools.json_out()
    def GET(self):
        return {
            "meta": {},
            "content": {
                "/exercise": "",
                "/solution": "",
                "/submit": ""
            }
        }

    @staticmethod
    def config():
        return {
            'global': {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 9090,
                'environment': 'production',
                'log.screen': 'error',
                'log.error_file': 'site.log',
                'server.thread_pool': 32,
                'log.screen': False,
            },
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }

if __name__ == "__main__":
    cherrypy.quickstart(API(), config=API.config)
