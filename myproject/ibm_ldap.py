import os

from ldap3 import ALL, Connection, Server
import json

# copied from https://raw.github.ibm.com/LinuxCoC/ldap_auth/master/ldap_auth.py?token=AACA43euqYmkHNleZGzDNhjiLqkk3tHmks5aefsywA%3D%3D


def getDN(email, ldapURL=None):
    """
    Get the DN for an email address

    To authenticated with the LDAP we first need to figure out their UID
    In the case of IBM this UID is your serial number, which is not as user
    friendly as just asking them for their email. This function will search
    the public LDAP interfaces by email and return their UID so you can
    then use that to then do the authentication described below
    """

    # In this example we pass in the LDAP_URL via an environment variable
    # or a parameter to the function
    server = Server(ldapURL or os.getenv('LDAP_URL'))

    # By using the 'with' clause it automatically cleans up (closes) the
    # connection
    with Connection(server) as conn:
        conn.bind()
        conn.search('OU=BLUEPAGES,O=IBM.COM', '(mail=%s)' % email)

        # Result set returned by the search preformed above
        entries = conn.entries

        # If there are multiple entries we don't want to try and assume
        # the UID. Edge case
        if len(entries) > 1:
            #print('Found multiple LDAP entries for email %s' % email)
            return None

        # If the email is incorrect and no results were returned: will
        # need to relay this back to user
        if len(entries) == 0:
            #print('Unable to find an LDAP entry for email %s' % email)
            return None

        entryJSON = json.loads(entries[0].entry_to_json())

        #print('Found DN Entry : %s' % entryJSON['dn'])

        # Return the UID
        return entryJSON['dn']


def auth(email, password, ldapURL=None):
    """Takes in an email and password and attempts to authenticated the user against ldap."""

    # In this example we pass in the LDAP_URL via an environment variable
    # or a parameter to the function
    server = Server(ldapURL or os.getenv('LDAP_URL'))

    dnRecord = getDN(email, ldapURL)

    # We want to make sure that we are able to find the DN
    if dnRecord:

        # By using the 'with' clause it automatically cleans up (closes) the
        # connection
        with Connection(server, dnRecord, password) as conn:

            # This is the function that validates the credentials. If this fails
            # we can say username/pass incorrect, otherwise log them in to your system
            if conn.bind():
                # Succesfully authenticated with LDAP
                return True
            else:
                # Unsuccessfully authenticated with LDAP
                return False
    else:
        #print('Unable to determine UID from the email')
        pass

    return False


from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string

from myproject.settings import LDAP_URL

class IBMLDAPBackend():
    def authenticate(self, request, username=None, password=None):
        """
        Custom LDAP backend as django_uth_ldap is not working
        """
        isAuthenticated = auth(username, password, LDAP_URL)

        if isAuthenticated:
            #print('Successfully authenticated with LDAP')
            try:
                user = User.objects.get(username=username)
                return user
            except Exception as ex:
                #print(ex)
                user = User.objects.create_user(username = username,
                                                email = username,
                                                password = get_random_string())
                #print('Creating User: %s' % user)
                return user

        else:
            #print('Unsuccessfully authenticated with LDAP')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
