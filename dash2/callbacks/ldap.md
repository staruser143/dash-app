docker pull osixia/openldap:latest

docker run -d \
  --name my-openldap-container \
  -p 389:389 -p 636:636 \
  --env LDAP_ORGANISATION="sri" \
  --env LDAP_DOMAIN="sri.example.com" \
  --env LDAP_ADMIN_PASSWORD="Testing123$" \
  osixia/openldap:latest

  docker exec -it my-openldap-container bash

  docker stop my-openldap-container
  docker rm my-openldap-container

  pip install ldap3

  docker ps

docker ps | grep ldap

docker inspect <container_id_or_name>


docker start <container_id_or_name>
docker run [options] <image_name>
docker logs <container_name_or_id>

cat /etc/os-release

docker restart <container_name_or_id>

docker exec -it <container_name_or_id> /bin/bash

docker exec -it ldapcontainer /bin/bash
docker exec -it <ldap_container_name_or_id> /bin/bash

ldapsearch -x -H ldap://localhost -D "cn=admin,dc=example,dc=com" -w password -b "dc=example,dc=com" "(objectclass=*)"


docker run --name openldap \
  --env LDAP_ADMIN_USERNAME=admin \
  --env LDAP_ADMIN_PASSWORD=adminpassword \
  --env LDAP_USERS=customuser \
  --env LDAP_PASSWORDS=custompassword \
  --env LDAP_ROOT=dc=example,dc=org \
  --env LDAP_ADMIN_DN=cn=admin,dc=example,dc=org \
  bitnami/openldap:latest