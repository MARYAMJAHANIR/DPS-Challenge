import requests
import json

# Fill in your details
github_repo = "https://github.com/MARYAMJAHANIR/DPS-Challenge"
email = "maryamjahangir593@gmail.com"
deployed_endpoint = "https://flaskdeploy.pythonanywhere.com/"
notes = "Thanks for givivng me this chance, hope so I am not too late, I was just sick because of Gummersbach weather, excited for the next step:) "  # This is optional

# Create the JSON payload
payload = {
    "github": github_repo,
    "email": email,
    "url": deployed_endpoint,
    "notes": notes
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
url = "https://dps-challenge.netlify.app/.netlify/functions/api/challenge"
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    print("Congratulations! Achieved Mission 3")
else:
    print("Failed to complete Mission 3. Status code:", response.status_code)
