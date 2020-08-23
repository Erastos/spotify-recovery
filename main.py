import webbrowser
from urllib.parse import urlparse
import requests
import base64

spotify_authorize_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"
spotify_playlist_get_url = "https://api.spotify.com/v1/me/playlists"

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


# Get Access Code
def authorize_application(env_options):
    authorize_parems = {"client_id": env_options["SPOTIFY_CLIENT_ID"], "response_type": "code", "redirect_uri": env_options['REDIRECT_URI'], "scope": "playlist-read-private"}
    authorize_url = create_url(spotify_authorize_url, authorize_parems)
    webbrowser.open(authorize_url)

    auth_code_redirect = input("Paste the url that you were directed to after logging in:\n")
    auth_code_redirect_query = urlparse(auth_code_redirect).query.split('&')
    auth_code = parse_vars(auth_code_redirect_query)['code']
    return auth_code

# Get Access And Refresh Tokens
def get_tokens(auth_code, env_options):
    token_request_body = {"grant_type": "authorization_code", "code": auth_code, "redirect_uri": env_options["REDIRECT_URI"]}
    app_info_encoded = base64.b64encode("{}:{}".format(env_options["SPOTIFY_CLIENT_ID"], env_options["SPOTIFY_CLIENT_SECRET"]).encode("utf-8"))
    token_request_header = {"Authorization": "Basic {}".format(str(app_info_encoded, "utf-8"))}

    result = requests.post(spotify_token_url, headers=token_request_header, data=token_request_body)
    return result.json()

def get_playlist_tracks(access_token, playlist):
    track_url = playlist["tracks"]["href"]
    track_header = {"Authorization": "Bearer {}".format(access_token)}
    track_request_results = requests.get(track_url, headers=track_header)




    print(track_request_results.text)

# Get Lists of Playlists
def get_playlist(access_token, list_of_playlists, offset):
    get_playlist_header = {"Authorization": "Bearer {}".format(access_token)}
    get_playlist_query = {"limit": "50", "offset": offset}
    result = requests.get(spotify_playlist_get_url, headers=get_playlist_header, params=get_playlist_query)
    get_playlist_tracks(access_token, result.json()["items"][0])

env_options = parse_vars(open('.env', 'r').readlines())
auth_code = authorize_application(env_options)
access_token = get_tokens(auth_code, env_options)["access_token"]
playlists = []
get_playlist(access_token, playlists, 0)

