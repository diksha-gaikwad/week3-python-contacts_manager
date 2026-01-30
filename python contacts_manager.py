# CONTACT MANAGEMENT SYSTEM
# MCA Mini Project – Functions & Dictionaries

import json
import re
import csv
from datetime import datetime
import os

FILE_NAME = "contacts.json"

# ---------------- VALIDATION ---------------- #

def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def clean_name(name):
    return name.strip().title()

# ---------------- FILE OPERATIONS ---------------- #

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

# ---------------- CRUD FUNCTIONS ---------------- #

def add_contact(contacts):
    print("\n--- ADD CONTACT ---")
    name = clean_name(input("Enter name: "))

    if not name:
        print("❌ Name cannot be empty")
        return

    if name in contacts:
        print("⚠ Contact already exists")
        return

    phone = input("Enter phone: ")
    valid, phone = validate_phone(phone)
    if not valid:
        print("❌ Invalid phone number")
        return

    email = input("Enter email (optional): ")
    if email and not validate_email(email):
        print("❌ Invalid email")
        return

    group = input("Group (Friends/Work/Family): ") or "Other"

    contacts[name] = {
        "phone": phone,
        "email": email or None,
        "group": group,
        "created_at": datetime.now().isoformat()
    }

    save_contacts(contacts)
    print("✅ Contact added successfully")

def search_contact(contacts):
    term = input("Enter name to search: ").lower()
    results = {k: v for k, v in contacts.items() if term in k.lower()}

    if not results:
        print("❌ No contact found")
        return

    for name, info in results.items():
        print_contact(name, info)

def update_contact(contacts):
    name = clean_name(input("Enter name to update: "))

    if name not in contacts:
        print("❌ Contact not found")
        return

    phone = input("New phone (leave blank to keep): ")
    if phone:
        valid, phone = validate_phone(phone)
        if not valid:
            print("❌ Invalid phone")
            return
        contacts[name]["phone"] = phone

    email = input("New email (leave blank to keep): ")
    if email:
        if not validate_email(email):
            print("❌ Invalid email")
            return
        contacts[name]["email"] = email

    group = input("New group (leave blank to keep): ")
    if group:
        contacts[name]["group"] = group

    contacts[name]["updated_at"] = datetime.now().isoformat()
    save_contacts(contacts)
    print("✅ Contact updated")

def delete_contact(contacts):
    name = clean_name(input("Enter name to delete: "))

    if name not in contacts:
        print("❌ Contact not found")
        return

    confirm = input("Are you sure? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        save_contacts(contacts)
        print("🗑 Contact deleted")

def display_all(contacts):
    if not contacts:
        print("No contacts available")
        return

    for name, info in contacts.items():
        print_contact(name, info)

# ---------------- EXTRA FEATURES ---------------- #

def print_contact(name, info):
    print("\n----------------------------")
    print(f"👤 Name : {name}")
    print(f"📞 Phone: {info['phone']}")
    if info["email"]:
        print(f"📧 Email: {info['email']}")
    print(f"👥 Group: {info['group']}")

def export_to_csv(contacts):
    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Group"])
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["group"]])
    print("📤 Exported to contacts.csv")

def statistics(contacts):
    print(f"\n📊 Total Contacts: {len(contacts)}")
    groups = {}
    for c in contacts.values():
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    for g, count in groups.items():
        print(f"{g}: {count}")

# ---------------- MENU ---------------- #

def menu():
    print("""
===============================
 CONTACT MANAGEMENT SYSTEM
===============================
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. Display All Contacts
6. Export to CSV
7. Statistics
8. Exit
""")

def main():
    contacts = load_contacts()

    while True:
        menu()
        choice = input("Choose option (1-8): ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            display_all(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            statistics(contacts)
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
