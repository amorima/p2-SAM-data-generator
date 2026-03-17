import re

IBAN = re.compile(r"^PT500067[0-9]{17}$")
POSTAL_CODE = re.compile(r"^([1-8][0-9]{3}|9[0-8][0-9]{2}|99[0-8][0-9]|9990)-[0-9]{3}$")
NIF = re.compile(r"^39\d{7}$")
NIPC = re.compile(r"^59\d{7}$")
NIF_ADMINISTRACAO = re.compile(r"^69\d{7}$")
