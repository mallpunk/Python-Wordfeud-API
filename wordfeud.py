from hashlib import sha1
import requests

USER_AGENT = "Python Wordfeud API 0.2"

# Wordfeud API client
# Based on PHP-Wordfeud-API (TODO url, attribution)
class Wordfeud:

    # Rule sets
    RuleSetAmerican = 0
    RuleSetNorwegian = 1
    RuleSetDutch = 2
    RuleSetDanish = 3
    RuleSetSwedish = 4
    RuleSetEnglish = 5
    RuleSetSpanish = 6
    RuleSetFrench = 7

    # Board types
    BoardNormal = 0
    BoardRandom = 1


    #
    # Init a new Wordfeud object.
    # Notice that all the parameters are optional.
    #
    # @param string session_id Wordfeud Session ID
    # @param boolean accept_encoding Set to False to disable any encoding of the HTTP response
    # @param boolean debug_mode Set to True to output debug information on each request
    #
    def __init__(self, session_id=None, accept_encoding=True, debug_mode=False):
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if session_id:
            self.session.cookies['sessionid'] = session_id
        self.accept_encoding = accept_encoding
        self.debug_mode = debug_mode

    #
    # Log in to Wordfeud using an email address and password
    #
    # @param string email Email address
    # @param string password Plain text password
    # @throws WordfuedLogInException If login fails
    #
    def login_email(self, email, password):
        url = 'user/login/email'
        data = {
            'email': email,
            'password': self._get_hash(password)
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudLogInException(res["content"]["type"])

    #
    # Log in to Wordfeud using an User ID and password
    #
    # @param type user_id User ID
    # @param type password Plain text password
    # @throws WordfuedLogInException If login fails
    #
    def login_id(self, user_id, password):
        url = 'user/login/id'
        data = {
            'id': int(user_id),
            'password': self._get_hash(password),
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudLogInException(res["content"]["type"])

    #
    # Get the Wordfeud Session ID of the current authenticated user.
    #
    # @return string Wordfeud Session ID
    #
    def get_session_id(self):
        return self.session.cookies.get('sessionid', None)

    #
    # Change the Wordfeud Session ID, in other words:
    # switch to another user.
    #
    # @param string session_id Wordfeud Session ID
    # @return boolean True if the internal value has been changed; False otherwise
    #
    def set_session_id(self, session_id):
        if session_id != self.session.cookies.get('sessionid', None):
            self.session.cookies['sessionid'] = session_id
            return True
        else:
            return False

    #
    # Unsets the internal Wordfeud Session ID.
    # You'll no longer be able to do any authenticated
    # calls until you login again.
    #
    def logout(self):
        self.session.close()
        self.session = None

    #
    # Search for a Wordfeud user
    #
    # @param string query Username or email address
    # @return array Search results
    #
    def search_user(self, query):
        url = 'user/search'

        data = {
            "username_or_email": query,
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["result"]


    #
    # Retrieve a list of your friends (relationships)
    #
    # @return array List of friends
    #
    def get_friends(self):
        url = 'user/relationships'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"].relationships

    #
    # Add a user to your list of friends (relationships)
    #
    # @param int user_id ID of the User you wish to add
    # @param int type Unknown?
    # @return array
    #
    def add_friend(self, user_id, friend_type=0):
        url = 'relationship/create'

        data = {
            "id": int(user_id),
            "type": int(friend_type),
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]

    #
    # Remove a user from your list of friends
    #
    # @param int user_id ID of the User your wish to 'unfriend'
    #
    def delete_friend(self, user_id):
        url = f'relationship/{int(user_id)}/delete'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])

    #
    # Search for a random opponent to play a game with.
    #
    # @param int ruleset Ruleset for the game
    # @param mixed board_type Board Type
    # @return array
    #
    def invite_random_opponent(self, ruleset, board_type=BoardRandom):
        url = "random_request/create"

        # TODO Test if an integer can be passed to the API
        if board_type == self.BoardNormal:
            board_type = "normal"
        elif board_type == self.BoardRandom:
            board_type = "random"

        data = {
            "ruleset": int(ruleset),
            "board_type": board_type,
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]

    #
    # Upload a new avatar
    #
    # @param string image_data Still need to figure out what this string contains?
    #
    def upload_avatar(self, image_data):
        url = "user/avatar/upload"

        # TODO Figure out how to generate this image data from an actual image

        data = {
            "image_data": image_data,
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])

    #
    # Get all of the chat messages from a specific game
    #
    # @param int game_id Game ID
    # @return array
    #
    def get_chat_messages(self, game_id):
        url = f"game/{int(game_id)}/chat"

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"].messages

    #
    # Send a chat message in a specific game
    #
    # @param int game_id Game ID
    # @param string message The message you wish to send
    # @return array
    #
    def send_chat_message(self, game_id, message):
        url = f"game/{int(game_id)}/chat/send"

        data = {
            "message": message.strip(),
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]

    #
    # Gets the URL of the User's avatar
    #
    # @param int user_id ID of the User
    # @param int size Size (sizes known to work: 40, 60)
    # @return string
    #
    def get_avatar_url(self, user_id, size):
        return f"http://avatars.wordfeud.com/{int(size)}/{int(user_id)}"

    #
    # Create an account
    #
    # @param string username
    # @param string email
    # @param string password
    # @return int Your new User ID if successful
    #
    def create_account(self, username, email, password):
        url = 'user/create'
        data = {
            'username': username,
            'email': email,
            'password': self._get_hash(password)
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["id"]

    #
    # Gets notifications!
    #
    # @return array An array with notifications
    #
    def get_notifications(self):
        url = 'user/notifications'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["entries"]

    #
    # Gets status! (Pending invites, current games, etc)
    #
    # @return array An array with statuses
    #
    def get_status(self):
        url = 'user/status'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]

    #
    # Get games!
    #
    # @return array An array with games
    #
    def get_games(self):
        url = 'user/games'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["games"]

    #
    # Get one game
    #
    # @param int game_id Game ID
    # @return array An array with game data
    #
    def get_game(self, game_id):
        url = f'game/{game_id}'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["game"]

    #
    # Get the layout of a board
    #
    # @param int board_id
    # @return array
    #
    def get_board(self, board_id):
        url = f'board/{board_id}'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])
        else:
            return res["content"]["board"]

    #
    # Place a word on the board. This should be much easier.
    #
    # @param int game_id
    # @param array ruleset
    # @param array tiles
    # @param array words
    # @return Object
    #
    def place(self, game_id, ruleset, tiles, words):
        # 'illegal_word', 'illegal_tiles'
        # TODO Have a look at the response

        url = f'game/{game_id}/move'

        data = {
            'move': tiles,
            'ruleset': ruleset,
            'words': [words],
        }

        res = self._execute(url, data)

        return res

    # 'not_your_turn'
    def skip_turn(self, game_id):
        url = f'game/{game_id}/pass'

        res = self._execute(url)

        return res

    # 'not_your_turn', 'game_over'
    def resign(self, game_id):
        url = f'game/{game_id}/resign'

        res = self._execute(url)

        if res["status"] == "success":
            return True

        return res["content"]["type"]

    #
    # Invite somebody to a game
    #
    # @return True|string 'duplicate_invite', 'invalid_ruleset', 'invalid_board_type', 'user_not_found'
    #
    def invite(self, username, ruleset=0, board_type=BoardRandom):
        url = 'invite/new'

        if board_type == self.BoardNormal:
            board_type = "normal"
        elif board_type == self.BoardRandom:
            board_type = "random"

        data = {
            'invitee': username,
            'ruleset': ruleset,
            'board_type': board_type
        }

        res = self._execute(url, data)

        return res

    #
    # Accept an invite.
    #
    # @param int invite_id Invite ID
    #
    def accept_invite(self, invite_id):
        # 'access_denied'
        url = f'invite/{invite_id}/accept'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])

    #
    # Reject an invite.
    #
    # @param int invite_id Invite ID
    #
    def reject_invite(self, invite_id):
        # 'access_denied'
        url = f'invite/{invite_id}/reject'

        res = self._execute(url)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])

    #
    # Change your password
    #
    # @param string password New password (plain text)
    #
    def change_password(self, password):
        url = 'user/password/set'
        data = {
            'password': self._get_hash(password),
        }

        res = self._execute(url, data)

        if res["status"] != "success":
            raise WordfeudException(res["content"]["type"])

    #
    # Hash the password for use with the API.
    #
    # @param string password Plain text password
    # @return strong SHA1 hash of the password with added salt
    #
    # TODO verify if utf-8 is actually the proper encoding. Does WordFeud allow non-ASCII
    # characters in passwords?
    #
    def _get_hash(self, password):
        password += 'JarJarBinks9'  # Add salt
        password = password.encode('utf-8') # The sha1 function takes a bytes object.
        return sha1(password).hexdigest()


    def _execute(self, url, data=None):
        if not data:
            data = {}

        url = f"http://game06.wordfeud.com/wf/{url}/"
        #  # cURL Options
        #  opt_array = {
        #      # LP TODO
        #      # CURLINFO_HEADER_OUT: True,
        #      # CURLOPT_RETURNTRANSFER: True,
        #      # CURLOPT_HEADER: True,
        #
        #      # LP DONE:
        #      # CURLOPT_FOLLOWLOCATION: True,
        #      # CURLOPT_POST: True,
        #      # CURLOPT_HTTPHEADER: headers,
        #      # CURLOPT_POSTFIELDS: json_encode(data),
        #  }

        # LP TODO
        #  # Use encoding if possible?
        #  if self.accept_encoding:
        #      opt_array[CURLOPT_ENCODING] = ""

        #  self.debug_log("cURL Options", a)

        r = self.session.post(url, json=data)
        if r.status_code != requests.codes['ok']:
              raise WordfeudHttpException(r.status_code)

        self.debug_log("Headers", r.headers)
        self.debug_log("Response", r.text)
        self.debug_log("Cookies", r.cookies)

        res = r.json()
        if not isinstance(res, dict):
            raise WordfeudJsonException("Could not decode JSON")
        self.debug_log("Decoded JSON", res)

        return res


    # LP TODO
    def debug_log(self, title, data):
        if self.debug_mode:
            title = title.strip()
            output = f"\n\n{title}\n"
            output += len(title) * "-"
            output += f"\n{str(data)}\n\n"

            print(output)

#
# General exception for the Wordfeud class.
# Also functions as the parent of all the other
# exceptions this class might throw, so you can
# easily catch them.
#
class WordfeudException(Exception):
    pass

#
# This exception is thrown when the log in failed
# or when we tried to make an authenticated call
# but failed because of invalid credentials or an
# invalid session id.
#
class WordfeudLogInException(WordfeudException):
    pass

#
# Exceptions of this type are thrown whenever
# something goes wrong with the HTTP request
# or the response we get.
#
class WordfeudClientException(WordfeudException):
    pass

#
# This exception is thrown if we the Wordfeud
# API server returns a HTTP status code other
# thane 200 OK.
#
class WordfeudHttpException(WordfeudClientException):
    pass

#
# This exception is thrown when PHP is
# unable to decode the JSON data we
# have received from the API server.
#
class WordfeudJsonException(WordfeudClientException):
    pass
