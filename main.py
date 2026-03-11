# #print("hello noori\nhow are you")
# #name = input("what is your name? ")
# #print(len(name))
# #a = input("a: ") #to switch values with each other
# #b = input("b: ")
# #c = a
# #a = b
# #b = c
# #print("a = "+ a)
# #print("b = "+ b)
# #two_digit_number = input("two digit number = ")
# #first_digit = int(two_digit_number[0])
# #second_digit = int(two_digit_number[1])
# #result = (first_digit) + (second_digit)
# #print(first_digit, "+" ,second_digit ,"=" ,result)
# #score = 1
# #team = "argentina"
# #iswinning = True
# #print(f"your'e score is {score}, your'e team is {team}, and your'e winning is {iswinning}")
# #number = int(input("enter the number"))
# #if number % 2 == 0:
#  #   print("this is an even  number")
# #else:
#  #   print("this is an odd number")
# #height = int(input("enter your height: "))
#
# #nested and multiple elif
#
# #bill = 0
# #if height >=120:
#     #print("you can ride")
#     #age =int(input("enter your age: "))
#     #if age<=12:
#       #  bill = 50
#      #   print("child ticket is 50Rs")
#     #elif age<=18:
#       #  bill = 100
#      #   print("youth ticket is for 100Rs")
#     #elif age>=18:
#       #  bill = 150
#      #   print("your adult ticket is for 150Rs")
#     #want_photo = input("do you want pic y/n: ")
#     #if want_photo == "y":
#         #bill+=30
#        # print(f"your total bill is {bill}")
# #else:
#    # print("you can't ride")
#
# # Randomisation [random module]
# #import random
# #randomInteger = random.randint(1,10)
# #print(randomInteger)
# #randomFloat = random.random() * 5
# #print(randomFloat)
#
# #randomCoin_side = random.randint(0,1) #head or tail
# #if randomCoin_side == 1:
#  #   print("head")
# #else:
#  #   print("Tail")
# #lists >>[item1,item2]
#Indian_states = ["Delhi","Mumbai","Bangalore","Kolkata","Uttar pradesh","Bihar","Harayana","Tamil Nadu"]
# print(Indian_states[2])
# My_states = Indian_states[4]
# print(My_states)
#Indian_states.append("Punjab") # to add single data in list
#print(Indian_states)
#print(Indian_states.)
# W=["Rajasthan","Gujarat","Goa"]
# Indian_states.append(W)
# Indian_states.extend(["Rajasthan","Gujarat","Goa"]) # to add group of data in a list use .extend
# print(Indian_states)
#
# #import random
# #names_string = input("Give me the names,seperated by comma. ")
# #names = names_string.split(", ")
# #num_items = len(names)
# #randomNames = random.randint(0,num_items-1)
# #person_who_will_pay = names[randomNames]
# #print(f"{person_who_will_pay} is going to pay the bill")
# #alpha = ["a","b","c"]
# #num = [1,2,3]
# #alpha_num = [alpha,num]
# #print(alpha_num)
# # ROCK PAPER SCISSOR GAME
# import random
# rock = "🪨"
# paper = "📝"
# scissor = "⚔"
# game_images = [rock,paper, scissor]
# user_choice = int(input("what do you choose? Type 0 for rock, 1 for paper, 2 for scissor.\n"))
# print("you chose:")
# print(game_images[user_choice])
# computer_choice = random.randint(0,2)
# print("computer chose")
# print(game_images[computer_choice])
# if user_choice >=3 or user_choice <0:
#     print("you typed invalid number, you lose ")
# elif user_choice == 0 and computer_choice == 2:
#     print("you win")
# elif computer_choice == 0 and user_choice == 2:
#     print("you loose")
# elif computer_choice > user_choice:
#     print("You lose")
# elif user_choice > computer_choice:
#     print("you win")
# elif computer_choice == user_choice:
#     print("it's a draw, play again")
#
# #For loop
# #student_heights = (input("Input a list of student heights: ")).split()
# #for n in range(0,len(student_heights)):
#  #   student_heights[n] = int(student_heights[n])
# #print(student_heights)
# #total_height = 0
# #for height in student_heights:
#  #   total_height +=height
# #print(total_height)
# #number_of_students = 0
# #for students in student_heights:
#  #   number_of_students +=1
# #print(total_height/number_of_students)
# #total = 0
# #for n in range(2,101,2):
#  #   total += n
# #print(total)
# #PYPASSWORD GENERATOR
#
# import random
# letters = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M"]
# numbers = ["1","2","3","4","5","6","7","8","9","0"]
# symbols = ["!","@","#","$","%","^","&","*","~"]
# print("welcome to pypassword generator!")
# nr_letters = int(input("how many letters do you want in your password?\n"))
# nr_numbers = int(input("how many numbers would you like in your paasword?\n"))
# nr_symbols = int(input("how many symbols would you like?\n"))
# password_list = []
# for char in range(0,nr_letters):
#    password_list +=random.choice(letters)
# for char in range(0,nr_numbers):
#    password_list += random.choice(numbers)
# for char in range(0,nr_symbols):
#    password_list += random.choice(symbols)
# #print(password_list)
# random.shuffle(password_list)
# #print(password_list)
# password =""
# for char in password_list:
#    password += char
# print(password)
#
# #PYTHON FNCTIONS It is used to package set of instructions in one line
# #def my_function():   #defining a function
#  ##  print("bye")
# #my_function()  #calling a function
# #HANGMAN PROJECT
# #step 1
# hangman = ["""
#    ________
#    |/   |
#   |   (_)
#     |   /|\
#     |    |
#     |   / \
#     |
#     |___
#     HANGMAN""",
#            """
#     ________
#     |/   |
#     |   (_)
#     |   /|\
#     |    |
#     |   /
#    |
#     |___
#      HANGMA""",
#            """
#               _________
#                |/   |
#                |   (_)
#                |   /|\
#                |    |
#                |
#                |
#                |___
#                HANGM""",
#            """
#               _________
#                |/   |
#                |   (_)
#                |   /|
#                |    |
#                |
#                |
#                |___
#                HANG""",
#
#           """
#               ________
#                |/   |
#                |   (_)
#                |    |
#                |    |
#                |
#                |
#                |___
#                HAN""",
#            """
#              _________
#                |/   |
#                |   (_)               |
#               |
#                |
#                |
#                |___
#                HA""",
#
#            """
#               _________
#                |/
#                |
#                |
#                |
#                |
#       ++ ++        |
#                |___
#               """
#           ]
# chances = 7
# end_of_game = False
# word_list =["india",'australia',"canada","america","nepal","korea","amsterdam","pakistan","switzerland"]
# import random
# chosen_word = random.choice(word_list)
# print(f"the chosen word is a country name :")
# #step 2
# display = []
# for letter in chosen_word:
#     display +="_"
# print(display)
# while not end_of_game:
#     guess = input("Guess a letter: ").lower()
# #step 3
#     for position in range(len(chosen_word)):
#         letter = chosen_word[position]
#         if letter == guess:
#             display[position] = letter
#     print(display)
#
# #step 4 condition to stop while loop
#     if guess not in chosen_word:
#         chances -= 1
#         print(hangman[chances])
#         print(f"{chances} chances left")
#         if chances == 0:
#             end_of_game == True
#             print("YOU LOOSE, man is hanged.")
#             print("WANNA TRY AGAIN ?")
#             break
#     if "_" not in display:
#        end_of_game = True
#        print("YOU SAVED THE MAN")
#        print(f"The chosen word was {chosen_word}.")
# # step 5
# # ENJOY THE GAME
#
# #def greet(name,name2):
# #   print(f"hello {name}")
# #   print(f"you are with {name2}")
# #greet(name="N",name2="A")
#
# #test_h = int(input("height of the wall: "))
# #test_w = int(input("width of the wall: "))
# #test_c = int(input("coverage: "))
# #def paint_calc(height,width,coverage):
# #    no_of_can = height*width/coverage
# #    total_no_of_can = round(no_of_can)
# #    print(f"you need {total_no_of_can} can")
# #paint_calc(height=test_h,width=test_w,coverage=test_c)
# #def prime_checker(number):
# #    for i in range(2,number):
# #        if number % i == 0:
# #            print("It's not a prime number.")
# #            break
# #    else:
# #        print("It's a prime number.")
# #n = int(input("check this number: "))
# #prime_checker(number= n)
# # CAESER CIPHER - it's a method to encrypt a message or password
# alphabet =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
# text = input("Type your message:\n").lower()
# shift = int(input("Type the shift number:\n"))

