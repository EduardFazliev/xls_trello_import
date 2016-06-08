# -*- coding: utf-8 -*-

import xlrd


class XLSColumns(object):
    """Class for creating dictionary of lists from .xls file,
    controlled by user's input.

    """
    def __init__(self, file, sheet):
        """Args:
            file (str): Full path to xls file.
            sheet (int): Number of sheet in xls file,
                that contain desired information.

        """
        self.file = file
        self.sheet = sheet
        self.xls_obj = xlrd.open_workbook(file, formatting_info=True)
        self.columns = dict()
        self.trello_title = list()
        self.trello_description = list()
        self.trello_cards = list()

    def create_structure(self):
        cur_sheet = self.xls_obj.sheet_by_index(self.sheet)
        for numcol in xrange(cur_sheet.ncols):
            column = cur_sheet.col_values(numcol)
            # Storing whole column as list in dictionary with
            # key equal first cell in
            # column(expect it will be header).
            self.columns[column[0]] = [cel for cel in column]
            # column[0] is a header, so remove it from list.
            self.columns[column[0]].remove(column[0])

    @staticmethod
    def ask_user_choose_number(options):
        for number, option in enumerate(options):
            print '[{}]: '.format(number), unicode(option)
        choice = input('Choose number: ')
        return options[choice]

    def headers_mapping(self):
        print """Now you need to choose two headers
        for exporting them to Trello as cards:
        Title for Trello card's name and
        Description for Trello's card description.

        Please, choose number of Title column:
        """
        title_num = self.ask_user_choose_number(self.columns.keys())
        self.trello_title = self.columns[title_num]

        print 'Please, choose number of Description column:'
        descr_num = self.ask_user_choose_number(self.columns.keys())
        self.trello_description = self.columns[descr_num]

        return self.trello_title, self.trello_description


if __name__ == '__main__':
    testclass = XLSColumns('/home/efazliev/Documents/ex.xls', 0)
    testclass.ask_user_choose_number([1, 2, 3])