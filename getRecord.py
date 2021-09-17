import secrets
import requests
import time


secretsVersion = input('To edit production server, enter the name of the secrets file: ')
if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Stage')
else:
    print('Editing Stage')

key = secrets.key
secret = secrets.secret
oclcSymbol = secrets.oclcSymbol
registryID = secrets.registryID
principalID = secrets.principalID
principalIDNS = secrets.principalIDNS
# sandboxRecords = secrets.sandboxRecords

baseURL = 'https://worldcat.org'

# Client Credentials Grant OAuth pattern.

session = requests.Session()
session.auth = (key, secret)

# Get an access token for WorldCat Metadata API.
authURL = 'https://oauth.oclc.org/token'
grant_type = 'client_credentials'
scope = 'WorldCatMetadataAPI'
params = {'grant_type': grant_type, 'scope': scope}

r = session.post(authURL, params=params).json()
access_token = r['access_token']
print(access_token)

# Create authorization header.
auth_header = 'Bearer {} , principalID="{}", principalIDNS="{}"'.format(access_token, principalID, principalIDNS)
headers = {'Authorization': auth_header,
           'Accept': 'application/atom+xml;content="application/vnd.oclc.marc21+xml"'}

file = open('marc.marcxml', 'w')

# Make request.
oclcNumbers = ['122412607', '1138904123']
for oclc in oclcNumbers:
    r = requests.get(baseURL+'/bib/data/'+oclc, headers=headers)
    text = r.text
    file.write(text)
file.close()
