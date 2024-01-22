from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]

    password_list += [choice(symbols) for _ in range(randint(2, 4))]

    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    passw = "".join(password_list)

    password_entry.insert(0, passw)
    pyperclip.copy(passw)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Fields cannot be empty")
    else:
        try:
            with open('password_file.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('password_file.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open('password_file.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website_to_search = website_entry.get()

    try:
        with open('password_file.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No file found", message="There is no file that was found that holds your "
                                                           "passwords. Create it first.")
    else:
        searched_website = {website: info for (website, info) in data.items() if website == website_to_search}

        try:
            website_data = searched_website[website_to_search]
        except KeyError:
            messagebox.showinfo(title="No website found",
                                message="There was no website that was found with the saved "
                                        "information.")
        else:
            email = website_data['email']
            password = website_data['password']
            messagebox.showinfo(f"{website_to_search}", message=f"Email: {email}\nPassword: {password}")


# ----------------------------------------------- UI Layout ---------------------------------
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

# ----------------------------------------------- Labels ---------------------------------
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# ----------------------------------------------- Entries ---------------------------------
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "Ioterzian@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)


# ----------------------------------------------- Buttons ---------------------------------
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=3)
window.mainloop()
