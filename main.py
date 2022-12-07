import kavitapy
import requests
import json


def main():
    kavita_api_key = "xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"
    kavita_domain_name = "https://" #NO TRAILING /

    emby_domain_name = "https://" # NO TRAILING /
    emby_api_key = "xxxxxxxxxxx"

    # Create the JWT from Kavita Info
    jwt = kavitapy.Reader(kavita_domain_name, kavita_api_key).token

    # Gets the Emby Connect Users
    connectusers = get_emby_users(emby_domain_name, emby_api_key)
    print('emby connect users:', connectusers)

    # Finds the missing emails in Kavita
    missing_emails = dupe_checker(kavita_domain_name, connectusers, jwt)
    print('missing:', missing_emails)

    pending_invite = kavita_pending_id(kavita_domain_name, jwt)
    print('pending invite id:', pending_invite)

    kavita_resend_email(kavita_domain_name, jwt, pending_invite)

    # Parse users to inviter
    for email in missing_emails:
        invite(kavita_domain_name, email, jwt)


###########################
# EMBY
###########################
def get_emby_users(emby_domain_name, emby_api_key):
    headers = {
        'accept': 'application/json',
    }
    params = {
        'IsDisabled': 'false',
        'api_key': emby_api_key,
    }

    response = requests.get(emby_domain_name + '/emby/Users/Query', params=params, headers=headers)

    connectusers = []

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        for item in data['Items']:
            if item.get('ConnectUserName') is not None:
                connectusers.append(item.get('ConnectUserName'))

    return connectusers


###########################
# KAVITA INVITES
###########################
def dupe_checker(kavita_domain_name, connectusers, jwt):
    # Get list of all Kavita Email Addresses
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
    }
    response = requests.get(kavita_domain_name + '/api/Users', headers=headers)

    kavitausers = []

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        for item in data:
            if item.get('email') is not None:
                kavitausers.append(item.get('email'))
                print(item.get('email'))

    # Compare list of Kavita Emails Addresses to Emby Email Addresses and return outputs

    set1 = set(kavitausers)
    set2 = set(connectusers)

    missing = list(sorted(set2 - set1))
    return missing


def kavita_pending_id(kavita_domain_name, jwt):
    # Get list of all Kavita Email Addresses
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
    }
    response = requests.get(kavita_domain_name + '/api/Users/pending', headers=headers)

    kavitaid = []

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        for item in data:
            if item.get('id') is not None:
                kavitaid.append(item.get('id'))
                print(item.get('id'))

    return kavitaid


def kavita_resend_email(kavita_domain_name, jwt, kavitaid):
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = {
        'userId': id,
    }


def invite(domain_name, email, jwt):
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
        'Content-Type': 'application/json',
    }
    json_data = {
        'email': email,
        'roles': [
            'Download',
            'Bookmark',
            'Change Restriction',
        ],
        'libraries': [
            1, 2, 3
        ],
        'ageRestriction': {
            'ageRating': -1,
            'includeUnknowns': False,
        },
    }
    response = requests.post(domain_name + '/api/Account/invite', headers=headers, json=json_data)

    if response.status_code == 200:
        print("invite: send successfully")


#
# Main Function do not move
#

if __name__ == '__main__':
    main()
