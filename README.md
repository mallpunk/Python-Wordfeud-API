# Python Wordfeud API

A Python client for the Wordfeud API, based on the original PHP code. This package provides a comprehensive interface to interact with Wordfeud's game servers.

## Features

- **Authentication**: Login with email/password or user ID
- **User Management**: Search users, manage friends, upload avatars
- **Game Management**: Create games, make moves, manage invites
- **Rating System**: Retrieve personal ratings by language and board type
- **Chat System**: Send and receive chat messages
- **Multiple Languages**: Support for various Wordfeud rule sets

## Installation

### From PyPI (when published)
```bash
pip install wordfeud-api
```

### From GitHub
```bash
pip install git+https://github.com/mallpunk/Python-Wordfeud-API.git
```

### Development Installation
```bash
git clone https://github.com/mallpunk/Python-Wordfeud-API.git
cd Python-Wordfeud-API
pip install -e .
```

## Quick Start

```python
from wordfeud_api import Wordfeud

# Create client
wf = Wordfeud()

# Login
wf.login_email("your_email@example.com", "your_password")

# Search for users
results = wf.search_user("some_username")

# Get your games
games = wf.get_games()

# Get your current rating (Norwegian, Standard board)
current_rating = wf.get_current_rating(ruleset=1, board_type=0)
print(f"Current Rating: {current_rating['rating']}")

# Get rating statistics
stats = wf.get_rating_stats(ruleset=1, board_type=0)
print(f"Average Rating: {stats['average_rating']}")
```

## Rating System

The API supports retrieving ratings for different languages and board types:

```python
# Norwegian (Bokmål), Standard board
norwegian_rating = wf.get_current_rating(ruleset=1, board_type=0)

# Dutch, Random board  
dutch_rating = wf.get_current_rating(ruleset=2, board_type=1)

# Get all ratings for a specific combination
ratings = wf.get_ratings(ruleset=1, board_type=0)
```

## Available Rule Sets

- `0`: American
- `1`: Norwegian (Bokmål)
- `2`: Dutch
- `3`: Danish
- `4`: Swedish
- `5`: English
- `6`: Spanish
- `7`: French

## Available Board Types

- `0`: Normal (Standard)
- `1`: Random

## Error Handling

The API provides specific exception classes:

```python
from wordfeud_api import WordfeudException, WordfeudLogInException

try:
    wf.login_email("email", "password")
except WordfeudLogInException as e:
    print(f"Login failed: {e}")
except WordfeudException as e:
    print(f"API error: {e}")
```

## Development

This is still a work in progress! The API is based on reverse engineering and may not include all available endpoints.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
