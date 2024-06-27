from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPException, LDAPBindError

# Define the server and the connection
try:
    server = Server('ldap://localhost', get_info=ALL)
    conn = Connection(server, 'cn=admin,dc=example,dc=com', 'admin', auto_bind=True)
except LDAPBindError as e:
    print(f'Bind failed: {e}')
    exit(1)
except LDAPException as e:
    print(f'LDAP error: {e}')
    exit(1)
except Exception as e:
    print(f'Unexpected error: {e}')
    exit(1)

# Perform a search
try:
    conn.search('dc=example,dc=com', '(objectclass=person)', attributes=['cn', 'sn'])
    # Make sure to check if the search was successful and handle results
    if conn.entries:
        print("Search successful. Entries found:")
        for entry in conn.entries:
            print(entry)
    else:
        print("Search successful. No entries found.")
except LDAPException as e:
    print(f'Search failed: {e}')