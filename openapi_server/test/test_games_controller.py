# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.game import Game  # noqa: E501
from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.platform import Platform  # noqa: E501
from openapi_server.test import BaseTestCase


class TestGamesController(BaseTestCase):
    """GamesController integration test stubs"""

    def test_delete_game(self):
        """Test case for delete_game

        Delete game by title
        """
        headers = { 
        }
        response = self.client.open(
            '/games/{search_title}'.format(search_title='search_title_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_games(self):
        """Test case for get_games

        Return all games according to filters
        """
        query_string = [('console', {}),
                        ('year', 'year_example'),
                        ('sort', 'year')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/games',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_games_by_title(self):
        """Test case for get_games_by_title

        Return closest matching games by comparing their title with `searchTitle`
        """
        query_string = [('console', {}),
                        ('year', 'year_example'),
                        ('sort', 'year')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/games/{search_title}'.format(search_title='search_title_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consummes. See https://github.com/zalando/connexion/pull/760")
    def test_post_new_game(self):
        """Test case for post_new_game

        Add new game
        """
        game = {
  "title" : "title",
  "releaseYear" : 0,
  "platforms" : [ null, null ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/games/new',
            method='POST',
            headers=headers,
            data=json.dumps(game),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
