# xbox-cloud-statistics

A backend and frontend application to gather and visualize the current wait times on Xbox Cloud Gaming.

## Backend

For setup and usage please refer to [backend/README](./backend/README.md).

```
➜  backend git:(main) poetry run xbox-cloud-statistics
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

## Frontend

For setup and usage please refer to [frontend/README](./frontend/README.md).

https://github.com/n-thumann/xbox-cloud-statistics/assets/46975855/05949add-87a4-4710-b908-41b47aa48b0a

## Measurement data

The measurement data is available as JSON on the [`results`](https://github.com/n-thumann/xbox-cloud-statistics/tree/results) branch.
