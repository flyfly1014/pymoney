import sys

file_name="records.txt"

class Record:
    """Represent a record."""
    def __init__(self,category,description,amount):
        self._category=category
        self._description=description
        self._amount=int(amount)

    @property
    def category(self):
        return self._category
    
    @property
    def description(self):
        return self._description

    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        self._records=[]
        try:

            fh=open(file_name,'r')

            self._initial_money=int(fh.readline())
            for record in fh.readlines():
                category,decription,val=record.split()
                self._records.append(Record(category,decription,val))
            fh.close()
            print("Welcome back!\n")         
        except FileNotFoundError:
                try:
                    self._initial_money=int(input("How much money do you have?\n"))
                except ValueError:
                    sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                    self._initial_money=0
        except ValueError:
            # invalid format
            sys.stderr.write(f'Invalid format in {file_name}. Deleting the contents.\n')
            self._records = []
            try:
                self._initial_money = int(input("How much imoney do you have?:\n"))
            except ValueError:
                # invalid money
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                self._initial_money = 0
 
    def add(self,record,categories):
        """add a record"""
        try:
            category,des,amount=record.split(" ")
            assert categories.is_category_valid(category,categories)
            record=Record(category,des,amount)
            self._records.append(record) 
        except ValueError:
                sys.stderr.write('The format of a record should be like this:meal breakfast -50.\n')
                sys.stderr.write("Fail to add a record.\n")

        except AssertionError:
            sys.stderr.write("The specified category is not in the category list.\n")
            sys.stderr.write("You can check the category list by command 'view categories\n")
            sys.stderr.write("Fail to add a record.\n")
        
    def view(self):
        """output all records"""
        print(f"{'No':<{5}} {'category':<{15}} {'Description':^{20}} {'Amount':<{5}}")
        print("="*5+" "+"=" *15+" " + "="*20 + " "+"="*6)
        ans=0
        for pos,record in enumerate(self._records,start=1):
            print(f"{pos:<{5}} {record.category:<{15}} {record.description:<{20}} {record.amount:<{5}}")
            ans+=record.amount
        print("="*5+" "+"=" *15+" " + "="*20 + " "+"="*6)
        ans+=self._initial_money
        print(f"Now you have {ans} dollars.")

    def delete(self,delete_record):
        """delete a record"""
        try:
            position,category,description, amount = delete_record.split(" ")
            #index starts from 1
            position=int(position)-1
            amount=int(amount)
            assert(position < len(self._records) and records[position][0] == category \
            and self._records[position][2] ==description  and self._records[position][3]==amount)
            self._records.pop(position)
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")
        except (AssertionError,IndexError):
            sys.stderr.write("The record does not exist\n")
            sys.stderr.write("Fail to delete a record.\n")

    def find(self,subcategories):
        """find the records in subcategories"""
        new_records = filter(lambda x:x.category in subcategories, self._records)
        print("Here's your expense and income records under category \"food\":")
        ans=0
        print(f"{'category':<{15}} {'Description':^{20}} {'Amount':<{5}}")
        print("=" *15+" " + "="*20 + " "+"="*6)
        for record in new_records:
            if record[0] in target_categories:
                print(f"{record.category:<15}{record.description:<20}{record.amount:<6}")
                ans+=self.amount
        print("=" *15+" " + "="*20 + " "+"="*6)
        print(f"The total amount above is {ans}.")

    def save(self):
        try:
            with open(file_name, 'w') as fh:
                fh.write(f"{self._initial_money}")
                for record in self._records:
                    fh.writelines(f"{record.category} {record.description} {record.amount}\n")
            print("Finish Saving\n")
        except:
            sys.stderr.write("Fail to save\n")


class Categories:
    """Maintain the category list and provide some methods."""

    def __init__(self):
        """Initalizing Categories instance"""
        self._categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transport', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
    
    def view(self):
        """Print a category with proper indentation."""
        def rec_view(categories,level=0):
            if(type(categories) in {list, tuple}):
                for v in categories:
                    rec_view(v, level+1)
            else:
                s = " " *2* (level - 1) + "-"
                s += categories
                print(s)
        rec_view(self._categories)
        
    def is_category_valid(self, category, categories):
        if type(categories) == list:
            for child in categories:
                if self.is_category_valid(category, child):
                    return True
        else:
            return category == categories
        return False

    def find_categories(self, category, categories):
        """to find subcategories of category"""
        def find_categories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_categories_gen(category, child, found)
                    if child == category and index+1 < len(categories) and type(categories[index+1]) == list:
                        flag = True
                        for i in categories[index+1]:
                            yield from find_categories_gen(category, i, flag)
            else:
                if category == categories or found == True:
                    yield categories
        return [i for i in find_categories_gen(category, categories)]


categories=Categories()
records = Records()
 
while True:
    command = input('\nWhat do you want to do (add / ...)? ')
    if command == 'add':
        record = input('Add an expense or income record with ...:\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete?Please input the position,category,\
        description and amount")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_categories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
    	sys.stderr.write('Invalid command. Try again.\n')