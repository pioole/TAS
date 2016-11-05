

class Timer(object):
    def __init__(self, tick=15):
        """
        creates new Timer object.
        :param tick: Int: time interval between iterations in minutes.
        :return: Timer
        """
        self._time = 0
        self._tick = tick

    def time(self):
        """
        returns current time in minutes
        :return: Int
        """
        return self._time

    def tick(self):
        """
        Ticks the timer by _tick
        :return: None
        """
        self._time += self._tick
