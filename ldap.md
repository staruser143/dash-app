docker run --name my-openldap-container -p 389:389 -p 636:636 \
-e LDAP_ORGANISATION="sri" -e LDAP_DOMAIN="sri.example.com" \
-e LDAP_ADMIN_PASSWORD="admin" --detach osixia/openldap:

docker exec -it my-openldap-container bash
ldapsearch -x -H ldap://localhost -b "dc=sri,dc=example,dc=com" -D "cn=admin,dc=sri,dc=example,dc=com" -w admin

dn: uid=johndoe,ou=users,dc=sri,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: top
cn: John Doe
sn: Doe
uid: johndoe
uidNumber: 1000
gidNumber: 1000
homeDirectory: /home/johndoe
loginShell: /bin/bash
mail: johndoe@sri.example.com
userPassword: {SSHA}examplePasswordHash

ldapadd -x -D "cn=admin,dc=sri,dc=example,dc=com" -w admin -f add_user.ldif

ldapadd -x -D "cn=admin,dc=sri,dc=example,dc=com" -w admin -f create_ou.ldif