# xbox-cloud-statistics / backend

## Setup

1. Run `poetry install` to install the dependencies
2. Run `git worktree add ./results origin/results` to checkout the latest results locally (optionally)
3. Create an App registration at Microsoft Azure
   - See https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app
   - Use `Personal Microsoft accounts only` as `Supported account types`
   - `CLIENT_ID` refers to `Application (client) ID` in Azure
   - `CLIENT_SECRET` refers to the value of the client secret in Azure
4. Authenticate as a Xbox Cloud Gaming user
   - Run `poetry run xbox-cloud-authenticate --client-id $CLIENT_ID --client-secret $CLIENT_SECRET`
   - Open the URL displayed in your browser and log in with your Xbox Cloud Gaming account
   - You will be redirected to e.g. `http://localhost/auth/callback?code=...`, paste the `code` into `xbox-cloud-authenticate` and hit enter
   - The output will contain a `refresh_token`
     - If you authenticated with a Free-to-Play account, this this the `F2P_TOKEN`
     - If you authenticated with a Game Pass Ultimate account, this this the `GPU_TOKEN`

## Usage

1. Export environment variables `CLIENT_ID` and `CLIENT_SECRET` to authenticate as the App registration
2. Export environment variables `F2P_TOKEN` and `GPU_TOKEN` to authenticate as the user
3. Run `poetry run xbox-cloud-statistics`, printing a table with the results and writing them to `./results`
