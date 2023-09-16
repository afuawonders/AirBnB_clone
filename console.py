#!/usr/bin/python3
""" Defines the console class
which is the entry point of the Airbnb Project
"""


import cmd
from models import storage
from models.engine.errors import *
import shlex
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel
from models.user import User
from models.state import State


classes = storage.models


class HBNBCommand(cmd.Cmd):
    """ does various HBNB commands """
    prompt = "(hbnb) "

    # Commands

    def do_EOF(self, args):
        """Exits the programme in non-interactive mode"""
        return True

    def do_quit(self, args):
        """Quits command that closes the programme"""
        return True

    def emptyline(self):
        """Overides empty line to do nothing """
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel, 
        saves it (to the JSON file) and prints the id
        """
        args, number = parse(args)
        if not number:
            print("** class name missing**")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif number == 1:
            # temp = classes[args[0]]()
            temp = eval(args[0])()
            # print(temp)
            print(temp.id)
            temp.save()
        else:
            print("** Too many argument for create **")
            pass

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and"""
        args, number = parse(arg)

        if not number:
            print("** class name missing **")
        elif number == 1:
            print("** instance id missing **")
        elif number == 2:
            try:
                inst = storage.get_instance_by_id(*args)
                print(inst)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for show **")
            pass

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args, number = parse(arg)

        if not number:
            print("** class name missing **")
        elif number == 1:
            print("** instance id missing **")
        elif number == 2:
            try:
                storage.remove_instance_by_id(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for destroy **")
            pass

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name"""
        args, number = parse(args)

        if number < 2:
            try:
                print(storage.get_all_instances(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many argument for all **")
            pass

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute"""
        args, number = parse(arg)
        if not number:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class name missing **")

        elif number == 1:
            print("** instance id missing **")
        elif number == 2:
            print("** attribute name missing **")
        elif number == 3:
            print("** value missing **")
        else:
            try:
                storage.modify_instance(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")

    def default(self, arg):
        """Override default method to handle class methods"""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in classes:
                print("** class doesn't exist **")
                return
            return self.handle_class_methods(arg)
        return cmd.Cmd.default(self, arg)

    # def do_models(self, arg):
    #     """Print all registered Models"""
    #     print(*classes)

    def handle_class_methods(self, arg):
        """Handle Class Methods
        <cls>.all(), <cls>.show() etc
        """

        printable = ("all(", "show(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printable:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")
            pass


def parse(line: str):
    """Splits lines by spaces"""
    args = shlex.split(line)
    return args, len(args)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
