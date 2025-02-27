TextToCadScript
This repository contains a Python script (textcad.py) that demonstrates how to use Zoo's Text-to-CAD API endpoint via the KittyCAD Python package. The script allows you to enter a text prompt describing a CAD model, then generates an STL file based on that prompt. The output file is automatically named after your input prompt.

Features
Text-to-CAD Generation: Submit a text prompt (e.g., "Design a gear with 40 teeth") to generate a CAD model.
Polling: The script polls the API until the CAD model generation is complete.
STL Output: Saves the generated STL file with a filename based on your prompt.
Secure API Token Management: Uses an environment variable to securely manage your API token.
Requirements
Python 3.x
KittyCAD Python package
Installation
Clone the Repository:

bash
Copy
git clone https://github.com/AaryanAn/TextToCadScript.git
cd TextToCadScript
Install Required Packages:

bash
Copy
pip install kittycad
Obtaining an API Key
To use this script, you must have a valid Zoo API token. Follow these steps:

Create an Account:
Sign up on Zoo's platform if you don't already have an account.

Sign In:
Log in to your account.

Generate an API Token:
Navigate to the API Tokens section in your account settings. Generate a new API token and copy it.
Important: Do not share your API token publicly or commit it to version control.

Setting Up Your Environment
Before running the script, set your API token as an environment variable in your terminal. Do not include your API token in this repository!

For example, in your terminal run:

bash
Copy
export ZOO_API_TOKEN="your-api-token-here"
Note: You will need to set this each time you start a new terminal session, or add the export command to your shell’s configuration file (e.g., ~/.bashrc or ~/.zshrc) for automatic loading.

Usage
Run the Script:

bash
Copy
python textcad.py
Enter a Prompt:
When prompted, enter a description for the CAD model (e.g., "Design a gear with 40 teeth").

Output:
The script will submit your prompt to the API, poll for completion, and save the generated STL file using a name derived from your prompt (for example, if you enter "Design a gear with 40 teeth", the file will be saved as Design_a_gear_with_40_teeth.stl).

Example
If you enter the prompt:

csharp
Copy
Design a gear with 40 teeth
The output file will be saved as:

Copy
Design_a_gear_with_40_teeth.stl
License
(Include your license information here if applicable.)

Acknowledgements
Zoo Text-to-CAD API
KittyCAD Python Package
