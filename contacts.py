# Create a CLI menu for the user to add a contact, edit a contact, delete a contact, or display all contacts.
import re
import os
import json

#Global data variable to be appended later by functions
data = []

def display_menu():
    #Display the menu for the Contact Book.
    print("Welcome to The Contact Book! Please select an option:")
    print("1. Add a contact")
    print("2. Edit a contact")
    print("3. Delete a contact")
    print("4. Display all contacts")
    print("5. Exit Program")

def add_contact():
    #Add a new contact with error checking for name, phone, and email inputs.
    global data
    print("Add a contact selected\n")
    
    #Get name input
    while True:
        name = input("Please enter the new contact's name (first last):\n")
        if not re.match(r"^[a-zA-Z]+\s[a-zA-Z]+$", name):
            print("Invalid name. Please enter both first and last names (letters only).")
        else:
            break
    
    #Get phone input
    while True:
        phone = input("Please enter the new contact's phone number (10 digits):\n")
        if not phone.isdigit() or len(phone) != 10:
            print("Invalid phone number. Please enter 10 digits only.")
        else:
            break
    
    #Get email input
    while True:
        email = input("Please enter the contact's email address:\n")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email address. Please enter a valid email address.")
        else:
            break
    #Determine if the JSON file exists and is readable
    if os.path.isfile('contact_book.json'):
        with open('contact_book.json', 'r') as f:
            try:
                json_data = json.load(f)
                if 'contacts' not in json_data:
                    print('JSON detected is missing the contacts key')
                    exit()
                data = json_data['contacts']
            except json.JSONDecodeError:
                print('Error reading JSON file')
                exit()
    else:
        #Create a new list with an empty dictionary
        data = []
    
    #Update the data variable with collected contact info
    first_name, last_name = name.split()
    data.append({'name': f'{first_name} {last_name}', 'phone': phone, 'email': email})

    #Write the data to the contact_book.json file
    with open('contact_book.json', 'w') as f:
        json.dump({'contacts': data}, f, indent=2)
    
    input("Contact added! Press enter to return to menu...")

def edit_contact():
    print("Edit a contact selected\n")
    # Prompt user to enter contact name.
    while True:
        name = input("Please enter the contact's name (first last):\n")
        if not re.match(r"^[a-zA-Z]+\s[a-zA-Z]+$", name):
            print("Invalid name. Please enter both first and last names (letters only).")
            continue

        # Search for the contact in the JSON
        if not os.path.isfile('contact_book.json'):
            print("No contacts found. Please add a contact first.")
            break
        
        with open('contact_book.json', 'r') as f:
            try:
                json_data = json.load(f)
                if 'contacts' not in json_data:
                    print('JSON detected is missing the contacts key')
                    exit()

                data = json_data['contacts']
                found_contact = None
                for contact in data:
                    if contact['name'] == name:
                        found_contact = contact
                        break

                if found_contact is None:
                    print("Contact not found! Please try again!")
                    continue

                # Ask user what data to edit
                print("Contact found! Editing Options:")
                print("1. Name")
                print("2. Phone Number")
                print("3. Email")
                edit_selection = input('Enter your selection (1-3): ')

                # Prompt the user for the updated contact info
                if edit_selection == '1':
                    while True:
                        new_name = input("Please enter the contact's updated name (first last):\n")
                        if not re.match(r"^[a-zA-Z]+\s[a-zA-Z]+$", new_name):
                            print("Invalid name. Please enter both first and last names (letters only).")
                            continue
                        else:
                            found_contact['name'] = new_name
                            break

                elif edit_selection == '2':
                    while True:
                        phone = input("Please enter the contact's updated phone number (10 digits):\n")
                        if not phone.isdigit() or len(phone) != 10:
                            print("Invalid phone number. Please enter 10 digits only.")
                            continue
                        else:
                            found_contact['phone'] = phone
                            break

                elif edit_selection == '3':
                    while True:
                        email = input("Please enter the contact's updated email address:\n")
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            print("Invalid email address. Please enter a valid email address.")
                            continue
                        else:
                            found_contact['email'] = email
                            break

                else:
                    print('Invalid selection. Please enter a number between 1 and 3.')
                    continue

                # Write the updated data to the JSON file
                with open('contact_book.json', 'w') as f:
                    json.dump(json_data, f, indent=2)

                input('Contact updated successfully! Press enter to return to menu...')
                break

            except json.JSONDecodeError:
                print('Error reading JSON file')
                exit()

def delete_contact():
    print("Delete a contact selected")

    with open('contact_book.JSON', 'r') as f:
        contacts = json.load(f)

    # Get name input
    while True:
        name = input("Please enter the contact's name (first last):\n")
        if not re.match(r"^[a-zA-Z]+\s[a-zA-Z]+$", name):
            print("Invalid name. Please enter both first and last names (letters only).")
        else:
            break
    
    found_contact = False
    
    # Get user confirmation before deletion
    for contact in contacts['contacts']:
        if contact['name'] == name:
            found_contact = True
            confirm = input(f"Are you sure you want to delete {name}? (y/n) ")
            if confirm.lower() == 'y':
                contacts['contacts'].remove(contact)
                with open('contact_book.JSON', 'w') as f:
                    json.dump(contacts, f, indent=2)
                print(f"{name} deleted successfully!")
            else:
                print(f"{name} was not deleted.")
            break
    # Loop user back if contact not found
    if not found_contact:
        print("Contact not found. Please try again!")
        delete_contact()

def display_contacts():
    print("Display all contacts selected.")

    with open('contact_book.JSON', 'r') as f:
        contacts = json.load(f)
    
    print(json.dumps(contacts, indent=2))

    input("Press enter to return to the main menu...")

# Main Menu
while True:
    display_menu()
    menu_selection = input("Enter your selection (1-5): ")

    if menu_selection == "1":
        add_contact()
    elif menu_selection == "2":
        edit_contact()
    elif menu_selection == "3":
        delete_contact()
    elif menu_selection == "4":
        display_contacts()
    elif menu_selection == "5":
        print("Exiting...")
        break
    else:
        print("Invalid selection. Please enter a number from 1-5")