import kavitapy
import requests
import json


class bcolors:
    HEADER = '\033[95m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'


def main():
    ##################
    # START OF CONFIG
    ##################

    emby_domain_name = '' # https://url or http://url
    emby_api_key = '' # 32 Character API Key

    kavita_domain_name = '' # https://url or http://url
    kavita_api_key = '' # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    roles = ['Download', 'Bookmark', 'Change Restriction'] # 'Download', 'Bookmark', 'Change Restriction'
    libraries = [1, 2, 3] # 1, 2, 3, etc

    debug = False

    ##################
    # END OF CONFIG
    ##################

    # Config Validation
    if bool(emby_domain_name) is False:
        raise ValueError('CONFIG | Emby domain name value is blank.')
    if bool(emby_api_key) is False:
        raise ValueError(bcolors.WARNING + 'CONFIG | Emby API key value is blank.')
    if bool(kavita_domain_name) is False:
        raise ValueError(bcolors.WARNING + 'CONFIG | avita domain name value is blank.')
    if bool(kavita_api_key) is False:
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita api key value is blank.')
    if bool(roles) is False:
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita roles value is blank.')
    if bool(libraries) is False:
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita libraries value is blank.')
    if '-' not in kavita_api_key:
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita API Key value is missing dash characters.')
    if '-' in emby_api_key:
        raise ValueError(bcolors.WARNING + 'CONFIG | Emby API Key does not use special characters.')
    if kavita_domain_name.endswith('/'):
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita Domain name can not have a trailing slash.')
    if emby_domain_name.endswith('/'):
        raise ValueError(bcolors.WARNING + 'CONFIG | Kavita Domain name can not have a trailing slash.')

    # 1. Get JWT from Kavita Info
    try:
        jwt = kavitapy.Reader(kavita_domain_name, kavita_api_key).token
    except Exception:
        print(bcolors.WARNING + 'JWT | Error retrieving Kavita JWT Token.')

    # 2. Get Emby Connect Users
    try:
        connect_users = get_emby_users(emby_domain_name, emby_api_key)
        if debug is True:
            print('DEBUG | Emby Connect Users | ', connect_users)
    except Exception:
        print(bcolors.WARNING + 'Emby Connect | Error retrieving Emby Connect Users.')

    # 3. Get missing emails in Kavita
    try:
        missing_emails = dupe_checker(kavita_domain_name, connect_users, jwt)
        if debug is True:
            print('DEBUG | Missing | ', missing_emails)
    except Exception:
        print(bcolors.WARNING + 'Missing Emails | Error generating Kavita JWT Token. Validate Kavita Config.')

    # 4. Post invite via Kavita
    try:
        for email in missing_emails:
            invite(kavita_domain_name, email, jwt, roles, libraries)
    except Exception:
        print(bcolors.WARNING + 'Missing Emails | Error generating Kavita JWT Token. Validate Kavita Config.')


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
        print("Success | Invite | Send Successful", response.status_code)
    else:
        print("Error | Invite | Send Failure with error ", response.status_code)


#
# Main Function do not move
#

if __name__ == '__main__':
    main()
