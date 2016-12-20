import os

_dir = os.path.dirname(os.path.abspath(__file__))

credential_dir = os.path.join(_dir, '.credentials')
client_secret_file = os.path.join(credential_dir, 'client_secret.json')

"""
Sheet should already exist, and have headers: 'Time' in A1 and 'External IP' in B1
Timestamps and IP addresses will be written in these columns,
and the last IP will be overwritten in cell D1
"""
sheet_id = '1oBdU8j-1Au4weXYzab-WZNHWVy4ES-_n7Ytqnsc-3ts'

