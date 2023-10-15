import sqlite3

# create DataBase and tables

def create_data(): 
    connection = sqlite3.connect("recipy_book.db")

    #create first table

    sql_create_table = """
    CREATE TABLE recipy_full(
        recipy_name TEXT PRIMARY KEY,
        prep_time_mins INTEGER,
        cook_time_mins INTEGER,
        total_time_mins INTEGER,
        steps TEXT,
        ingredients TEXT,
        stars INTEGER
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql_create_table)
        connection.commit()
    except Exception as e:
        connection.rollback()

    steps = "Step 1: boil water \nStep 2: Add ramen noodles \nStep 3: cook for 5 mins \nStep 4: add seasoning and stir"
    ingredients = "ramen packet, 2 cups water"
    insert_into_full_table("ramen", 1, 5, steps , ingredients, 2)

    steps = "Step 1: line caserole dish w/slightly crushed doritos \nStep 2: layer chicken, sauce mix, and grated cheese\nStep 3: Bake 350 for 35 mins"
    ingredients = "2 cooked boned cubed chicken, 2 cans cream chicken soup, 1 can evaporated milk,\n 1 1/2 pkg doritos, 1 can diced tomatoes, 1 can cream mushroom soup,\n 1 1/2 cup chicken broth"
    insert_into_full_table("dorito casserole", 5, 35, steps , ingredients, 4)

    steps = "Step 1: mix together all ingredients \nStep 2: put in loaf pans(greased) \nStep 3: Bake 375 for 35-55 mins or until comes clean"
    ingredients = "3 cups flour, 1 cup vegetable oil, 3 eggs,\n 2 cups brown sugar, 3 tsp cinnamon, 4 bananas mashed,\n 1 tsp baking soda, 1 tsp vanilla, 1/4 tsp baking powder,\n 1 tsp salt"
    insert_into_full_table("banana bread", 15, 55, steps, ingredients, 3)

    steps = "Step 1: mix together sugar, coca, butter, and milk \nStep 2: Bring to a full boil, boil for 1 min \nStep 3: Remove from heat \nStep 4: Blend Peanut butter in \nStep 5: add oatmeal"
    ingredients = "2 cups sugar, 2 tbs coca, 1/2 cup butter,\n 1/2 cups milk, 3 cups oatmeal, 1/2 cup peanutbutter"
    insert_into_full_table("no bake cookies", 20, 1, steps, ingredients, 5)


def insert_into_full_table(recipy_name, prep_time_mins, cook_time_mins, steps, ingredients, stars):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()
    
    insert = "INSERT INTO recipy_full Values (\"" + recipy_name + "\", \"" + str(prep_time_mins) + "\", \"" + str(cook_time_mins) + "\", \"" + str(prep_time_mins + cook_time_mins) + "\",\"" + steps + "\",\"" + ingredients + "\", \"" + str(stars) + "\")"
    
    try:
        cursor = connection.cursor()
        cursor.execute(insert)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()

def get_recipies():
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_query = "SELECT * FROM recipy_full"

    rows = cursor.execute(sql_query)

    records = rows.fetchall()

    # print(records)
    return records

def query_total_time(time_start, time_end):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_query = "SELECT * FROM recipy_full WHERE total_time_mins BETWEEN \"" + str(time_start) + "\" AND \"" + str(time_end) + "\""

    rows = cursor.execute(sql_query)

    records = rows.fetchall()

    # print(records)
    # records[0][2]
    return records

def query_recipy_name(name):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_query = "SELECT * FROM recipy_full WHERE recipy_name=\"" + name + "\""

    rows = cursor.execute(sql_query)

    records = rows.fetchall()

    # print(records)
    # records[0][2]
    return records


def query_stars(stars_start):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_query = "SELECT * FROM recipy_full WHERE stars BETWEEN \"" + str(stars_start) + "\" AND \"5\""

    rows = cursor.execute(sql_query)

    records = rows.fetchall()

    return records

def delete_all():
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_drop = """
        DROP TABLE recipy_full
    """

    cursor.execute(sql_drop)
    connection.commit()

def delete_recipy(name):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_drop = "DELETE FROM recipy_full WHERE recipy_name=\"" + name + "\""

    cursor.execute(sql_drop)
    connection.commit()

def update_stars(name, stars):
    connection = sqlite3.connect("recipy_book.db")
    cursor = connection.cursor()

    sql_update = "UPDATE recipy_full SET stars = " + str(stars) + " WHERE recipy_name='" + name + "'"

    cursor.execute(sql_update)
    connection.commit()
    
def add_recipy():
    print("What is the recipy name: ")
    name = input()

    print("How long is the prep (mins): ")
    prep_time = input()

    print("How long does it cook (mins): ")
    cook_time = input()

    is_more = True
    step = 1
    steps = ""
    while(is_more):
        
        print("what is step " + str(step) + ": ")
        steps += "Step " + str(step) + ": " + input() + "\n"
        step += 1

        print("is there more Steps(y/n)? ")
        if(input().lower() == "n"):
            is_more = False
    
    is_more = True
    step = 1
    ingredients = ""
    while(is_more):
        print("list the Ingredients (1 at a time): ")
        ingredients += input() + ", "

        if(step % 3 == 0):
            ingredients += "\n"

        print("is there more Steps(y/n)? ")
        if(input().lower() == "n"):
            is_more = False

    print("How many stars do you give it (1-5): ")
    stars = input()
    
    insert_into_full_table(name, prep_time, cook_time, steps, ingredients, stars)

def total_time(name):
    recipy = query_recipy_name(name)
    print("\n" + str(recipy[0][3]) + " mins\n")
    input()

def print_recipy_book():
    book = get_recipies()

    print_recipies(book)
    input()

def print_recipies(book):
    
    for recipy in book:
        print_recipy(recipy[0])
        print("\n\n")

def print_recipy(name):
    recipy = query_recipy_name(name)
    print()
    print(recipy[0][0] + " - " + str(recipy[0][3]) + " mins - " + str(recipy[0][6]) + " stars\n")
    print(recipy[0][5])
    print()
    print(recipy[0][4])
    input("\n\npress enter to look at next Recipy\n\n")
        

def main():

    book_is_open = True
    user_input = ""

    while(book_is_open):
        print("Recipy Book")
        print("what action would you like to preform")
        print("1. look at full book")
        print("2. look at 1 recipy")
        print("3. look at recipies with at least X stars")
        print("4. edit stars for recipy")
        print("5. remove recipy")
        print("6. see total time for recipy")
        print("7. look at recipies between 2 times to prepare")
        print("8. add recipy")
        print("9. close book")


        try:
            user_input = int(input())
        except:
            print("please use an integer")
        if(user_input == 1):
            print_recipy_book()
        elif(user_input == 2):
            print("What is the name of the recipy?")
            print_recipy(input())
        elif(user_input == 3):
            user_input = ""
            while(isinstance(user_input, str)):
                print("What is the minimum stars you want to see: ")
                try:
                    user_input = int(input())
                    print_recipies(query_stars(user_input))
                except:
                    print("please use an integer")
        elif(user_input == 4):
            print("What is the name of the recipy?")
            recipy_name = input()
            print("How many stars does it deserve: ")
            stars = ""
            while(isinstance(stars, str)):
                stars = input()
                try:
                    stars = int(input())
                    update_stars(recipy_name, stars)
                except:
                    print("please use an integer")
                    print("How many stars does it deserve: ")
        elif(user_input == 5):
            print("What is the name of the recipy you want to remove?")
            delete_recipy(input())
        elif(user_input == 6):
            print("What is the name of the recipy?")
            total_time(input())
        elif(user_input == 7):
            time1 = ""
            time2 = ""
            while(isinstance(time1, str) and isinstance(time2, str)):
                try:
                    time1 = int(input("What is your shortest time?\n"))
                    time2 = int(input("What is your longest time?\n"))
                    print_recipies(query_total_time(time1, time2))
                except:
                    print("please use an integers for both inputs")
        elif(user_input == 8):
            add_recipy()
        elif(user_input == 9):
            book_is_open = False



"""uncomment if you want to reset recipy book"""
# delete_all()

# create_data()

main()