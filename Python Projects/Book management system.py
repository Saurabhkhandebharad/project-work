import maskpass
password = "sk"
confirm = maskpass.advpass("Please enter your Librarian's password: ")

if confirm == password:
    print("WELCOME TO...")
    import mysql.connector as m
    # Connecting to MySQL server
    libdatabase = m.connect(host='localhost', user='root', password='saurabh')
    # Create database if it doesn't exist
    cursor = libdatabase.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")
    cursor.close()
    # Connect to "library" database
    libdatabase = m.connect(host='localhost', user='root', password='saurabh', database='library')
    # Create "collection" table if it doesn't exist
    cursor = libdatabase.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS collection(Lib_Index int primary key auto_increment, ISBN bigint(13), Title varchar(100), Author varchar(100), Publisher varchar(100), Book_status varchar(20) ,Reader_Name varchar(20), Issue_Date date , Due_Date date, Return_Date date, Dues int)")
    cursor.close()
    # Close database connections
    # libdatabase.close()


    from datetime import datetime, timedelta

    def add_book():
        # Prompt user for book information
        # Add book to library collection
        query = "INSERT INTO collection(ISBN, Title, Author, Publisher, Book_status) VALUES (%s, %s, %s, %s,%s)"
        while True:
            isbn_input = input("Enter book's ISBN NO (min 10, max 13 digits): ")
            if not isbn_input.isdigit():
                print("Invalid input for ISBN. Please enter a number.")
                continue
            isbn = int(isbn_input)
            if len(isbn_input) > 13:
                print("Invalid input for ISBN. ISBN should be at most 13 digits.")
                continue
            if len(isbn_input) < 10:
                print("Invalid input for ISBN. ISBN should be at least 10 digits.")
                continue
            if isbn <= 0:
                print("Invalid input for ISBN. ISBN should be a positive number.")
                continue

            while True:
                title = input("Enter book's title: ")
                if any(char.isdigit() for char in title):
                    doubt = input("Are you sure about the name?(y/n): ")
                    if (doubt == 'y'):
                        break
                    else:
                        ("Type the Title again: ")
                        continue
                else:
                    print("In case of wrong input for a book title, drop and add the book again in the system.")
                    break        
            while True:
                author = input("Enter Author's name: ")
                try:
                    if any(char.isdigit() for char in author):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input for Author. Please enter a name.")
                    continue
            while True:
                pub = input("Enter Publisher's name: ")
                try:
                    if any(char.isdigit() for char in pub):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input for Publisher. Please enter a name.")
                    continue
            cursor = libdatabase.cursor()
            try:
                cursor.execute(query, [isbn, title, author, pub,'Available'])
                libdatabase.commit()
            except Exception as e:
                print("Error inserting book:", e)
                libdatabase.rollback()
                continue
            print("Book added to library collection.")
            break
        end()


    def check_out_book():
        # Search for book by title or author
        search_by = input("Search by 1 - title, 2 - author, or 3 - ISBN?: ")
        if (search_by == '1'):
            query = "select * from collection where title like %s"
            search_term = input("enter book title: ").lower()
        elif (search_by == '2'):
            query = "select * from collection where author like %s"
            search_term = input("enter author name: ").lower()
        elif (search_by == '3'):
            query = "select * from collection where isbn = %s"
            search_term = input("enter ISBN number: ")
        else:
            print("Invalid Search Criteria.")
            return
            
        cursor = libdatabase.cursor()
        cursor.execute(query, [search_term])
        result=cursor.fetchall()       
        if len(result) == 0:
            print("No results found.")
            return
        else:
            print("*Sk's library*")
            for record in result:
                print(record)
                
        # Prompt user for book index number and borrower's name
        while True:
            try:
                book_index = int(input("Enter book's library index number: "))
                if book_index < 0:
                    raise ValueError("Index number must be a positive integer")
                break
            except ValueError:
                print("Invalid input: please enter a positive integer")
        while True:
            reader_name = input("Enter borrower's name: ")
            if not reader_name.isalpha():
                print("Invalid input: name must contain only letters")
            else:
                break
            
        # Check if user has already borrowed two books
        query = "SELECT COUNT(*) FROM collection WHERE book_status='Unavailable' AND reader_name=%s"
        cursor.execute(query, [reader_name])
        result = cursor.fetchone()
        if result[0] >= 2:
            print("You have already borrowed two books. Please return one before borrowing another.")
            return
        
        while True:
            issue_date_str = input("Enter a date in YYYY-MM-DD format: ")
            try:
                issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid input: please enter a date in YYYY-MM-DD format")
        due_date = issue_date + timedelta(days=7)
            
        # Update book status and due date
        query = "UPDATE collection SET book_status='Unavailable', reader_name=%s, issue_date=%s, due_date=%s WHERE lib_index=%s AND book_status='Available'"
        cursor = libdatabase.cursor()
        try:
            cursor.execute(query, (reader_name, issue_date, due_date, book_index))
            if cursor.rowcount == 0:
                print("The book cannot be borrowed")
            else:
                libdatabase.commit()
                print("Book checked out successfully!")
        except Exception as e:
            libdatabase.rollback()
            print("An error occurred: ", e)

        cursor.close()
        end()



    def check_in_book():
        # Prompt user for book index
        search_by = input("Enter '1': ")
        query = "select * from collection where title like %s"
        if (search_by == '1'):
            search_term = input("enter book title: ").lower()
        
        cursor = libdatabase.cursor()
        cursor.execute(query, [search_term])
        result=cursor.fetchall()       
        if len(result) == 0:
            print("No results found.")
            return
        else:
            print("*Sk's library*")
            for record in result:
                print(record)    
        
        while True:
            try:
                book_index = int(input("Enter book's index number: "))
                if book_index < 0:
                    raise ValueError("Index number must be a positive integer")
                break
            except ValueError:
                print("Invalid input: please enter a positive integer")

        # Prompt user for return date
        while True:
            return_date_str = input("Enter return date in YYYY-MM-DD format: ")
            try:
                return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid input: please enter a date in YYYY-MM-DD format")

        # Check if book is overdue
        cursor = libdatabase.cursor()
        query = "SELECT reader_name, issue_date, due_date FROM collection WHERE lib_index=%s AND book_status='Unavailable'"
        cursor.execute(query, (book_index,))
        row = cursor.fetchone()
        if not row:
            print("The book is not checked out")
        else:
            due_date = row[2]
            if due_date is None:
                print("The due date for this book is not set.")
            else:
                due_datetime = datetime.combine(due_date, datetime.min.time())
                days_overdue = (return_date - due_datetime).days
                if days_overdue > 0:
                    overdue_fine = days_overdue * 2
                    update_query = "UPDATE collection SET dues=%s, return_date=%s WHERE lib_index=%s"
                    cursor.execute(update_query, (overdue_fine, return_date, book_index))
                    libdatabase.commit()
                    print(f"The book is {days_overdue} day(s) overdue. Please pay a fine of {overdue_fine} Rs.")
                    pay_fine = int(input(": "))
                    if pay_fine == overdue_fine:
                        print("Fine has been successfully paid")
                    else:
                        print("Fine payment unsuccessful")
                        return

                else:
                    overdue_fine = 0
                    print("Thank you for returning the book on time.")

            # Update book status and fine amount
            query = "UPDATE collection SET book_status='Available', reader_name=NULL, issue_date=NULL, due_date=NULL, return_date = null, dues=null WHERE lib_index=%s"
            try:
                    cursor.execute(query, (book_index,))
                    if cursor.rowcount == 0:
                         print("The book status could not be updated")
                    else:
                        libdatabase.commit()
                        print("Book checked in successfully!")
            except Exception as e:
                    libdatabase.rollback()
                    print("An error occurred: ", e)
            

    # End transaction
            cursor.close()
            end()
                   

    def drop_book():
        cursor = libdatabase.cursor()
        try:
            lost = input("Enter ISBN of book to remove from library: ")
            # convert the ISBN to an integer
            lost = int(lost)
        except ValueError:
            print("Invalid ISBN. Please enter a valid integer.")
            return
        query = "DELETE FROM collection WHERE isbn = %s"
        try:
            cursor.execute(query, (lost,))
            if cursor.rowcount > 0:
                libdatabase.commit()
                print("Book removed successfully!")
            else:
                print("Book not found in the library.")
        except Exception as e:
            libdatabase.rollback()
            print("An error occurred: ", e)
        end()

    def end():
        bye = input('do you wish to continue?(y/n): ')
        if bye == 'y':
            library()
        else:
            print("*Sk's Library*")
            exit()

    def tata():
        tata = input("do you wish to get out of system?(y/n): ")
        if tata == 'y':
            exit()
        else:
            end()
        
    def library():
        while True:
            print("*** SK's Library ***")
            try:
                ans = input("\n1 - Add new book \n2 - Check out book\n3 - Check in book\n4 - drop book\n5 - exit : ")
                if(ans=="1"):
                    add_book()
                elif(ans=='2'):
                    check_out_book()
                elif(ans=='3'):
                    check_in_book()
                elif(ans=='4'):
                    drop_book()
                elif(ans=='5'):
                    tata()
                else:
                    print("inalid input. Please enter a number between 1 to 5.")
            except Exception as e:
                print(f"An error occurred: {e}")
                    
    library()    
    
else:
    print("Access denied")

