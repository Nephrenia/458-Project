# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 21:55:39 2021

@author: Bin Map & Vincent Bui
"""
import numpy as np
import random

# Constant variables no touch please

MAXIMUM_WAITING_TIME = 120 # minutes
MAXIMUM_EATING_TIME = 120 # minutes
MAXIMUM_CAPACITY = 300 # maximum customer can be in restaurant
RESTAURANT_WIDTH = 15 
RESTAURANT_LENGTH = 15
#BEGINNING_HOURS = 10 # 10 o'clock am
#ENDING_HOURS = 22 # 10 o'clock 
BEGINNING_HOURS_IN_MINUTES = 0 #time in minutes
ENDING_HOURS_IN_MINUTES= 600 #time in minutes
TABLES = 9 # init tables


# list of variable
menu = ["Hamburger","Pizza","Steak"] # Food menu
prep_time = [12,10,15] # the amount of time it take to make each meal 
food_cost = [15,12,20] # the cost of each food
total_number_of_customers = 0
lost_customers = 0
list_of_tables = [] # list to keep track of table
list_of_customers = [] # list to keep track of group
list_of_people_in_line = []
priority_list=[]
preoccupied_table=[]
operating_hours = BEGINNING_HOURS_IN_MINUTES

# Other variables
waiting_time_spawn_customer = 0 # wait time to spawn each customer
chairs = 4 # init chairs
group = 10 # init customer group
revenue = 0 # init revenue
average_time = 0 # init average time
served_customer = 0 # init served customer
unserved_customer = 0 # init not served customer
time_step = 1
beginning_number_of_customers = 12
probability_of_large_group = 0.20
grid = []
payment = []
#------------------------------------------------------------------------------
class Customer(object):

    def __init__(self, food_order, number_of_people, eating_time):
        self.state = "Away"        
        self.food_order = food_order
        self.number_of_people = number_of_people
        self.waiting_time = 0
        self.time_in_restaurant = 0
        self.eating_time = eating_time
        self.tableNumber = []
        

    def state(self, status):
        if status == 0:
            self.state = "Waiting"
        if status == 1:
            self. state = "Served"
        if status == 2:
            self.state = "Left"
        if status == 3:
            self.state = "Order"
    def location(self):
        return self.tableNumber
    
    def toString(self):
        return self.food_order, self.number_of_people, self.waiting_time, self.eating_time
    
#------------------------------------------------------------------------------
class Restaurant(object):
    
    def __init__(self):
        self.restaurant_width = RESTAURANT_WIDTH
        self.restaurant_length = RESTAURANT_LENGTH
        self.tables = list_of_tables
        self.state ="Empty"

    def state(self, status):
        if status == 0:
            self.state = "Occupied"
        if status == 1:
            self.state = "Empty"
        if status == 2:
            self.state = "Preoccupied"
    
    def availableTables(self):
        
        count = 0
        
        for i in list_of_tables:
            for j in i:
                if j.availability():
                    count += 1
        
        return count
    
    def toString(self):
        return self.tables, self.chairs, self.state

class Table(object):
    
    def __init__(self, tableNumber):
        self.chairs = chairs
        self.state = "Empty"
        self.tableNumber = tableNumber
    
    def availability(self):
        if self.state == "Empty":
            return True
        else:
            return False
    
    def state(self):
        return self.state

def simulationDriver(phase):
    
    initialization()
    operations()
            
def initialization():
    
    # create the number of customers
    
    for i in range(beginning_number_of_customers):
        customer = createCustomer()
        list_of_people_in_line.append(customer)
    
    # for i in range(len(list_of_customers)):
    #     print(list_of_customers[i].toString())
    
    global list_of_tables

    for i in range(1, TABLES + 1):
        table = Table(i)
        list_of_tables.append(table)
    
    tab = np.array(list_of_tables)
    
    tab = np.reshape(tab, (3,3))
    
    list_of_tables = tab
    # for i in list_of_tables:
    #     print(i.state)
    #     print(i.tableNumber)
    
    
def createCustomer():
    
    food_order = menu[random.randint(0, 2)]
        
    rand = random.random()
    
    if probability_of_large_group > rand:
        number_of_people = random.randint(4, 6)
    else:
        number_of_people = random.randint(1, 4)
        
    if number_of_people >= 4:
        eating_time = random.randint(30, 60)
    else:
        eating_time = random.randint(15, 60)
            
    return Customer(food_order, number_of_people, eating_time)
 
def find_extra_table(customer):
    #look at each row of tables
    for row in range(len(list_of_tables)):
        #look at each table
        for table in range(len(list_of_tables[row])):
            #check if there is an extra table
            check = list_of_tables[row][table]
            
            #if the there is an extra table available
            if check.availability() == True:
                
                #set table to occupied
                list_of_tables[row][table].state= "Occupied"
                customer.state = "Order"
                customer.waiting_time += time_step
                list_of_customers.append(customer)
                #remove customer from the waitlist
                list_of_people_in_line.remove(customer)
                
                #add another table next to the assigned table
                customer.tableNumber.append(list_of_tables[row][table].tableNumber)
                return True           
    #return false because there are no available table    
    return False


#check customer eating time
def eating_food():
    global served_customer
    for people in list_of_customers:
        #if group is current being served
        if people.state == "Served":
            #increment eating time by one every minutes
            people.time_in_restaurant+=time_step
            #print(people.time_in_restaurant,people.eating_time)
            #if the time spend in restaurant is equal to approximate eating time
            #set customer to done eating
            if people.time_in_restaurant == people.eating_time:
                #print(people.time_in_restaurant)
                people.state = "Left"
                served_customer+=1
                for row in range(len(list_of_tables)):
                    for table in range(len(list_of_tables[row])):
                        for customer_table in people.tableNumber:
                            check_table= list_of_tables[row][table].tableNumber
                            if customer_table==check_table:
                                list_of_tables[row][table].state = "Empty"
        
def order_food():
    for people in list_of_customers:
        if people.state == "Order":           
            if people.food_order == "Steak":
                payment.append(food_cost[2]*people.number_of_people)
                people.eating_time += prep_time[2]
                people.state = "Served"
            if people.food_order == "Pizza":
                payment.append((food_cost[1]*people.number_of_people))
                people.eating_time += prep_time[1]
                people.state = "Served"
            if people.food_order == "Hamburger":
                payment.append((food_cost[0]*people.number_of_people))
                people.eating_time += prep_time[0]    
                people.state = "Served"

def operations():
    
    restaurant = Restaurant()
    global list_of_people_in_line
    global lost_customers
    global operating_hours
    global total_number_of_customers
    
    while (operating_hours != ENDING_HOURS_IN_MINUTES):
        
        if restaurant.availableTables() > 0:
        
            for i in range(len(list_of_tables)):
                for j in range(len(list_of_tables[i])):
                    temp = list_of_tables[i][j]
                    
                    if temp.availability() == True:
                        #check the priority list
                        #if it is not empty get the next customer
                        if priority_list:
                            customer = priority_list[0]
                            print("next group of",customer.number_of_people,"from the priority list")      
                            #add the next available table next to the assigned table
                            customer.tableNumber.append(list_of_tables[i][j].tableNumber)
                            customer.waiting_time += time_step
                            customer.state = "Order"
                            
                            list_of_customers.append(customer)
                            list_of_tables[i][j].state= "Occupied"                                                     
                            priority_list.remove(customer)
                            
                            
                        #if the priority list is empty                       
                        else:  
                            #get the next customer in line
                            if list_of_people_in_line:
                                customer = list_of_people_in_line[0]
                        
                                #if the number of customer is less than the number of chair in a table
                                if customer.number_of_people <= list_of_tables[i][j].chairs:
                                
                                    customer.tableNumber.append(list_of_tables[i][j].tableNumber)
                                    list_of_tables[i][j].state = "Occupied"
                                    customer.waiting_time += time_step
                                    customer.state = "Order"
                                    list_of_customers.append(customer)
                                    list_of_people_in_line.remove(customer)   
                                    print("next group of",customer.number_of_people,"table",customer.tableNumber)                                                               
                                    #if the number of customer is greater than the number of chair in a table
                                else:                                        
                                    customer.tableNumber.append(list_of_tables[i][j].tableNumber)
                                    list_of_tables[i][j].state = "Occupied"  
                                    is_table_available=find_extra_table(customer)
                                    print("big group of",customer.number_of_people,"tables", customer.tableNumber)
                                    if not is_table_available:
                                        print("move customer to priority list and reserve a table")
                                        priority_list.append(customer)  
                                                                                                       
        order_food()
        eating_food()                                                   
        
        list_of_people_in_line.append(createCustomer())
        
        #for i in list_of_people_in_line:
        total_number_of_customers = total_number_of_customers + list_of_people_in_line[-1].number_of_people
        
        if total_number_of_customers > MAXIMUM_CAPACITY:
            total_number_of_customers = total_number_of_customers - list_of_people_in_line[-1].number_of_people
            list_of_customers.append(list_of_people_in_line[-1])
            list_of_people_in_line.remove(list_of_people_in_line[-1])
            lost_customers = lost_customers + 1
        
        operating_hours = operating_hours + time_step

        #print(total_number_of_customers)
        
        for i in list_of_people_in_line: 
            i.waiting_time = i.waiting_time + time_step
            if i.waiting_time > MAXIMUM_WAITING_TIME:
                list_of_customers.append(i)
                list_of_people_in_line.remove(i)
                lost_customers = lost_customers + 1
        #increase the time by one minute
        operating_hours+=1
        
    #print(lost_customers)
    
    #print(len(list_of_customers))
    
    #print(len(list_of_people_in_line))
    
    print(served_customer)
simulationDriver(0)