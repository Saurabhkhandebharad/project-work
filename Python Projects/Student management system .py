# Define menu options as a list for better organization
menu_options = [    "Add Student",    "Delete Student",    "Update Student",    "Show Student",    "Exit"]

# Define a dictionary to store student data
students = {
    "Roll_no": [],
    "Name": [],
    "Age": []
}

def admission_management_system():
    # Display the menu options
    display_menu()
    
    # Get user input for menu option
    try:
        user_input = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        admission_management_system()
        return
    
    # Handle user input based on selected option
    if user_input in range(1, 6):
        match user_input:
            case 1:
                add_student()    
            case 2:
                delete_student()
            case 3:
                update_student()
            case 4:
                show_student()
            case 5:
                exit_program()
    else:
        print("Invalid input. Please enter a number between 1 and 5.")
        admission_management_system()

def display_menu():
    print()
    print("=======================MENU=======================")
    for i, option in enumerate(menu_options):
        print(f"{i+1}. {option}")
    print()

def add_student():
    try:
        r = int(input("Enter Roll Number: ")) 
        n = input("Enter Name of Student: ")
        a = int(input("Enter Age of Student:"))
        students["Roll_no"].append(r)
        students["Name"].append(n)
        students["Age"].append(a)
    except ValueError:
        print("Invalid input. Please enter a valid value for Roll Number and Age.")
    admission_management_system()

def delete_student():
    try:
        r = int(input("Enter Roll Number: "))
        rm = students["Roll_no"].index(r)
        students["Roll_no"].pop(rm)
        students["Name"].pop(rm)
        students["Age"].pop(rm)
    except ValueError:
        print("Invalid input. Please enter a valid value for Roll Number.")
    admission_management_system()

def update_student():
    try:
        r = int(input("Enter Roll Number: ")) 
        n = input("Enter Name of Student: ")
        a = int(input("Enter Age of Student: "))
        up = students["Roll_no"].index(r)
        students["Name"][up] = n
        students["Age"][up] = a
    except ValueError:
        print("Invalid input. Please enter a valid value for Roll Number and Age.")
    admission_management_system()

def show_student():
    print("Roll_No"+ "\t" + "Name" + "\t" + "Age")
    for i, j, k in zip(students["Roll_no"], students["Name"], students["Age"]):
        print(i, "\t", j, "\t", k)
    admission_management_system()

def exit_program():
    pass

def run_ams():
    try:
        admission_management_system()
    except Exception as e:
        print()
        print("An error occurred. Please try again.")
        print(str(e))

run_ams()
