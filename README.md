# CMS website

## Prerequisites

Before running the project, ensure you have the following installed/created:

- `make` – used to manage setup
- `.env` file at the root of the repo with the following lines:
- - GEMINI_API_KEY=key-here
- - POSTGRES_CMS_USER_PASSWORD=any-generated-password-here

## Setup

To start the project, simply run:

```bash
make up
```

If you need to restart the services:   
You can run `make rm-pg-volume` to remove all data from postgres and start the services afterwars again with `make up`.