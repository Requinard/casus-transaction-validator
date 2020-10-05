# Luminis Rotterdam Case

Check `docs` for more info

## How to run/access

### Frontend

The frontend can currently only be run locally.

- cd frontend
- npm install
- npm run start

### Local

you will need a linux and python3.8+ installation for this

- cd app
- pip install poetry
- poetry install
- python main.py

This should print the CLI help command. To run the webapp, use `python main.py run`

### Docker

You will need docker installed locally

- docker-compose up -d

You can now access the app at localhost:8000

### Terraform

This will need AWS credentials to my account. You can change this for yourself by editing

- backend.tf > point this at your own tf bucket
- variables.tf > change dns-zone to your own dns zone

do it like this

- cd terraform
- terraform init
- terraform apply

The command concludes with the publically accessible URL

