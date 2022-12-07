# Emby2Kavita
python script to invite users from emby to kavita

I am not firmiliar with python so this is very rough but should work.

## Invite Process:
1. Pulls list of Emby Connect emails attached to users on your Emby server
2. Finds the Emby Connect emails that don't exist in Kavita
3. Invites users that are missing in Kavita (not including users with pending invites)
4. Resends pending invite emails (WIP, currently does this every run)

## Requirements
kavitapy
requests
json

## Tested on:
Emby - v4.7.10.0
Kavita - v0.6.1
KavitaEmail (using Gmail) - v0.1.10
Python - v3.10
