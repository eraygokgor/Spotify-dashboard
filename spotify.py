from flask import Flask, redirect, request, render_template, session
from urllib.parse import urlencode
from credentials import CLIENT_ID, CLIENT_SECRET
from functions import generate_random_string, base64_encoder, sha256_hash
import requests

# Spotify API credentials
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = 'http://127.0.0.1:5000/callback'

# Spotify API endpoints
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes required by your application
SPOTIFY_SCOPES = ['user-read-private', 'user-read-email', 'user-top-read', 'user-follow-read',
                  'user-read-recently-played']

app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/index')
def index():
    return render_template('html/index.html')


@app.route('/login')
def authorize():
    code_verifier = generate_random_string(64)
    # Store the code verifier in local storage to use later to exchange for a token
    session['code_verifier'] = code_verifier
    code_challenge = base64_encoder(sha256_hash(code_verifier))

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(SPOTIFY_SCOPES),
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    auth_url = f'{SPOTIFY_AUTH_URL}?{urlencode(params)}'
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    if request.args.get('error'):
        return request.args.get('error')
    else:
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': session['code_verifier']  # Retrieve the code verifier from local storage
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(SPOTIFY_TOKEN_URL, data=params, headers=headers)
        session['access_token_data'] = response.json()
        return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    access_token = session['access_token_data'].get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # Get Current User's Profile
    response = requests.get(SPOTIFY_API_URL + 'me', headers=headers)
    user_data = response.json()

    # Get a User's Top Artists
    params = {
        'time_range': 'medium_term',  # 'long_term', 'medium_term', 'short_term'
        'limit': 10,
    }
    response = requests.get(SPOTIFY_API_URL + 'me/top/artists', headers=headers, params=params)
    top_artists = response.json()

    # Get a User's Top Tracks
    params = {
        'time_range': 'medium_term',  # 'long_term', 'medium_term', 'short_term'
        'limit': 10,
    }
    response = requests.get(SPOTIFY_API_URL + 'me/top/tracks', headers=headers, params=params)
    top_tracks = response.json()

    # Get User's Recently Played Tracks
    params = {
        'limit': 10,
    }
    response = requests.get(SPOTIFY_API_URL + 'me/player/recently-played', headers=headers, params=params)
    recently_played = response.json()

    return render_template('html/dashboard.html',
                           user_data=user_data,
                           top_artists=top_artists,
                           top_tracks=top_tracks,
                           recently_played=recently_played)


