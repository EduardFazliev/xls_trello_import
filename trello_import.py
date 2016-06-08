# -*- coding: utf-8 -*-

import time

import trello

from config import apikey, token


class TrelloImport(object):
    """Class for creating new cards in user-defined list.

    """
    def __init__(self, board_id, list_name):
        """Args:
            board_id (str): ID of board,
                where list list_name is created.
            list_name (str): Name of list,
                where new cards will be created.

        """
        self.board_id = board_id
        self.list_name = list_name
        self.trelo = trello.TrelloApi(
            apikey=apikey
        )
        self.trelo.set_token(
            token=token
        )
        self.list_id = self._get_list_id()

    def _get_list_id(self):
        """Method returns list id by name.

        Returns:
            string: ID of list.
        """
        lst_list = self.trelo.boards.get_list(self.board_id)
        for lst in lst_list:
            if lst['name'] == self.list_name:
                return lst['id']

    def create_cards(self, titles, descriptions):
        """ Method creates new cards.

        Args:
            titles (str): Title of new card.
            descriptions (str): Description of a new card.

        Returns:
            dict: dict of str: str
                {
                    key (str): card title
                    value (str): "Card created"
                        if card created successfully,
                        "Card not created" and traceback
        """
        responses = dict()
        for title, description in zip(titles, descriptions):
            try:
                self.trelo.lists.new_card(list_id=self.list_id, name=title, desc=description)
                time.sleep(1)
            except Exception as e:
                responses[title] = 'Card not created: {}'.format(e)
                print u'Card with title: {0}\n' \
                      'Result:' \
                      'Card not created because {1}'.format(title, e)
                print '-*'*50
            else:
                responses[title] = 'Card created.'
                print u'Card with title: {0}\nResult: Created successfully!'.format(title)
                print '-*' * 50
        return responses
