from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value
    def __str__(self) -> str:
        return f'{self.value}'
    def __eq__(self, other) -> bool:
        return self.value == other.value #otherwise python uses is and returns False when comparing two objects, here we specify that we want to compare value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: Name, phones=[]) -> None:
        self.name = name
        self.phones = phones
    
    def __str__(self) -> str:
        return f'User: {self.name} Phone(s): {", ".join([phone.value for phone in self.phones])}'

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def delete_phone(self, phone: Phone) -> None:
        self.phones.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phones.remove(phone)
        self.phones.append(new_phone)

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

class PhoneExists(Exception):
    pass

class InputError:
    def __init__(self, func) -> None:
        self.func = func
    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except ValueError:
            return "The phone number you entered is not correct"
        except KeyError:
            return "There is no such user"
        except IndexError:
            return "Your entry should include a name and a phone"
        except PhoneExists:
            return "This phone already exists in the address book"

def hello_func(*args):
    return "Hello! How can I help you?"

@InputError
def add(contacts, *args): # when you add name and phone it adds the contact to the address book
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in contacts:
        if phone in contacts[name.value].phones:
            raise PhoneExists
        else:
            contacts[name.value].add_phone(phone)
    else:
        contacts[name.value] = Record(name, [phone])
        return f'Added {phone} to user {name}'

@InputError
def change_phone(contacts, *args): #when you enter user's name and phone it chnages it to the new one
    name = args[0]
    phone = args [1]
    new_phone = args[2]
    contacts[name].edit_phone(Phone(phone), Phone(new_phone))
    print(contacts[name])
    return f'Phone {phone} changed to {new_phone} for {name}'

@InputError
def phone(contacts, *args): # when you enter user's name it returns users phones
    name = args[0]
    phone = contacts[name]
    return f'{phone}'

@InputError
def show_all(contacts, *args): #shows all contacts in address book
    result = ""
    for key in contacts:
        result = result + f' {contacts[key]}'
    return result

def exit(*args):
    return "Good bye!"

COMMANDS = {hello_func:["hello"], exit:["exit", ".", "bye"], add:["add", "добавь", "додай"], change_phone:["change"], phone:["phone"], show_all:["show all", "show"]}


def parse_command(user_input: str):
    for k,v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")
            

def main():
    contacts = AddressBook()
    while True:
        user_input = input(">>>")
        result, data = parse_command(user_input)
        print(result(contacts, *data), '\n')
        if result is exit:
            break

if __name__ == '__main__':
    main()

        
# 1 Adds a phone to existing record
#record_1 = Record("Kate", [1223])
#record_1.add_phone(456)
#print(record_1.phones)

# 2 Deletes a phone from existing record
#record_2 = Record("Sophia", [123, 437])
#record_2.delete_phone(437)
#print(record_2.phones)

# 3 Changes a phone in the record
#record_3 = Record("Sergii", [567, 789])
#record_3.change_phone(567, 5567)
#print(record_3.phones)








        
