import weakref
import logging


class Observed:
    def __init__(self):
        self._observers = weakref.WeakKeyDictionary()
        # TODO: try change WeakKeyDict to WeakSet
        self._mutex = False

    def attach(self, obs):
        self._observers[obs] = 1
        logging.debug("{} added to observers of {}".format(repr(obs), repr(self)))

    def detach(self, obs):
        del self._observers[obs]
        logging.debug("{} removed from observers of {}".format(repr(obs), repr(self)))

    def notify(self, event):
        for obs in self._observers:
            logging.debug("notifying {} of {} event".format(repr(obs), repr(event)))
            obs.handle_event(event, self)


class Event:
    MODEL_CHANGE = 1
    USER_EVENT = 2
    VIEW_CHANGE = 3
    CHANGE_VISIBILITY = 4
