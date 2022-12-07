import kavitapy
import requests
import json


def main():
    ##################
    # START OF CONFIG
    ##################

    emby_domain_name = 'https://x' #NO TRAILING /
    emby_api_key = ''

    kavita_domain_name = 'https://read.solostream.org' #NO TRAILING /
    kavita_api_key = 'xxxxxx-xxxx-xxxx-xxxx-xxxxxxxx' #INCLUDE DASHES
    roles = ['Download', 'Bookmark', 'Change Restriction']
    libraries = [1, 2, 3] 

    ##################
    # END OF CONFIG
    ##################

    # 1. Get JWT from Kavita Info
    jwt = kavitapy.Reader(kavita_domain_name, kavita_api_key).token

    # 2. Get Emby Connect Users
    connect_users = get_emby_users(emby_domain_name, emby_api_key)
    print('emby connect users:', connect_users)

    # 3. Get missing emails in Kavita
    missing_emails = dupe_checker(kavita_domain_name, connect_users, jwt)
    print('missing:', missing_emails)

    # 4. Post invite via Kavita
    for email in missing_emails:
        invite(kavita_domain_name, email, jwt, roles, libraries)


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

    connect_users = []

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        for item in data['Items']:
            if item.get('ConnectUserName') is not None:
                connect_users.append(item.get('ConnectUserName'))

    return connect_users


###########################
# KAVITA
###########################
def dupe_checker(kavita_domain_name, connect_users, jwt):
    # Get list of all Kavita Email Addresses
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
    }
    response = requests.get(kavita_domain_name + '/api/Users', headers=headers)

    kavita_users = []

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        for item in data:
            if item.get('email') is not None:
                kavita_users.append(item.get('email'))
                print(item.get('email'))

    # Compare list of Kavita Emails Addresses to Emby Email Addresses and return outputs

    set1 = set(kavita_users)
    set2 = set(connect_users)

    missing = list(sorted(set2 - set1))
    return missing


def invite(domain_name, email, jwt, roles, libraries):
    headers = {
        'accept': 'text/plain',
        'Authorization': jwt,
        'Content-Type': 'application/json',
    }
    json_data = {
        'email': email,
        'roles': roles,
        'libraries': libraries,
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
