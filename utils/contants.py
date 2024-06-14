from enum import Enum

class SearchItemType(Enum):
    MOVIE = "Movie"
    TV_SHOW = "TV Show"
    CELEB = "Celeb"

class CelebRoles(Enum):
    WRITER = 1
    PRODUCER = 2
    DIRECTOR = 3
    ACTOR = 4