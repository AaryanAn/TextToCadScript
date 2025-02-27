# TextToCadScript

This repository contains a Python script (`textcad.py`) that demonstrates how to use Zoo's Text-to-CAD API endpoint via the KittyCAD Python package. The script allows you to enter a text prompt describing a CAD model, then generates an STL file based on that prompt. The output file is automatically named after your input prompt.

## Features

- **Text-to-CAD Generation:** Submit a text prompt (e.g., "Design a gear with 40 teeth") to generate a CAD model.
- **Polling:** The script polls the API until the CAD model generation is complete.
- **STL Output:** Saves the generated STL file with a filename based on your prompt.
- **Secure API Token Management:** Uses an environment variable to securely manage your API token.

## Requirements

- Python 3.x
- [KittyCAD](https://pypi.org/project/kittycad/) Python package

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AaryanAn/TextToCadScript.git
   cd TextToCadScript

2. **Install Required Packages:**

   ```bash
   pip install kittycad

Obtaining an API Key
--------------------

To use this script, you must have a valid Zoo API token. Follow these steps:

1.  **Create an Account:**\
    Sign up on Zoo's platform if you don't already have an account.

2.  **Sign In:**\
    Log in to your account.

3.  **Generate an API Token:**\
    Navigate to the API Tokens section in your account settings. Generate a new API token and copy it.\
    **Important:** Do not share your API token publicly or commit it to version control.
