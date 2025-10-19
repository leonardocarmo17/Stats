from backend.files.ApiMatches import ApiMatches
from backend.files.FutureMatches import FutureMatches
from backend.files.Stats import Stats
def exec():
    ApiMatches().exec()
    FutureMatches().NextMatches()
    Stats().calculate_stats()
    return True