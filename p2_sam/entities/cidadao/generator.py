import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import math
import json
import csv
import time
from pathlib import Path
from faker import Faker
import pgeocode

# Configuração 

faker      = Faker("pt_PT")
geo        = pgeocode.Nominatim("PT")
OUTPUT_DIR = Path(__file__).parent.parent / "output"
N          = 100


# cp = faker.postcode()
# r = cp.replace("-", "")

cp = faker.postcode()
r  = geo.query_postal_code(cp)
print(cp)
print(r)