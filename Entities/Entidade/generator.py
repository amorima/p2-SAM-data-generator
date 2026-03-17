from faker import Faker

faker = Faker('pt_PT')
ibanList = []
nameList = []

def generateIban(n=100):
 while len(ibanList) < n:
  digits = faker.numerify(text='#############')
  iban = f"PT500067{digits}"
  ibanList.append(iban)

def generateName(n=100):
 while len(nameList) < n:
  names = faker.name()
  nameList.append(names)

generateIban()
generateName()
print(ibanList)
print(nameList)