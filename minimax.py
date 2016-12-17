from google.appengine.api import urlfetch
import urllib
import json


class MiniMaxOrganisation:
    def __init__(self, name, org_id, resource_url):
        self.name = name
        self.org_id = org_id
        self.resource_url = resource_url


class MiniMax:
    def __init__(self, username, password, client_id, client_secret, grant_type="password"):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.auth_result = None
        self.auth_token = None
        self.organisations = []
        self.root_url = "https://moj.minimax.si/demo/si"

    def connect(self):
        """Connect to MiniMAX API, get token and a list of organizations connected to the account."""
        get_token_url = self.root_url + "/aut/oauth20/token"

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "username": self.username,
            "password": self.password
        }

        form_data = urllib.urlencode(params)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        result = urlfetch.fetch(url=get_token_url, payload=form_data, method=urlfetch.POST, headers=headers)

        self.auth_result = result
        self.auth_token = json.loads(result.content)["access_token"]
        self._get_organizations()

    def _get_organizations(self):
        """Get a list of all organisations that belong to the account."""
        url = self.root_url + "/api/api/currentuser/orgs"

        headers = {"Authorization": "Bearer {}".format(self.auth_token)}

        result = urlfetch.fetch(url=url, method=urlfetch.GET, headers=headers)

        rows = json.loads(result.content)["Rows"]

        for row in rows:
            org = MiniMaxOrganisation(name=row["Organisation"]["Name"],
                                      org_id=row["Organisation"]["ID"],
                                      resource_url=row["Organisation"]["ResourceUrl"])
            self.organisations.append(org)

        return result

    def issue_invoice(self):
        pass
