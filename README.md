# Luminis Rotterdam Case

## How to run/access

### Local

you will need a linux and python3.6+ installation for this

- cd app
- pip install poetry
- poetry install
- python main.py

You can now access this app at localhost:8000

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

## Architecture

For the workings itself, I started with a functional-like onion architecture with BDD modelling. All layers can only communicate upwards

- types -> Contains specific type definitions for this project
- models -> Implements model constraints and models interaction
- operations -> handle side effects from working on models such as reading files and parsing it to a common data structure
- api -> handle validated API requests


