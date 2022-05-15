from time import time as timestamp
from datetime import datetime
import pyotp
import base64
import re
import os
import hashlib
import subprocess

# unique seed for generate key
seed = 42346542

# license may have period, now it's infinity.
def get_mounth():
    ts = timestamp()
    dt = datetime.fromtimestamp(ts).strftime("%Y-%m-01")
    dt_ts = datetime.strptime(dt, "%Y-%m-%d")
    return datetime.timestamp(dt_ts)
 
def get_crypted_uuid():
    x = subprocess.check_output('wmic csproduct get UUID')
    x = re.sub(r"[\W]+", "", str(x)).replace("rrn", "")[1:]
    crypted_uuid = hashlib.sha224(x.encode()).hexdigest()
    return crypted_uuid

def create_lic(licence: str):
    with open("lic.licensefile", "w", encoding="utf-8") as f:
        f.write(str(licence))

def get_lic_key(licence):
    otp = pyotp.TOTP(base64.b32encode(str(licence).encode()))
    key = otp.at(seed)
    lic_key = hashlib.sha224(base64.b32encode(str(key).encode())).hexdigest()

    lic_key = lic_key[:16].upper()
    for i in range(4):
        lic_key = "-".join([lic_key[:i*5], lic_key[i*5:]])
    lic_key = lic_key[1:]

    return lic_key

def check_licence():
    uuid = get_crypted_uuid()
    # get hardware id

    if os.path.isfile("lic.licensefile") is False:
        # create if not exist
        create_lic(uuid)
    else:
        # if uuid don't match, rewrite file.
        with open("lic.licensefile") as f:
            if uuid not in f.read():
                create_lic(uuid)

    # generate license key 
    license = get_lic_key(uuid)
    with open("lic.licensefile", "r", encoding="utf-8") as l:
        lic_file = l.read()

    if license in lic_file:
        return True
    else:
        uz_lic = input("Введите лицензионный ключ: ")

        while uz_lic.replace(" ", "") != license:
            print("Неверный лицензионный ключ, проверьте правельность введённых данных.\nЕсли ключ всё равно не подходит, обратитесь к создателю ")
            uz_lic = input("Введите лицензионный ключ снова: ")

        with open("lic.licensefile", "a", encoding="utf-8") as l:
            l.write("\n" + license)

        print("Лицензия успешно активирована!")
        return True

if __name__ == "__main__":
    while True:
        k = input("Input key (user uuid): ") 
        print(get_lic_key(k))

"""
Example:
# in code
from license import check_licence
check_licence()

"""