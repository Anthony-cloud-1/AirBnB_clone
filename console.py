#!/usr/bin/python3
"""Defines the HBnB console using cmd."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State
from models.city import City

def parse(arg):
    curlbraces = re.search(r"\{(.*?)\}", arg)
    braces = re.search(r"\[(.*?)\]", arg)
    if curlbraces is None:
        if braces is None:
            return [i.strip(",") for i in split(arg)]
        else:
            spliter = split(arg[:braces.span()[0]])
            stripper = [i.strip(",") for i in spliter]
            stripper.append(braces.group())
            return stripper
    else:
        spliter = split(arg[:curlbraces.span()[0]])
        stripper = [i.strip(",") for i in spliter]
        stripper.append(curlbraces.group())
        return stripper


class HBNBCommand(cmd.Cmd):
    """HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The cmd prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, arg):
        """Default behavior for cmd module when input is unrecognized"""
        dict_arg = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        pair = re.search(r"\.", arg)
        if pair is not None:
            argmat = [arg[:pair.span()[0]], arg[pair.span()[1]:]]
            pair = re.search(r"\((.*?)\)", argmat[1])
            if pair is not None:
                cmd = [argmat[1][:pair.span()[0]], pair.group()[1:-1]]
                if cmd[0] in dict_arg.keys():
                    call_up = "{} {}".format(argmat[0], cmd[1])
                    return dict_arg[cmd[0]](call_up)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the CLI."""
        return True

    def emptyline(self):
        """Do nothing on receiving an empty line."""
        pass

    def do_EOF(self, arg):
        """Handle EOF signal."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new instance of the class and print its id.
        """
        argmat = parse(arg)
        if len(argmat) == 0:
            print("** class name missing **")
        elif argmat[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argmat[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Print the string representation of a class instance for a given id.
        """
        argmat = parse(arg)
        o_dict = storage.all()
        if len(argmat) == 0:
            print("** class name missing **")
        elif argmat[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argmat) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argmat[0], argmat[1]) not in o_dict:
            print("** no instance found **")
        else:
            print(o_dict["{}.{}".format(argmat[0], argmat[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance for a given id."""
        argmat = parse(arg)
        o_dict = storage.all()
        if len(argmat) == 0:
            print("** class name missing **")
        elif argmat[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argmat) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argmat[0], argmat[1]) not in o_dict.keys():
            print("** no instance found **")
        else:
            del o_dict["{}.{}".format(argmat[0], argmat[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Print string representations of all instances for a given class.
        If no class is specified, prints all instantiated objects."""
        argmat = parse(arg)
        if len(argmat) > 0 and argmat[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            list_obj = []
            for obj in storage.all().values():
                if len(argmat) > 0 and argmat[0] == obj.__class__.__name__:
                    list_obj.append(obj.__str__())
                elif len(argmat) == 0:
                    list_obj.append(obj.__str__())
            print(list_obj)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances for a given class."""
        argmat = parse(arg)
        counter = 0
        for obj in storage.all().values():
            if argmat[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance for a given id by adding or updating
        a given attribute key-value pair or dictionary."""
        argmat = parse(arg)
        o_dict = storage.all()

        if len(argmat) == 0:
            print("** class name missing **")
            return False
        if argmat[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argmat) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argmat[0], argmat[1]) not in o_dict.keys():
            print("** no instance found **")
            return False
        if len(argmat) == 2:
            print("** attribute name missing **")
            return False
        if len(argmat) == 3:
            try:
                type(eval(argmat[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argmat) == 4:
            obj = o_dict["{}.{}".format(argmat[0], argmat[1])]
            if argmat[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[argmat[2]])
                obj.__dict__[argmat[2]] = value_type(argmat[3])
            else:
                obj.__dict__[argmat[2]] = argmat[3]
        elif type(eval(argmat[2])) == dict:
            obj = o_dict["{}.{}".format(argmat[0], argmat[1])]
            for key, val in eval(argmat[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(val)
                else:
                    obj.__dict__[key] = val
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
