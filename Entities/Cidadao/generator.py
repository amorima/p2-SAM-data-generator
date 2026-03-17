from faker import Faker

faker = Faker('pt_PT')

for _ in range(10):
 generatedAddress = faker.address()
 generatedNames = faker.name()
 # print(generatedNames)
print(generatedAddress)