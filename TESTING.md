# Testing the Wordfeud API

This document explains how to test the Python Wordfeud API client.

## Setup

### 1. Configure Credentials

Create a `credentials.py` file with your Wordfeud login information:

```python
# Wordfeud login credentials
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

# Optional: Session ID if you want to reuse an existing session
SESSION_ID = None
```

**Important**: The `credentials.py` file is excluded from version control for security reasons.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

The easiest way to perform basic checks is to run the automated test script:

```bash
python3 test_basic.py
```

This will run 5 basic tests that check:
1. ✅ Object initialization
2. ✅ Session management
3. ✅ Password hashing
4. ✅ API connectivity
5. ✅ Exception classes

## What the Tests Check

### Basic Functionality Tests
- **Object Creation**: Verifies the Wordfeud class can be instantiated
- **Session Management**: Tests setting/getting session IDs and logout functionality
- **Password Hashing**: Ensures the password hashing algorithm works correctly
- **API Connectivity**: Tests that the API server is reachable (without authentication)
- **Exception Classes**: Verifies all custom exception classes can be created

### What's NOT Tested
These tests don't require real Wordfeud credentials and don't test:
- User authentication (login/logout)
- Game creation and management
- User search with real data
- Game moves and gameplay

## Testing with Real Credentials

To test the full functionality:

1. **Create a Wordfeud account** at https://wordfeud.com
2. **Configure credentials** in `credentials.py`
3. **Run the example script**:
   ```bash
   python3 example_usage.py
   ```
4. **Run rating analysis**:
   ```bash
   python3 rating_analysis.py
   ```

## Example Usage

```python
from wordfeud import Wordfeud
from credentials import EMAIL, PASSWORD

# Create client
wf = Wordfeud()

# Login
wf.login_email(EMAIL, PASSWORD)

# Search for users
results = wf.search_user("some_username")

# Get your games
games = wf.get_games()

# Get rating information
rating_data = analyze_ratings()
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you have the `requests` library installed:
   ```bash
   pip install requests
   ```

2. **Credentials Error**: Ensure your `credentials.py` file is properly configured

3. **Authentication Errors**: Ensure your Wordfeud credentials are correct

4. **Network Issues**: Check your internet connection and that the Wordfeud servers are accessible

### Debug Mode

Enable debug mode to see detailed API requests and responses:

```python
wf = Wordfeud(debug_mode=True)
```

## API Features

The API supports:
- User authentication (email/password)
- User search
- Game management
- Chat functionality
- Friend management
- Avatar uploads
- Multiple rule sets (American, Norwegian, Dutch, etc.)
- Different board types (Normal, Random)
- **Rating information** (from finished games)

For more details, see the `wordfeud.py` file and the example usage script. 