class ContactBook:
    def __init__(self):
        self.contacts: dict = {}
        
        
    def add_contacts(self, vip_id: str,name: str, phone: str, email: str, address: str):
        if vip_id not in self.contacts:
            self.contacts[vip_id]= {'vip_id': vip_id, 'name': name, 'phone': phone, 'email': email, 'address': address}
            print('contact add succesfully.')
            return
        else:
            print('Contac already EXISTS!!!')
            
    def show_contacts(self):
        if not self.contacts:
            print("No contacts to display.")
            return
    
        print(f"{'vip_id':<10} {'Name':<10} {'Phone':<15} {'Email':<25} {'Address':<30}")
        print("-" * 90)
    
        for c in self.contacts.values():
            print(f"{c['vip_id']:<10} {c['name']:<10} {c['phone']:<15} {c['email']:<25} {c['address']:<30}")
            
            
            
    def view_contacts(self):
        for vip_id, info in self.contacts.items():
            print(
                f'ID: {vip_id},\n '
                f'Name: {info["name"]}, '
                f'Phone: {info["phone"]}, '
                f'Email: {info["email"]},'
                f'Address: {info["address"]}')

        
            
    def update_contacts(self, vip_id: str, name: str = None, phone: str = None, email: str = None, address: str = None):
        if vip_id in self.contacts:
            if name:
                self.contacts[vip_id]['name']= name
            if phone:
                self.contacts[vip_id]['phone']= phone
            if email:
                self.contacts[vip_id]['email']= email
            if address:
                self.contacts[vip_id]['address']= address
            print('Contact updated was successfully...')
            return
        else:
            print('Sorry!!! Contact not found.')
            
            
            
    def delete_contacts(self, vip_id: str):
        if vip_id in self.contacts:
            del self.contacts[vip_id]
            print('Contact was deleted successfully...')
        else:
            print('Sorry!!! Contact not found.')
            
            
if __name__ == "__main__":
    book = ContactBook()

    while True:
        print("1. Add contact")
        print("2. View contacts")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Exit")
        user_input = input("Please select an option(1-5):")
            
        if user_input == "1":
            vip_id = input("Enter VIP ID:")
            name = input("Enter Name:")
            phone = input("Enter Phone:")
            email = input("Enter Email:")
            address = input("Enter Address:")
            book.add_contacts(vip_id, name, phone, email, address)
        elif user_input == "2":
            print("\n--- Contact List ---")
            book.show_contacts()
            book.view_contacts()
            
                
        elif user_input == "3":
            vip_id = input("Enter VIP ID of the contact to update:")
            name = input("Enter new Name (leave blank to keep current):")
            phone = input("Enter new Phone (leave blank to keep current):")
            email = input("Enter new Email (leave blank to keep current):")
            address = input("Enter new Address (leave blank to keep current):")
            book.update_contacts(vip_id, name if name else None, phone if phone else None, email if email else None, address if address else None)
        elif user_input == "4":
            vip_id = input("Enter VIP ID of the contact to delete:")
            book.delete_contacts(vip_id)
        elif user_input == "5":
            print("Have a nice day! Goodbye!")
            break
        else:
            print("\n Invalid option. Please try again.")