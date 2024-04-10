# Drink dispenser

This projects want to create a drink dispenser backend.
This project is implemented with DDD (Domain Driven Design) and TDD (Test Driven Development) methodologies
and Hexagonal Architecture.

## Requirements

To add more products to the dispenser
To consult a product stock by an employee
To consult the machine status by an employee
To dispense a product to an employee

## Actual things done

- Entities
- Value Objects
- Repositories
- Models for the persistence
- Logic for the dispenser
- Can consult the stock of a product by an employee
- Can add more products to the dispenser
- Can consult the logs of the dispenser
- Can consult the machine status by an employee
- Can dispense a product to an employee


## How to run the tests
### First up the infrastructure

```bash
$ docker-compose up
```

### Run the tests
```bash
$ docker exec python_container pytest
```

## Considerations

- The project is finished
- The project was soo interesting to do
- Was my very first time implementing Hexagonal Architecture and DDD, so I learned a lot
- Please any feedback is welcome
- The project is not perfect, but I tried to do my best

## Future work
- Implement a frontend to interact with the dispenser
- Add better logs
- Add more tests

## Images of the project
Consult stock of a product
![consult_stock](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/consult_stock.png)

Add more products to the dispenser and other logs
![add_products](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/general_logs.png)

Consult machine status
![machine_status](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/consult_status.png)

Add coin to the dispenser
![add_coin](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/add_coin.png)


## Newcomers
### Setup

Install the git hooks with:

```bash
pre-commit install
cp ./config/git-hook-commit-msg .git/hooks/commit-msg
docker-compose up -d
```
