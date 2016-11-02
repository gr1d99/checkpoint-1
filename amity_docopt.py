"""
AlloAmity is an Office Space allocation sysytem that allocates
offices and living sapces in Amity, one of Andela's facilties.

Usage:
	amity 	create_room <room_name> <room_type> <room_capacity>
	amity 	add_person <first_name> <last_name> <job_group> <gender> [want_accomodation]
	amity 	reallocate_person <person_identifier> <new_room_name>
	amity 	load_people
	amity 	print_allocations [-o=filename]
	amity 	print_unallocated [-o=filename]
	amity 	print_room <room_name>
	amity 	save_state [--db=database]
	amity 	load_state <database>
	amity 	--help|-h
	amity 	--version
	amity 	--interactive|-i

Options:
	-o 			outputs to a file with specified filename
	--db 		specifies the database that should be saved to
	--help,-h 	shows this help message and exits
	--version	shows the version of AlloAmity
	--interactive, -i 	interactive mode

"""

import sys
import cmd
from models import amity_database
from app.amity import Amity
from app.room import Room
from app.people import Person
from docopt import docopt, DocoptExit
import os


def docopt_cmd(func):

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            print('\nInvalid Command! Type help to see list of available commands')
            print(e)
            return
        except SystemExit:
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)

    return fn


class AlloAmity(cmd.Cmd):

    intro = '\nWelcome to AlloAmity - A Space allocation system \n'
    prompt = 'AlloAmity-->'

    @docopt_cmd
    def do_about(self, args):
        """
        Displays the Usage docstring

        Usage: about
        """
        print(__doc__)

    @docopt_cmd
    def do_create_room(self, args):
        """
        Creates new rooms in Amity

        Usage: create <room_name> <room_type> <room_capacity>

        """
        Room.create_room(
            args["<room_name>"],
            args["<room_type>"],
            args["<room_capacity>"])

    @docopt_cmd
    def do_add_person(self, args):
        """
        Adds a person to the system and allocates the person to a random room.

        Usage: add_person <first_name> <last_name> <job_group> <gender> [want_accomodation]
        """
        Room.add_person(
            args['<first_name>'],
            args['<last_name>'],
            args['<job_group>'],
            args['want_accomodation'],
            args['<gender>'])

    @docopt_cmd
    def do_load_people(self, args):
        """
        Adds people to rooms from a txt file. See Appendix 1A for text input format.

        Usage: load_people
        """
        Room.load_people(args)

    @docopt_cmd
    def do_print_allocations(self, args):
        """
        Prints a list of allocations onto the screen. Specifying the
        optional -o option here outputs the registered allocations to a txt file.

        Usage: print_allocations [-o=filename]
        """
        Amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, args):
        """
        Prints a list of unallocated people to the screen. Specifying the -o
        option here outputs the information to the txt file provided.

        Usage: print_unallocated [-o=filename]
        """
        Amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Prints  the names of all the people in room_name on the screen.

        Usage: print_room <room_name>
        """
        Room().print_room(arg['<room_name>'])

    @docopt_cmd
    def load_state(self, args):
        """
        Loads data from a database into the application.

        Usage: load_state <sqlite_database>
        """
        load_state(args['<sqlite_database>'])

    @docopt_cmd
    def save_state(self, args):
        """
        Persists user session into the database

        Usage: save_state
        """
        save_state()

    @docopt_cmd
    def do_quit(self, arg):
        """
        Exits the application interface on the terminal

        Usage: quit
        """
        print('\n********** You have exited AlloAmity **********\n')
        exit()


if __name__ == '__main__':
    AlloAmity().cmdloop()
