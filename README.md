# Emby2Kavita
python script to automatically invite users from emby to kavita

I'm not firmiliar to Python so this is very rough but should work.   Can be triggered on a cron, or via emby-scripterx on usercreate.

## Invite Process:
1. Pulls list of Emby Connect emails attached to users on your Emby server
2. Finds the Emby Connect emails that don't exist in Kavita
3. Invites users that are missing in Kavita (not including users with pending invites)

## Requirements
kavitapy
requests
json

## Tested on:
Emby - v4.7.10.0

Kavita - v0.6.1

KavitaEmail (using Gmail) - v0.1.10

Python - v3.10
