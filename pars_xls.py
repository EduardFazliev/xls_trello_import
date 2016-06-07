# -*- coding: utf-8 -*-
from multiprocessing import Pool

import time

import trello
import xlrd


class XLS_Columns(object):
    def __init__(self, file, sheet):
        self.columns = dict()
        self.file = file
        self.sheet = sheet
        self.xls_obj = xlrd.open_workbook(file, formatting_info=True)
        self.trello_title = list()
        self.trello_description = list()
        self.trello_cards = list()

    def create_structure(self):
        cur_sheet = self.xls_obj.sheet_by_index(self.sheet)
        for numcol in xrange(cur_sheet.ncols):
            column = cur_sheet.col_values(numcol)
            # Storing whole column as list in dictionary with
            # key equal first cell in
            # column(expect it will be header)
            self.columns[column[0]] = [cel for cel in column]
            self.columns[column[0]].remove(column[0])

    def headers_mapping(self):
        print """Please, choose mapping between xls document's headers and Trello's card fields:
        Title of Trello card is:"""
        trello_choose = [key for key in self.columns.keys()]
        for i, key in enumerate(trello_choose):
            print '[{0}]: '.format(i), unicode(key)

        num_title = raw_input('Choose number: ')
        self.trello_title = self.columns[trello_choose[int(num_title)]]

        print """Nice! Well done!
        Now choose Trello description field:"""

        for i, key in enumerate(trello_choose):
            print '[{0}]: '.format(i), unicode(key)

        num_desc = raw_input('Choose number: ')
        self.trello_description = self.columns[trello_choose[int(num_desc)]]
        for title, desc in zip(self.trello_title, self.trello_description):
            self.trello_cards.append((title, desc))


class TrelloCardsImport(object):
    def __init__(self, board_id, list_name):
        self.board_id = board_id
        self.list_name = list_name
        self.trelo = trello.TrelloApi(
            apikey='40b1ba0b3506b70fdd24fe3654697479'
        )
        self.trelo.set_token(
            token='1546d5ce710fe94801d36df875313fc4e3aa78a5a5e5cca3c811ca232356dc4a'
        )
        self.list_id = self._get_list_id()

    def _get_list_id(self):
        lsts_list = self.trelo.boards.get_list(self.board_id)
        for lst in lsts_list:
            if lst['name'] == self.list_name:
                return lst['id']

    def create_cards(self, cards_list):
        for elem in cards_list:
            try:
                self.trelo.lists.new_card(list_id=self.list_id, name=elem[0], desc=elem[1])
                time.sleep(2)
            except Exception as e:
                print e
                result = (1, e)
            else:
                result = (0, 'success')


if __name__ == '__main__':
    xls = XLS_Columns('/home/efazliev/Documents/issues_export.xls', 0)
    xls.create_structure()
    xls.headers_mapping()
    list_name = raw_input('Enter name of Trello\'s list you wish to add new Trello cards:')
    board_id = raw_input('Enter board ID (from board URL)') # hZHMkyYU
    trl = TrelloCardsImport('hZHMkyYU', 'Issues')
    trl.create_cards(xls.trello_cards)