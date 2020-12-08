from typing import List, Optional

import connexion
import six

from openapi_server.models.game import Game  # noqa: E501
from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.platform import Platform  # noqa: E501
from openapi_server import util

all_games = [
    Game(title='final fantasy vii remake', release_year=2020, platforms=[Platform.PLAYSTATION_4]),
    Game(title='final fantasy ix', release_year=2000, platforms=[Platform.PLAYSTATION_1]),
    Game(title='final fantasy viii', release_year=1999, platforms=[Platform.PLAYSTATION_1]),
    Game(title='final fantasy vii', release_year=1997, platforms=[Platform.PLAYSTATION_1]),
    Game(title='zelda breath of the wild', release_year=2017, platforms=[Platform.NINTENDO_SWITCH]),
    Game(title='cyberpunk 2077', release_year=2020,
         platforms=[Platform.PLAYSTATION_4, Platform.PC, Platform.XBOX_ONE])
]


def _find_by_year(source: List[Game], year: int) -> List[Game]:
    ret = []
    for game in source:
        if game.release_year == year:
            ret.append(game)
    return ret


def _find_by_title(source: List[Game], title: str) -> List[Game]:
    ret = []
    for game in source:
        if game.title.startswith(title.lower()):
            ret.append(game)
    return ret


def _find_by_console(source: List[Game], console: str) -> List[Game]:
    ret = []
    for game in source:
        for platform in game.platforms:
            if platform == console:
                ret.append(game)
                break
    return ret


def _filter_games(source: List[Game], sort: str, year: Optional[int], console: Optional[str]) -> List[Game]:
    tmp_source = source
    if year:
        tmp_source = _find_by_year(tmp_source, year)
    if console:
        tmp_source = _find_by_console(tmp_source, console)

    ret = []
    if sort == 'name':
        ret = sorted(tmp_source, key=lambda g: g.title)
    elif sort == 'year':
        ret = sorted(tmp_source, key=lambda g: g.release_year, reverse=True)
    return ret


def delete_game(search_title):  # noqa: E501
    """Delete game by title

     # noqa: E501

    :param search_title: 
    :type search_title: str

    :rtype: None
    """
    found = False
    count = 0
    while not found and count < len(all_games):
        if search_title.lower() == all_games[count].title:
            found = True
        else:
            count += 1
    if found:
        del all_games[count]
        return Message(message="game '{}' deleted".format(search_title), code=200, success=True)
    else:
        return Message(message="game '{}' not found".format(search_title), code=404, success=False)


def get_games(console=None, year=None, sort=None):  # noqa: E501
    """Return all games according to filters

     # noqa: E501

    :param console: Console name
    :type console: dict | bytes
    :param year: 
    :type year: str
    :param sort: 
    :type sort: str

    :rtype: List[Game]
    """
    year = int(year) if year else None
    console = str(console) if console else None
    return _filter_games(all_games, sort, year, console)


def get_games_by_title(search_title, console=None, year=None, sort=None):  # noqa: E501
    """Return closest matching games by comparing their title with &#x60;searchTitle&#x60;

     # noqa: E501

    :param search_title: 
    :type search_title: str
    :param console: Console name
    :type console: dict | bytes
    :param year: 
    :type year: str
    :param sort: 
    :type sort: str

    :rtype: List[Game]
    """
    found_games_by_title = _find_by_title(all_games, search_title)
    year = int(year) if year else None
    console = str(console) if console else None
    return _filter_games(found_games_by_title, sort, year, console)


def post_new_game(game):  # noqa: E501
    """Add new game

     # noqa: E501

    :param game: Game parameters
    :type game: dict | bytes

    :rtype: Message
    """
    if connexion.request.is_json:
        game = Game.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        tmp_dict = {}
        for k in connexion.request.form.keys():
            value = connexion.request.form[k]
            if k == 'platforms':
                value = [item.strip() for item in value.split(',')]
            tmp_dict[k] = value
        game = Game.from_dict(tmp_dict)
        game.title = game.title.lower()
    ret_code, ret_msg = _add_game(game)
    return Message(message=ret_msg, code=ret_code, success=ret_code == 201) if connexion.request.is_json else ret_code


def _add_game(new_game: Game):
    games = _find_by_title(all_games, new_game.title)
    if games:
        return 409, '{} already exists'.format(new_game.title)
    else:
        all_games.append(new_game)
        return 201, '{} game added successfully'.format(new_game.title)
