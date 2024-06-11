from enum import Enum

class SearchItemType(Enum):
    MOVIE = "Movie"
    TV_SHOW = "TV Show"
    CELEB = "Celeb"

class CelebRoles(Enum):
    WRITER = "Writer"
    PRODUCER = "Producer"
    DIRECTOR = "Director"
    ACTOR = "Actor"