# def caesar(start_text,shift_amount,cipher_direction):
#     end_text = ""
#     if cipher_direction == "decode":
#        shift_amount *= -1
#        for letter in start_text:
#           position = alphabet.index(letter)
#           new_postion = position + shift_amount
#           end_text += alphabet[new_postion]
#        print(f"The {cipher_direction} text is {end_text}")
# #         # OR YOU CAN USE THIS WAY
# caesar(start_text=text,shift_amount=shift,cipher_direction=direction)
# def encrypt(plain_text,shift_amount):
#     cipher_text =""
#         for letter in plain_text:
#             position =alphabet.index(letter)
#             new_position = position+ shift_amount
#             new_letter = alphabet[new_position]
#             cipher_text += new_letter
#    print(f"encoded message is {cipher_text}")
#
# def decrypt(cipher_text,shift_amount):
#    plain_text = ""
#    for letter in cipher_text:
#        position = alphabet.index(letter)
#        new_position = position - shift_amount
#        plain_text += alphabet[new_position]
#    print(f"the message is {plain_text}")
# decrypt(cipher_text=text,shift_amount=shift)
# if direction == "encode":
#    encrypt(plain_text=text,shift_amount=shift)
# elif direction == "decode":
#    decrypt(cipher_text=text,shift_amount=shift)
# else:
#    print("You typed it wrong,try again")
#
# #DICTIONARY {key : value} remeber each key can have only one value
# #life_dictionary = {
# # "birth":"you come to the world",
# # "learning":"you learn many things, some are bitter but important too",
# # "death":"you leave the world",
# #  786:"kind of good"
# #}
# #print(life_dictionary["learning"])
# #Adding new items to dicitionary or to edit items in dictionary
# #life_dictionary["always_remember"] = "Never ever betray your friend"
# #print(life_dictionary)
#
# #to wipe an existing dicitionary
# # dicitonary name = {} (syntax)
# #student_scores ={
# #    "H":81,
# #    "R":78,
# #    "D":99,
# #    "N":95,
# #}
# #student_grades ={}
# #for student in student_scores:
# #    score = student_scores[student]
# #    if score > 90:
# #        student_grades[student] = "A+"
# #    elif score > 80:
# #        student_grades[student] = "A"
# #    else:
# #        student_grades[student] = "Average"
# #print(student_grades)
# #nesting list in dictionary
# #travel_log = {
# #    "France" : ["Paris","Lille","Dijon"]
# #    "Germany" : ["Berlin","Hamburg"]
# #}
# # Nesting dictionary in a dictionary
# #travel_log = {
# #    "France" :{ "cities visited" : ["Paris","Lille","Dijon"]},
# #    "Germany" : ["Berlin","Hamburg"]
# #}
# #print(travel_log["Germany"])
# #adding piece of data(dicitionary) in list containing dicitionary
# #travel_log = [
# #    {
# #        "Country" : "Germany",
# #        "visits" : 4,
# #        "Cities" : ["Berlin","Hamburg","Stuttgart"]
# #    }
# #]
# #def add_new_country(country_visited,time_visited,cities_visited):
# #    new_country ={}
# #    new_country["country"] = country_visited
# #    new_country["visits"] = time_visited
# #    new_country["cities"] = cities_visited
# #    travel_log.append(new_country)
#
# #add_new_country("Russia",2,["Moscow","Saint Petersburg"])
# #print(travel_log)
#
# #Bidding project
# #print("Welcome to the Bid\n")
# #bids ={}
# #bidding_finished = False
#
# #def find_highest_bidder(bidding_record):
# #    highest_bid = 0
# #    winner =""
# #    for bidder in bidding_record:
# #        bid_amount = bidding_record[bidder]
# #        if bid_amount > highest_bid:
# #            highest_bid = bid_amount
# #            winner = bidder
# #    print(f"The winner is {winner} with a bid of Rs {highest_bid}")
# #while not bidding_finished:
# #    name = input("Enter your Name: ")
# #    price = int(input("enter your Bid: Rs "))
# #    bids[name] = price
# #    should_continue = input("Is there anyone else to bid?  type 'yes' or 'no'\n")
# #    if should_continue == "no":
# #        bidding_finished = True
# #        find_highest_bidder(bids)
# # Function with output -- return
# # def format_name(f_name,l_name):
# #     if f_name == "" or l_name == "":
# #         return "you didn't provide valid input"
# #     formated_f_name = (f_name.title())  # '.title()' converts first letter to caps and other letter to small letters
# #     formated_l_name = (l_name.title())
# #     return f"{formated_f_name} {formated_l_name}"
# # formated_string = format_name(input("Enter your first name: "),input("Enter your last name: "))
# # print(formated_string)
# calculator
# def add(n1,n2):
#     return n1+ n2
# def sub(n1,n2):
#     return n1-n2
# def multiply(n1,n2):
#     return n1*n2
# def divide(n1,n2):
#     return n1 / n2
# operations = {"+":add,
#               "-" : sub,
#               "*":multiply,
#               "/":divide}
# def calculator():
#     num1 = float(input("What's the first number: "))
#     for operator in operations:
#         print(operator)
#     should_contine = True
#     while should_contine:
#         operator = input("Pick an operation : ")
#         num2 = float(input("what's the next number: "))
#         calculation_function = operations[operator]
#         answer = calculation_function(num1,num2)
#         print(f"{num1} {operator} {num2} = {answer}")
#         perform_again = input(f"Type 'y' to contine calculating with {answer}, or type 'n' to start a new calculation : ")
#         if perform_again == "n":
#             should_contine = False
#             calculator()
#         else:
#             num1 = answer
#
# calculator()
# ## BLACKJACK/21 PROJECT
# # import random
# # def deal_cards():
# #     """returns a random card from deck"""
# #     cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]
# #     card = random.choice(cards)
# #     return card
# # def play_game():
# #     user_card = []
# #     computer_card =[]
# #     game_over = False
# #     for i in range(2):
# #          user_card.append(deal_cards())
# #          computer_card.append(deal_cards())
# #     def calculate_score(cards):
# #        if sum(cards)==21 and len(cards) == 2:
# #            return 0
# #        if 11 in cards and sum(cards) > 21:
# #            cards.remove(11)
# #            cards.append(1)
# #        return sum(cards)
# #     while not game_over:
# #         user_score = calculate_score(user_card)
# #         computer_score = calculate_score(computer_card)
# #         print(f"Your cards:{user_card},\nyour score is {user_score}")
# #         print(f"computer's first card:{computer_card[0]},")
# #         if user_score == 0 or computer_score == 0 or user_score > 21:
# #                 game_over = True
# #         else:
# #             user_should_deal=input("Type 'y' to draw another card, type 'n' to pass: ")
# #         if user_should_deal == 'y':
# #             user_card.append(deal_cards())
# #         else:
# #             game_over = True
# #     def compare(user_score,computer_score):
# #         if user_score == computer_score:
# #             return "Draw"
# #         elif computer_score == 0:
# #             return "You lose! opponent has a blackjack"
# #         elif user_score == 0:
# #             return "You win with a Blackjack"
# #         elif user_score >21:
# #             return "You lose! because your score is >21"
# #         elif computer_score > 21:
# #             return "You Win"
# #         elif user_score > computer_score:
# #             return "you win"
# #         else:
# #             return "You lose"
# #     while computer_score != 0 and computer_score < 17:
# #         computer_card.append(deal_cards())
# #         computer_score = calculate_score(computer_card)
# #     print(f"Your score is {user_score}, computer score is {computer_score}")
# #     print(compare(user_score,computer_score))
# # while input("Do you want to play again? type 'y' or 'n': ") == 'y':
# #     play_game()
# # else:
# #     game_over = True
# """ FOR ASCII WE CAN USE PATORJK.COM WEBSITE"""
# # NUMBER GUESSING GAME
# logo = """ _____ _     _____ ____  ____    _____  _     _____   _      _     _        ____  __
# /  __// \ /\/  __// ___\/ ___\  /__ __\/ \ /|/  __/  / \  /|/ \ /\/ \__/|  /  _ \/  __//  __\
# | |  _| | |||  \  |    \|    \    / \  | |_|||  \    | |\ ||| | ||| |\/||  | | //|  \  |  \/|
# | |_//| \_/||  /_ \___ |\___ |    | |  | | |||  /_   | | \||| \_/|| |  ||  | |_\\|  /_ |    /
# \____\\____/\____\\____/\____/    \_/  \_/ \|\____\  \_/  \|\____/\_/  \|  \____/\____\\_/\_\
#                                                                                              """
# print(logo)
# print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
# EASY_LEVEL_TURNS =10
# HARD_LEVEL_TURNS =5
#
# import random
# def game():
#     def check_number(guess,number,turns):
#         if guess > number:
#             print("too high")
#             return turns -1
#
#         elif guess < number:
#             print("Too low")
#             return turns -1
#
#         else:
#             print(f"You got it! the number was {number}.")
#     number = random.randint(1,100)
#     #print(f"the number is {number}")
#     def set_difficulty():
#         user_option = input("choose a difficulty. Type 'easy' or 'hard': ")
#         if user_option == 'easy':
#             return EASY_LEVEL_TURNS
#         else:
#             return HARD_LEVEL_TURNS
#     turns = set_difficulty()
#     guess = 0
#     while guess!=number:
#         print(f"You have {turns} attempts left to guess a number.")
#         guess = int(input("Make a guess: "))
#         turns = check_number(guess,number,turns)
#         if turns== 0:
#             print("you lost")
#             return
# game()
# """ INTERMEDIATE"""
# # "OOP"
# """ it is a method of spliting task, ehich consisit class and object. eg: teacher is a class and x,y,z are objects"""
# """ syntax : car = carblueprint()   car is object and carblueprint is class"""
# # from turtle import Turtle,Screen # tutrle is a module and Turtle is a class in a turtle module
# # zombies =Turtle()
# # zombies.shape("turtle") #this is used to change shape
# # zombies.color("blue")  #this is used to change colour
# # zombies.forward(100)
# # my_screen = Screen()              #Screen() function is used as place or screen where our work will be shown
# # my_screen.exitonclick()            #exitonclick is a function that holds the screen and exits when it detects a click
# """object attributes, attributes means features of objects or a variable associated with objects"""
# #syntax is object.attribute
#
# """functions when tied with an object is called methods"""
# #syntax is object.function()
# """Python Packages""" "you can find lot of packages in pypi.org website"
# # packages are bunch of code written by different coders for everyone's use and we can use for our project.
# """ CREATING A CLASS"""
# #syntax class classname:
# # class User:
# #     def __init__(self,user_id,user_name):                     #__init__ is used to initialise the attribute
# #         self.id = user_id
# #         self.name = user_name
# #         self.follower = 0                   #this makes the follower value 0 as default
# #
# # user_1 = User("001","Aryan")
# # user_2 = User("002","Amit")
# #
# # User_1 = User()
# # user_1.id = "001"
# # user_1.name = "xyz"
# # print(user_2.name,user_2.follower)
#
# # Open/create the file in write mode
# file = open("naveen.py", "w")
#
# # Write content to the file
# file.write("print('Hello, Naveen!')\n")
#
# # Close the file
#
#
# # Confirmation message
# print("File 'naveen.py' has been created successfully.")
#
# def find_file_in_records(file_name, records):
#     for record in records:
#         if file_name in record:
#             return True
#     return False
#
# # Open the file and read the records
# file = open("naveen.py", "r")
# lines = file.readlines()
# file.close()
#
# # List of records
# records = ["naveen.py"]
# for line in lines:
#     records.append(line.strip())
#
# # Prompt the user for a file name to search
# search_file_name = input("Enter the file name to search: ")
#
# # Call the function to find the file in the records
# found = find_file_in_records(search_file_name, records)
#
# # Display the result
# if found:
#     print(f"The file '{search_file_name}' is found in the records.")
# else:
#     print(f"The file '{search_file_name}' is not found in the records.")
# # Open the file in read mode
# file = open("naveen.py", "r")
#
# # Read lines from the file
# lines = file.readlines()
#
# # Close the file
# file.close()
#
# # Process the lines and display student names and marks
# for line in lines:
#     # Split the line into name and marks
#     data = line.strip().split(",")
#     if len(data) == 2:
#         name = data[0]
#         marks = data[1]
#         print("Name:", name)
#         print("Marks:", marks)
#         print("-------------------")
#
# def create_file(): #1
#     file_name = input("Enter the file name: ")
#     file = open(file_name, "w")
#     file.close()
#     print(f"File '{file_name}' created successfully.")
#
#
# def write_to_file(): #2
#     file_name = input("Enter the file name: ")
#     num_students = int(input("Enter the number of students: "))
#
#     file = open(file_name, "w")
#
#     for _ in range(num_students):
#         student_name = input("Enter student name: ")
#         student_marks = input("Enter student marks: ")
#         file.write(f"""Student name            student marks
#         {student_name}     :        {student_marks}\n""")
#
#     file.close()
#     print(f"Data written to '{file_name}' successfully.")
#
#
# def open_file(): #3
#     file_name = input("Enter the file name: ")
#     file = open(file_name, "r")
#     print("File contents:")
#     print(file.read())
#     file.close()
#
#
# # Main program loop
# while True:
#     print("1. Create a file")
#     print("2. Write student data to a file")
#     print("3. Open and view a file")
#     print("4. Quit")
#
#     choice = input("Enter your choice (1-4): ")
#
#     if choice == "1":
#         create_file()
#     elif choice == "2":
#         write_to_file()
#     elif choice == "3":
#         open_file()
#     elif choice == "4":
#         break
#     else:
#         print("Invalid choice. Please try again.\n")
#
# print("Program terminated.")

