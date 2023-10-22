import argparse

import msal

SCOPES = ["xboxlive.signin", "xboxlive.offline_access"]


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    arguments = parser.parse_args()

    app = msal.ConfidentialClientApplication(
        client_id=arguments.client_id,
        client_credential=arguments.client_secret,
        authority="https://login.microsoftonline.com/consumers",
    )
    url = app.get_authorization_request_url(scopes=SCOPES)
    print(f"Open '{url}' in your browser and login: ")
    code = input("Please enter the code and hit enter:")

    response = app.acquire_token_by_authorization_code(code=code, scopes=SCOPES)
    print("The refresh_token is in the following response")
    print(response)


if __name__ == "__main__":
    run()
