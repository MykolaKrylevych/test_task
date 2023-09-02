from argparse import ArgumentParser
from random import choice
from dotenv import load_dotenv
from requests import get, exceptions
from os import getenv
from database import ActivityDatabase
from tabulate import tabulate
from termcolor import colored

load_dotenv()


def add_new_data(args):
    if not args.type:
        args.type = choice(["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music",
                            "busywork"])
    param = {
        "type": args.type,
        "minaccessibility": args.accessibility_min,
        "maxaccessibility": args.accessibility_max,
        "participants": args.participants,
        "minprice": args.price_min,
        "maxprice": args.price_max,
    }
    db = ActivityDatabase()
    try:
        response = get(f'{getenv("URL")}', params=param)
        if response.status_code == 200:
            db.save_activity(response.json())
            return "Activity successfully added to database :)"
    except exceptions.HTTPError as error:
        print(f"HTTP error occurred {error}")
    except exceptions.RequestException as error:
        print(f"An error occurred during the request:{error}")
    except Exception as error:
        print(f"An error occurred:{error}")
    finally:
        db.close_connection()


def last_activities():
    db = ActivityDatabase()
    colored_headers = [colored(header, 'green') for header in
                       ['ID', 'Type', 'Activity', 'Participants', 'Price', 'Link', 'Key', 'Accessibility']]
    table = tabulate(db.get_latest_activities(),
                     headers=colored_headers,
                     tablefmt='fancy_grid')
    db.close_connection()
    return table


def main():
    parser = ArgumentParser(
        prog='my_program',
        description='This command line app have a method that returns a random activity,'
                    ' and should accept parameters to filter the activities by type,'
                    ' number of participants, price range, and accessibility range.',
    )
    parser.add_argument('filename', default='my_program')

    subparsers = parser.add_subparsers(dest='subcommand', required=True)

    parser_list = subparsers.add_parser('list',
                                        help='This command should return the last 5 activities saved in the database.')
    parser_list.set_defaults(func=last_activities)
    parser_new = subparsers.add_parser('new',
                                       help='This command save random activity in'
                                            ' database if you dont use optional params')
    parser_new.set_defaults(func=add_new_data)

    parser_new.add_argument('--type', default=None, nargs='?', help='This option add type of activities',
                            required=False)
    parser_new.add_argument('--participants', default=None, nargs='?',
                            help='This option set count of participants in request')
    parser_new.add_argument('--price_min', type=float, default=None, nargs='?',
                            help='This option set min price in range')
    parser_new.add_argument('--price_max', type=float, default=None, nargs='?',
                            help='This option set max price in range')
    parser_new.add_argument('--accessibility_min', type=float, default=None, nargs='?',
                            help='This option set a min of accessibility range')
    parser_new.add_argument('--accessibility_max', type=float, default=None, nargs='?',
                            help='This option set a max of accessibility range')

    parser_args_data = parser.parse_args()
    if hasattr(parser_args_data, 'func'):
        if parser_args_data.func == add_new_data:
            return parser_args_data.func(parser_args_data)
        else:
            return parser_args_data.func()
    else:

        print('You must choose action {new or list}')


if __name__ == '__main__':
    result = main()
    if result:
        print(result)
