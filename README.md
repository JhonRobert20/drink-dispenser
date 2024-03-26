# Drink dispenser

This projects want to create a drink dispenser backend.
This project is implemented with DDD (Domain Driven Design) and TDD (Test Driven Development) methodologies
and Hexagonal Architecture.

## Requirements

To add more products to the dispenser
To consult a product stock by an employee
To consult the machine status by an employee
To dispense a product to an employee

## Actual status of the project
Is not possible to consult the machine status by an employee
Is not possible to dispense a product to an employee

## Actual things done

- Entities
- Value Objects
- Repositories
- Models for the persistence
- Logic for the dispenser
- Can consult the stock of a product by an employee
- Can add more products to the dispenser


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

- The project is not finished
- The project was soo interesting to do
- Was my very first time implementing Hexagonal Architecture and DDD, so I learned a lot
- Please any feedback is welcome

## Images of the project
Consult stock of a product
![consult_stock](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/consult_stock.png)

Add more products to the dispenser and other logs
![add_products](https://github.com/JhonRobert20/drink-dispenser/blob/main/docs/general_logs.png)
