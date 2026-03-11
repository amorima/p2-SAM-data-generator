from faker.providers import BaseProvider


class PortugalProvider(BaseProvider):

    def nif(self):
        return self.generator.regexify(r"[1-9][0-9]{8}")

    def telefone(self):
        return self.generator.regexify(r"9[1236][0-9]{7}")

    def postal_code_pt(self):
        return self.generator.regexify(r"([1-8][0-9]{3}|9[0-8][0-9]{2}|99[0-8][0-9]|9990)-[0-9]{3}")