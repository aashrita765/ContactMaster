import tkinter as tk
from tkinter import simpledialog, messagebox

# AVL Tree Node class
class AVLTreeNode:
    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None
        self.height = 1

# Contact class to store contact details
class Contact:
    def __init__(self, contact_id, name, phone_number):
        self.contact_id = contact_id
        self.name = name
        self.phone_number = phone_number

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

# AVL Tree class for managing contacts
class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, contact):
        if not root:
            return AVLTreeNode(contact)
        elif contact < root.contact:
            root.left = self.insert(root.left, contact)
        else:
            root.right = self.insert(root.right, contact)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and contact < root.left.contact:
            return self.right_rotate(root)
        if balance < -1 and contact > root.right.contact:
            return self.left_rotate(root)
        if balance > 1 and contact > root.left.contact:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and contact < root.right.contact:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, contact):
        if not root:
            return root
        elif contact < root.contact:
            root.left = self.delete(root.left, contact)
        elif contact > root.contact:
            root.right = self.delete(root.right, contact)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.contact = temp.contact
            root.right = self.delete(root.right, temp.contact)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def search(self, root, name):
        if root is None or root.contact.name == name:
            return root
        if root.contact.name < name:
            return self.search(root.right, name)
        return self.search(root.left, name)

    def in_order_traversal(self, root):
        contacts = []
        if root:
            contacts.extend(self.in_order_traversal(root.left))
            contacts.append(root.contact)
            contacts.extend(self.in_order_traversal(root.right))
        return contacts

# Global variables
avl_tree = AVLTree()
root_node = None
contact_id_counter = 0

# Function to add a new contact to the phone book
def add_contact_helper(name, phone_number):
    global contact_id_counter, root_node
    if not isinstance(name, str):
        print("Error: Name must be a string.")
        return False
    if not isinstance(phone_number, str) or not phone_number.isdigit() or not len(phone_number)==10:
        print("Error: Phone number must be a valid integer string.")
        return False
    contact_id_counter += 1
    contact = Contact(contact_id_counter, name, phone_number)
    root_node = avl_tree.insert(root_node, contact)
    print(f"Added {name} with phone number {phone_number} to the phone book.")
    return True

# Function to display all contacts in the phone book
def display_contacts_helper():
    contacts = avl_tree.in_order_traversal(root_node)
    if contacts:
        print("PhoneBook Contacts:")
        for contact in contacts:
            print(f"ID: {contact.contact_id}, Name: {contact.name}, Phone Number: {contact.phone_number}")
    else:
        print("No contacts found in the phone book.")
    return contacts

# Function to search for a contact by name
def search_contact_helper(name):
    result = avl_tree.search(root_node, name)
    if result:
        print(f"Search Result for '{name}':")
        print(f"ID: {result.contact.contact_id}, Name: {result.contact.name}, Phone Number: {result.contact.phone_number}")
        return [result.contact]
    else:
        print(f"No contacts found with name '{name}'.")
        return []

# Function to update an existing contact's phone number
def update_contact_helper(name, new_phone_number):
    global root_node
    if not isinstance(name, str):
        print("Error: Name must be a string.")
        return False
    if not isinstance(new_phone_number, str) or not new_phone_number.isdigit() or not len(new_phone_number)==10:
        print("Error: New phone number must be a valid integer string.")
        return False
    contact_node = avl_tree.search(root_node, name)
    if contact_node:
        contact = contact_node.contact
        contact.phone_number = new_phone_number
        root_node = avl_tree.delete(root_node, contact)
        root_node = avl_tree.insert(root_node, contact)
        print(f"Phone number updated for contact with name {name}.")
        return True
    else:
        print(f"No contact found with name {name}.")
        return False

# Function to delete a contact by name
def delete_contact_helper(name):
    global root_node
    if not isinstance(name, str):
        print("Error: Name must be a string.")
        return False
    contact_node = avl_tree.search(root_node, name)
    if contact_node:
        root_node = avl_tree.delete(root_node, contact_node.contact)
        print(f"Contact with name {name} deleted.")
        return True
    else:
        print(f"No contact found with name {name}.")
        return False

def operations():

    def add_contact():
        name = simpledialog.askstring("Input", "Enter name:")
        phone_number = simpledialog.askstring("Input", "Enter phone number:")
        if name and phone_number:
            phone_number_str = str(phone_number)
            if add_contact_helper(name, phone_number):
                messagebox.showinfo("Success", f"Added {name} with phone number {phone_number} to the phone book.")
            else:
                messagebox.showinfo("Error","Incorrect name or phone number!")

    def display_contacts():
        contacts = display_contacts_helper()
        if contacts:
            contact_list.delete(0, tk.END)
            for contact in contacts:
                contact_list.insert(tk.END, f"ID: {contact.contact_id}, Name: {contact.name}, Phone Number: {contact.phone_number}")
        else:
            messagebox.showinfo("Info", "No contacts found in the phone book.")

    def search_contact():
        name = simpledialog.askstring("Input", "Enter name to search:")
        if name:
            contacts = search_contact_helper(name)
            if contacts:
                contact_list.delete(0, tk.END)
                for contact in contacts:
                    contact_list.insert(tk.END, f"ID: {contact.contact_id}, Name: {contact.name}, Phone Number: {contact.phone_number}")
            else:
                messagebox.showinfo("Info", f"No contacts found with name '{name}'.")

    def update_contact():
        name = simpledialog.askstring("Input", "Enter name to update:")
        new_phone_number = simpledialog.askstring("Input", "Enter new phone number:")
        if name and new_phone_number:
            new_phone_number_str = str(new_phone_number)
            success = update_contact_helper(name, new_phone_number)
            if success:
                messagebox.showinfo("Success", f"Phone number updated for contact with name {name}.")
            else:
                messagebox.showinfo("Error", f"No contact found with name {name} or invalid information given.")

    def delete_contact():
        name = simpledialog.askstring("Input", "Enter name to delete:")
        if name:
            success = delete_contact_helper(name)
            if success:
                messagebox.showinfo("Success", f"Contact with name {name} deleted.")
            else:
                messagebox.showinfo("Error", f"No contact found with name {name}.")

    root = tk.Tk()
    root.title("Enhanced PhoneBook Application")

    tk.Button(root, text="Add New Contact", command=add_contact).pack(fill=tk.X)
    tk.Button(root, text="Display All Contacts", command=display_contacts).pack(fill=tk.X)
    tk.Button(root, text="Search Contact by Name", command=search_contact).pack(fill=tk.X)
    tk.Button(root, text="Update Contact Phone Number", command=update_contact).pack(fill=tk.X)
    tk.Button(root, text="Delete Contact", command=delete_contact).pack(fill=tk.X)

    contact_list = tk.Listbox(root)
    contact_list.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    operations()