# Importing required libraries
# NumPy (Your Super Calculator), Scikit-learn (Your AI Playground),  Matplotlib (Your Visual Storyteller)
import numpy as np  # We import numpy and call it np (short and cool!)
# What is NumPy?
# Python’s built-in lists are cool, but when you want to do fast math on large data, they get slow and clunky.
# NumPy gives you powerful arrays that are like supercharged lists — optimized for math and scientific computing.
# Create a simple NumPy array (like a list)
# Lists can hold different data types; arrays hold same type (usually numbers).
#
# Arrays allow fast math operations on all elements at once.
#
# Arrays have a shape (dimensions).
# numbers = np.array([10, 20, 30, 40])
# print(numbers)
# arr = np.array([1, 2, 3, 4, 5])
#
# print("Sum:", arr.sum())        # Adds all elements → 15
# print("Mean:", arr.mean())      # Average → 3.0
# print("Std Dev:", arr.std())    # Spread of data
# print("Min:", arr.min())        # Smallest number → 1
# print("Max:", arr.max())        # Largest number → 5
# matrix = np.array([[1, 2, 3],
#                    [4, 5, 6]])
# #
# print("Sum all elements:", matrix.sum())
# print("Sum each column:", matrix.sum(axis=0))  # [5 7 9]
# print("Sum each row:", matrix.sum(axis=1))     # [6 15]

