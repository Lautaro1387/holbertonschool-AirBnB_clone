#!/usr/bin/python3
"""The console"""
import cmd
import json
from models.engine.file_storage import FileStorage
from models.__init__ import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def create_update(clas):
    """Function for create"""
    if clas == "BaseModel":
        return BaseModel()
    if clas == "Amenity":
        return Amenity()
    if clas == "City":
        return City()
    if clas == "Place":
        return Place()
    if clas == "Review":
        return Review()
    if clas == "State":
        return State()
    if clas == "User":
        return User()


class HBNBCommand(cmd.Cmd):
    """Command interpreter"""
    prompt = '(hbnb) '
    ClassList = [
        "Amenity",
        "BaseModel",
        "City",
        "Place",
        "Review",
        "State",
        "User"
    ]

    def do_EOF(self, arg):
        """Quit command to exit the program"""
        exit()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        exit()

    def emptyline(self):
        """empty line"""
        pass

    def do_create(self, arg):
        """Create new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
        else:
            if arg in self.ClassList:
                new = create_update(arg)
                new.save()
                print("{}".format(new.id))
            else:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """
        The string representation of an instance based on the class name
        """
        line = arg.split(" ")
        my_dict = storage.all()
        if len(line) == 1 and line[0] == "":
            print("** class name missing **")
        else:
            if line[0] not in self.ClassList:
                print("** class doesn't exist **")
                return
            elif len(line) == 1:
                print("** instance id missing **")
                return
            for obj in my_dict:
                line2 = obj.split(".")
                if line2[1] == line[1] and line2[0] == line[0]:
                    print("{}".format(my_dict[obj]))
                    return
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name"""
        line = arg.split(" ")
        if len(line) == 1 and line[0] == "":
            print("** class name missing **")
            return
        if len(line) < 2:
            print("** instance id missing **")
            return
        if line[0] not in self.ClassList:
            print("** class doesn't exist **")
            return
        try:
            my_dict = storage.all()
            key = line[0] + '.' + line[1]
            my_dict[key]
        except Exception:
            print("** no instance found **")
            return
        with open('file.json', 'w') as f:
            del my_dict[key]
            f.write(json.dumps(my_dict, default=str))
            storage.reload()

    def do_all(self, arg):
        """Prints all string representation based or not on the class name"""
        lis = []
        line = arg.split(" ")
        my_dict = storage.all()
        if len(line) < 1 or line[0] == "":
            for i in my_dict:
                lis.append(str(my_dict[i]))
            print(lis)
            return
        if line[0] not in self.ClassList:
            print("** class doesn't exist **")
            return
        for obj in my_dict:
            line2 = obj.split(".")
            if line2[0] == line[0]:
                lis.append(str(my_dict[obj]))
        print(lis)

    def do_update(self, arg):
        """Updates an instance based on the class name"""
        line = arg.split(" ")
        my_dict = storage.all()
        if len(line) == 1 and line[0] == "":
            print("** class name missing **")
            return
        if line[0] not in self.ClassList:
            print("** class doesn't exist **")
            return
        if len(line) < 2:
            print("** instance id missing **")
            return
        if len(line) < 3:
            print("** attribute name missing **")
            return
        if len(line) < 4:
            print("** value missing **")
            return
        for obj in my_dict:
            line2 = obj.split(".")
            if line2[1] == line[1]:
                dictt = my_dict[line[0] + '.' + line[1]]
                break
        else:
            print("** no instance found **")
            return
        dictt.__dict__[line[2]] = line[3]
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
