import webbrowser
from urllib.parse import urlparse
import requests
import base64

spotify_authorize_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"

def create_url(base, query_list):
    finished_url = base + '?'
    for var in query_list:
        finished_url += "{0}={1}&".format(var, query_list[var])
    return finished_url.rstrip("&")

# Load Enviromental Variable Information
def parse_vars(var_string):
    env_options = {}
    for line in var_string:
        line_formated = line.split('=')
        env_options[line_formated[0].rstrip('\n')] = line_formated[1].rstrip('\n')
    return env_options


# Get Access Token
def authorize_application(env_options):
    authorize_parems = {"client_id": env_options["SPOTIFY_CLIENT_ID"], "response_type": "code", "redirect_uri": env_options['REDIRECT_URI'], "scope": "user-read-private"}
    authorize_url = create_url(spotify_authorize_url, authorize_parems)
    webbrowser.open(authorize_url)

    auth_code_redirect = input("Paste the url that you were directed to after logging in:\n")
    auth_code_redirect_query = urlparse(auth_code_redirect).query.split('&')
    auth_code = parse_vars(auth_code_redirect_query)['code']
    return auth_code

def get_tokens(auth_code, env_options):
    token_request_body = {"grant_type": "authorization_code", "code": auth_code, "redirect_uri": env_options["REDIRECT_URI"]}
    app_info_encoded = base64.b64encode("{}:{}".format(env_options["SPOTIFY_CLIENT_ID"], env_options["SPOTIFY_CLIENT_SECRET"]).encode("utf-8"))
    token_request_header = {"Authorization": "Basic {}".format(str(app_info_encoded, "utf-8"))}

    result = requests.post(spotify_token_url, headers=token_request_header, data=token_request_body)
    print(result.text)

env_options = parse_vars(open('.env', 'r').readlines())
auth_code = authorize_application(env_options)
get_tokens(auth_code, env_options)

