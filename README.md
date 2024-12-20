# xbox-cloud-statistics

A backend and frontend application to gather and visualize the current wait times on Xbox Cloud Gaming.

## Backend

### Setup

1. `cd xbox_cloud_statistics/`
2. `poetry install` to install the dependencies
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
5. Setup InfluxDB (create organization, bucket and API token)

### Usage

1. Export environment variables `CLIENT_ID` and `CLIENT_SECRET` to authenticate as the App registration
2. Export environment variables `F2P_TOKEN` and `GPU_TOKEN` to authenticate as the user
3. Export environment variables `INFLUXDB_URL`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET` and `INFLUXDB_TOKEN` to connect to InfluxDB
4. Run `poetry run xbox-cloud-statistics`, printing a table with the results and writing them to InfluxDB

```
➜  xbox_cloud_statistics git:(main) poetry run xbox-cloud-statistics
| Game                                         | Region             | Subscription     | Server time               |   Wait time (s) |
|----------------------------------------------|--------------------|------------------|---------------------------|-----------------|
| FORTNITE                                     | AustraliaEast      | Subscription.F2P | 2023-10-22 10:05:46+00:00 |             704 |
| FORTNITE                                     | AustraliaEast      | Subscription.GPU | 2023-10-22 10:05:47+00:00 |              38 |
| FORTNITE                                     | AustraliaSouthEast | Subscription.F2P | 2023-10-22 10:05:46+00:00 |             704 |
| FORTNITE                                     | AustraliaSouthEast | Subscription.GPU | 2023-10-22 10:05:47+00:00 |              38 |
| FORTNITE                                     | BrazilSouth        | Subscription.F2P | 2023-10-22 10:05:45+00:00 |              10 |
| FORTNITE                                     | BrazilSouth        | Subscription.GPU | 2023-10-22 10:05:47+00:00 |              10 |
| FORTNITE                                     | EastUS             | Subscription.F2P | 2023-10-22 10:05:45+00:00 |              10 |
[...]
```

### Configuration

The configuration file ([config.toml](config.toml)) contains all games that should be queried.
The example below shows the configuration for Fortnite with Xbox Cloud ID `FORTNITE`, title `Fortnite` and image (poster) URL and the subscriptions its available in (Free-to-Play and Game Pass Ultimate):

```
[games.FORTNITE]
title = "Fortnite"
image_url = "https://store-images.s-microsoft.com/image/apps.9582.70702278257994163.a9af653c-54d0-4c47-a1f0-bd2f08fe0fd1.3ea1af1a-95a6-4543-be33-94c112ed5dc3"
subscriptions = ["F2P", "GPU"]
```

After adding new games to the configuration, please run `poetry run toml-sort -i config.toml` to keep them sorted.

## Frontend

### Setup

1. `cd site_generator/`
2. Run `poetry install` to install the dependencies
3. Run `python3 -m http.server -d dist/` to start a local HTTP server (useful for development)

### Usage

1. Export environment variables `INFLUXDB_URL`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET` and `INFLUXDB_TOKEN` to connect to InfluxDB
2. Run `poetry run site-generator` to build the static page to `dist/`

https://github.com/n-thumann/xbox-cloud-statistics/assets/46975855/05949add-87a4-4710-b908-41b47aa48b0a

## Measurement data

The measurement data is available in a private InfluxDB instance. Feel free to message me to request access.
