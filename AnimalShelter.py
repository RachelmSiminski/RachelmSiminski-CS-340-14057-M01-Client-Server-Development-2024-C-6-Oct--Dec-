""" AnimalShelter.py is a CRUD program intended to assist in the process of
    creating, reading, updating, and deleting animal records for the Austin
    Animal Clinic. The team at AAC works to recruit animals to help in Search
    and Rescue efforts. The program is linked to a MongoDB database, wherein
    the AAC has already bulk uploaded around 10000 animal records. The MongoDB
    connections are hard-coded at this time, since the program is intended
    for the AAC specifically, but these connection variables can be changed
    for those who may desire to utilize this free software for their own
    work!

    Developer: Rachel Siminski"""


from pymongo import MongoClient
import bson.json_util as json_util
import re

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password, host, port):
        # Initializing the MongoClient. This helps to access the MongoDB databases and
        # collections. This is hard-wired to use the aac database, the animals
        # collections, and the aac user. Definitions of the connection string variables
        # are unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect your own instance
        # of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
            # Test connection
            self.client.admin.command('ping')
            print("MongoDB connection successful!")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")

        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Complete this create method to implement the C inf CRUD.
    def create(self, data):
        try:
            if data is not None:
                print(f"Inserting data: {data}")  # Debug: print what data is being inserted
                result = self.database.animals.insert_one(data)
                if result.inserted_id:
                    return True
            else:
                print("Nothing to save, because data parameter is empty")
                return False
        except Exception as e:
            print(f"Error occurred during data insertion: {e}")

    # Create method to implement the R in CRUD.
    def read(self, data):
        try:
            if data is not None:
                results = self.collection.find(data)
                results_list = [doc for doc in results]
                if results_list:
                    return results_list
                else:
                    print("No matching records found for query")
                    return []
            else:
                return []
        except Exception as e:
            print("No available data: {e}")
            return []

    # Method to implement the U in CRUD
    def update(self, query, update_values):
        try:
            if query and update_values:
                result = self.database.animals.update_many(query, {'$set': update_values})
                print(f"Matched {result.matched_count} document, Modified {result.modified_count} documents.")
                return True
            else:
                print("Unable to update record(s).")
                return False
        except Exception as e:
            print(f"Error occurred during update: {e}")
            return False

    # Method to implement the D in CRUD
    def delete(self, query):
        try:
            if query:
                result = self.database.animals.delete_many(query)
                print(f"Deleted {result.deleted_count} documents.")
                return True
            else:
                print("Unable to delete record(s).")
                return False
        except Exception as e:
            print(f"Error occurred during deletion: {e}")
            return False

# Implement user input to demonstrate the programs abilities
#Instantiate the class object
shelter = AnimalShelter('aacuser','SNHU1234', 'localhost', '27017')

# Present the user with options
while True:
    print("Main Menu\n")
    print("1: Create animal.\n")
    print("2: Read animal records.\n")
    print("3: Update animal.\n")
    print("4: Delete animal.\n")
    print("Q: Exit program\n")

    choice = input("Enter selection: ").strip().lower()

    # Implement create functionality using user input
    if choice == "1":
        # Collect animal data
        rec_num = input("Record number: ")
        age_upon_outcome = input("Age Upon Outcome: ")
        animal_id = input("Animal ID: ")
        animal_type = input("Animal Type: ")
        breed = input("Breed: ")
        color = input("Color: ")
        date_of_birth = input("Date of Birth: ")
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM:SS): ")
        datetime = date + " " + time
        monthyear = date + "T" + time
        name = input("Name: ")
        outcome_subtype = input("Outcome Subtype: ")
        outcome_type = input("Outcome Type: ")
        sex_upon_outcome = input("Sex Upon Outcome: ")
        location_lat = input("Location Latitude: ")
        location_long = input("Location Longitude: ")
        age_upon_outcome_in_weeks = input("Age Upon Outcome in Weeks: ")

        # Insert data
        data = {"rec_num": rec_num, "age_upon_outcome": age_upon_outcome, "animal_id": animal_id, "animal_type": animal_type, "breed": breed, "color": color, "date_of_birth": date_of_birth, "datetime": datetime, "monthyear": monthyear, "name": name, "outcome_subtype": outcome_subtype, "outcome_type": outcome_type, "sex_upon_outcome": sex_upon_outcome, "location_lat": location_lat, "location_long": location_long, "age_upon_outcome_in_weeks": age_upon_outcome_in_weeks}
        try:
            # Check that data inserted properly
            if shelter.create(data):
                print("Animal data insert successful!")
            else:
                print("Unable to add animal data.")
        except Exception as e:
            print("Unable to insert animal data: ",e)

    # Implement the read functionality using user input
    elif choice == "2":
        # Search animal records (query)
        query = input("Enter search request ({'key':'value'}): ")
        query = query.strip()

        # Try to search the database for given key value pair
        try:
            # Ensure the user input uses double quotes for JSON format
            query = query.replace("'", "\"")  # Replace single quotes with double quotes
            # Parse the input string into a Python dictionary
            query_dict = json_util.loads(query)
            results = shelter.read(query_dict)

            # Check that the query has worked properly
            if results:
                print("Matching records: ")
                for record in results:
                    print(record)

            else:
                print("No matching records found.")

        except Exception as e:
            print("Unable to retrieve data:", e)

    # Implement update functionality using user input
    elif choice == "3":
        # Search animal records (query)
        query = input("Enter search request ({key:value}): ")

        # Try to search the database for given key value pair
        try:
            # Parse the input string into a Python dictionary
            query_dict = json_util.loads(query)
            results = shelter.read(query_dict)

            # Check that the query has worked properly
            if results:
                print("Matching records: ")
                for record in results:
                    print(record)

                # Prompt user for new values
                update_query = input("Enter update values ({key:value}): ")
                # Parse the updated values
                update_dict = json_util.loads(update_query)

                # Attempt to update the record(s)
                if shelter.update(query_dict, update_dict):
                    print("Records updated successfully!")
                else:
                    print("Update failed.")

            else:
                print("No matching records found.")

        except Exception as e:
            print("Unable to retrieve data:", e)

    # Implement delete functionality using user input
    elif choice == "4":
        # Search animal records (query)
        query = input("Enter search request ({key:value}): ")

        try:
            # Parse the input string into a Python dictionary
            query_dict = json_util.loads(query)
            results = shelter.read(query_dict)

            if results: # Display records matching the query
                print("Matching records:")
                for record in results:
                    print(record)

                # Confirm intent
                confirm = input("Are you sure you want to delete these records? (yes/no): ").strip().lower()
                if confirm == "yes":
                    if shelter.delete(query_dict):
                        print("Records deleted successfully!")
                    else:
                        print("Failed to delete records.")
                else:
                    print("Delete operation canceled.")
            else:
                print("No matching records found.")

        except Exception as e:
            print("Unable to retrieve or delete data:", e)

    # Implement choice to terminate program
    elif choice == "q":
        print("Exiting the program.")
        break

    else:
        print("Please enter a valid input. Choose an option 1, 2, 3, 4, or enter 'Q' to terminate the program.")