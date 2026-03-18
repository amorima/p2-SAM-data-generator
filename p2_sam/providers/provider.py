from p2_sam.patterns.regex import IBAN, POSTAL_CODE

IBAN_PATTERN     = r"PT50[0-9]{21}"
POSTAL_PATTERN   = r"([1-8][0-9]{3}|9[0-8][0-9]{2}|99[0-8][0-9]|9990)-[0-9]{3}"

def gerar_iban():
    valor = faker.regexify(IBAN_PATTERN)
    assert IBAN.match(valor)
    return valor