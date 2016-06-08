import cmd
import readline
import os

from prettytable import PrettyTable, ALL

from xls_columns import XLSColumns
from trello_import import TrelloImport


def yes_no_choose(question):
    while True:
        ans = raw_input('{0} [y/n] '.format(question))
        if ans in ['Y', 'y', 'yes', 'Yes', 'YES']:
            return True
        elif ans in ['N', 'n', 'no', 'No', 'NO']:
            return False
        else:
            print 'Choose "y" or "n", please.'


if __name__ == '__main__':
    print """
    +------------------------------------------------+
    |                                                |
    +-------------> Fork me on GitHub! <-------------+
    |                                                |
    +------------------------------------------------+

    https://github.com/EduardFazliev/xls_trello_import

    +------------------------------------------------+

    Hi! xls_trello_import is a console tool, that allows you to export
    some info from xls file to Trello. You need to get apikey and
    generate token to use this tool. Enjoy!
    -----
    """

    readline.parse_and_bind("tab: complete")
    try:
        while True:
            filename = raw_input('Enter full path to xls file you want to import: ')
            if not os.path.isfile(filename):
                print '\nNo such file, please try again.\n'
                continue
            break
    except Exception as e:
        print 'Error: {0}'.format(e)
    except KeyboardInterrupt:
        print '\nGot keyboard interrupt, exiting...'
        exit(0)

    try:
        while True:
            try:
                sheet_num = input('Enter number of sheet you want to import: ')
            except NameError:
                print 'Enter number, please.'
                continue
            else:
                break
    except Exception as e:
        print 'Error: {0}'.format(e)
    except KeyboardInterrupt:
        print '\nGot keyboard interrupt, exiting...'
        exit(0)

    xls = XLSColumns(filename, sheet_num)

    print 'Creating xls structure...'
    try:
        xls.create_structure()
    except Exception as e:
        print 'Error: {0}'.format(e)
    except KeyboardInterrupt:
        print '\nGot keyboard interrupt, exiting...'
        exit(0)
    else:
        print 'Structure created!'

    print 'Start field mapping...'
    try:
        titles, descriptions = xls.headers_mapping()
    except Exception as e:
        print 'Error: {0}'.format(e)
    except KeyboardInterrupt:
        print '\nGot keyboard interrupt, exiting...'
        exit(0)
    else:
        print 'Mapping is done!'

    if yes_no_choose('Do you want to see example of trello cards? '):
        pt = PrettyTable(['Title', 'Description'])
        pt.align = 'l'
        pt.header = True
        pt.hrules = ALL
        for title, descr in zip(titles, descriptions):
            pt.add_row([title[0:75]+'...', descr[0:75]+'...'])
        print pt
        raw_input('Press ENTER to continue...')

    trello_imp = TrelloImport('hZHMkyYU', 'Issues')
    responses = trello_imp.create_cards(xls.trello_title, xls.trello_description)

    if yes_no_choose('Do you want to print results in table format?'):
        resp_table = PrettyTable(['Card', 'Response'])
        resp_table.align = 'l'
        resp_table.header = True
        resp_table.hrules = ALL
        for key in responses.keys():
            resp_table.add_row(key, responses[key])
        print resp_table
