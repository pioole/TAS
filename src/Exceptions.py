
class NoBinsAvailableException(Exception):
    pass


class BinTooSmallException(Exception):
    pass


class UnAuthorisedAccessException(Exception):
    pass


class NoMoreStaticDataException(Exception):
    pass


class BinNotEmptyException(Exception):
    pass


class BackfillJobPriorityException(Exception):
    pass


class JobQueueEmptyException(Exception):
    pass


class NoFittingStrategyException(Exception):
    pass