# # axis=0 means down columns
# axis=1 means across rows
# a = np.array([1, 2, 3,10])
# b = np.array([4, 5, 6,9])
# #
# print("Dot product:", np.dot(a, b))  # 1*4 + 2*5 + 3*6 = 32
# print("Square root:", np.sqrt(arr))      # [1. 1.41 1.73 2. 2.24]
# print("Exponential:", np.exp(arr))      # e^x for each element
# print("Logarithm:", np.log(arr))        # natural log (ln)
# print("Round:", np.round(np.array([1.2, 2.8, 3.5])))

# Mini Project: Analyze Exam Scores
# scores = np.array([78, 85, 62, 90, 88])
# print(scores +1)
# # Find average score
# print("average:", np.average(scores))
# avg= np.average(scores)
# # Find highest and lowest score
# print("highest:", np.max(scores))
# print("lowest:", np.min(scores))
# # Calculate standard deviation
# print("standard deviation:", np.std(scores))
# # Print a message if the average is above 80 (“Great class!”) or below (“Needs improvement.”)
# if avg>80:
#     print("great class!")
# else:
#     print("needs improvement!")


# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats, fft
# import urllib.request
#
# # Step 1: Download dataset
# url = "https://raw.githubusercontent.com/datasets/co2-ppm/main/data/co2-mm-mlo.csv"
# urllib.request.urlretrieve(url, "co2.csv")
#
# # Load dataset (skip header)
# data = np.genfromtxt("co2.csv", delimiter=",", skip_header=1, dtype=str)
#
# # Process years into fractional years
# years = np.array([float(date.split("-")[0]) + (float(date.split("-")[1]) - 1)/12 for date in data[:,0]])
# co2_values = data[:,1].astype(float)
#
# # Step 2a: Long-term trend using SciPy linear regression
# slope, intercept, r_value, p_value, std_err = stats.linregress(years, co2_values)
# trend_line = slope * years + intercept
#
# # Step 2b: Seasonal pattern using FFT
# co2_detrended = co2_values - trend_line
# fft_result = fft.fft(co2_detrended)
# frequencies = fft.fftfreq(len(years), d=1/12)  # monthly data → 1/12 year step
#
# # Keep only the strongest seasonal component (besides 0 frequency)
# fft_result_filtered = np.zeros_like(fft_result)
# season_freq = frequencies[np.argsort(np.abs(fft_result))[::-1][1]]  # 2nd strongest
# fft_result_filtered[np.where(frequencies == season_freq)] = fft_result[np.where(frequencies == season_freq)]
# fft_result_filtered[np.where(frequencies == -season_freq)] = fft_result[np.where(frequencies == -season_freq)]
# seasonal_pattern = fft.ifft(fft_result_filtered).real
#
# # Step 3a: Prediction for next 10 years
# future_years = np.linspace(years[-1], years[-1] + 10, num=120)  # monthly for 10 years
# future_trend = slope * future_years + intercept
# future_season = np.tile(seasonal_pattern[:12], int(len(future_years)/12) + 1)[:len(future_years)]
# future_prediction = future_trend + future_season
#
# # Step 3b: Plot everything
# plt.figure(figsize=(12,6))
# plt.scatter(years, co2_values, color="blue", s=8, label="Measured CO₂")
# plt.plot(years, trend_line, color="red", linewidth=2, label="Long-term trend")
# plt.plot(years, trend_line + seasonal_pattern, color="orange", alpha=0.7, label="Trend + Seasonality")
# plt.plot(future_years, future_prediction, color="green", linestyle="--", label="Forecast (10 yrs)")
# plt.fill_between(future_years, future_prediction-1, future_prediction+1, color="green", alpha=0.2, label="Prediction Range")
#
# plt.title("Atmospheric CO₂ at Mauna Loa Observatory with Seasonal Pattern & Forecast")
# plt.xlabel("Year")
# plt.ylabel("CO₂ concentration (ppm)")
# plt.legend()
# plt.grid(True)
# plt.show()
#
# # Step 4: Print insights
# print(f"Trend: CO₂ increases {slope:.2f} ppm/year")
# print(f"Strongest seasonal frequency: {abs(season_freq):.2f} cycles/year (~{12/abs(season_freq):.1f} months)")
# print(f"Correlation (R²): {r_value**2:.3f}")


