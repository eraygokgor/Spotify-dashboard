# Spotify Dashboard
This app is designed to help you to explore the data given by Spotify API via Flask framework.

## Installation
After downloading th repository, you should create a file named `.env` in the root directory of the project. This file should contain the following variables:
``` python
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
```
Then, you should create a virtual environment and install the requirements by typing the following commands in the terminal:
``` bash
conda env create -n <your-env-name> python=3.11.5
conda activate <your-env-name>
pip install -r requirements.txt
```


### How to get credentials?
1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
2. Click on `CREATE AN APP` button.
3. Fill the form and click on `CREATE` button. While filling, you should remember the `Redirect URIs` field. It should be `http://127.0.0.1:5000/callback`
4. After creating the app, you will see your `Client ID` and `Client Secret`. Copy them and paste into `.credentials.py` file as mentioned above.

## Usage
After handling the installation process, you can run the app by typing `python app.py` in the terminal. Then, you can go to `http://127.0.1:5000` in your browser and use the app.
In the index page, you fill find the following, and click `Authenticate`. <br>

At that point, you will be redirected to Spotify login page. After logging in, you will be redirected to the dashboard page. <br>

## Future Work
- [ ] Add more features to the dashboard page as much as Spotify API data allows.
- [ ] Improve the UI.
- [ ] Fix the bug in the recently played on mobile. 
- [ ] Add more statistics to the dashboard page.
- [ ] Create a public app which totally free and secure.
