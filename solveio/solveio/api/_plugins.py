"""Cherrypy plugins"""

import cherrypy
import queue
import threading


class Evaluator(cherrypy.plugins.SimplePlugin):

    thread = None

    def __init__(self, bus, queue_size=100, timeout=2):
        super(Evaluator, self).__init__(self, bus)
        self._queue = queue.Queue(queue_size)
        self._timeout = timeout
        self._stop_event = threading.Event()

    def start(self):
        """Power on."""
        if not self.thread:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        """Power off."""
        self._stop_event.set()
        if self.thread:
            self.thread.join()
            self.thread = None

    def run(self):
        """Run until stop event is set."""
        while not self._stop_event.is_set():
            try:
                function, args, kwargs = self._queue.get(block=True,
                                                         timeout=self._timeout)
            except queue.Empty:
                continue

            try:
                function(*args, **kwargs)
                pass
            except Exception as exc:
                self.bus.log("Error in Evaluator %r: %s." % (self, exc),
                             level=40, traceback=True)

    def put(self, function, *args, **kwargs):
        """Schedule the given script to be run."""
        self._queue.put((function, args, kwargs))
