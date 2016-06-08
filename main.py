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

    print """Now you need to enter board ID. You can find it in URL.
    Example: https://trello.com/b/jOnfDJKu/boardname.
    'jOnfDJKu' here is board ID.
    """
    board_id = raw_input("Enter Trello's board ID: ")

    list_name = raw_input("Please, enter name of list you want to use for new cards: ")

    trello_imp = TrelloImport(board_id, list_name)

    responses = trello_imp.create_cards(xls.trello_title, xls.trello_description)

    if yes_no_choose('Do you want to write results in file?'):
        log_file = raw_input("Path to file to store results: ")
        resp_table = PrettyTable(['Card', 'Response'])
        resp_table.align = 'l'
        resp_table.header = True
        resp_table.hrules = ALL
        for key in responses.keys():
            resp_table.add_row([key, responses[key]])

        try:
            with open(log_file, 'w') as f:
                f.write(str(resp_table))
        except IOError as e:
            print "Can't write results to file {0}. " \
                  "Error: {1}".format(log_file, resp_table)
        except KeyboardInterrupt:
            exit(1)

