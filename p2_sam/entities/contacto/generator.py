from faker import Faker

faker = Faker('pt_PT')

emailList = []
contactList = []

def generateContact(n=100):
 while len(contactList) < n:
  numberDigits = faker.numerify("#######")
  contactNumber = f"97{numberDigits}"
  if contactNumber not in contactList:
   contactList.append(contactNumber)

generateContact()
print(contactList)
