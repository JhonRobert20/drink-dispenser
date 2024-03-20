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
Is not possible to add more products to the dispenser
Is not possible to consult a product stock by an employee
Is not possible to consult the machine status by an employee
Is not possible to dispense a product to an employee

## Actual things done

- Entities
- Value Objects
- Repositories
- Models for the persistence
- Logic for the dispenser

## Next steps

- Add logic to send async events to an LCD screen
- Implement the connection between the application and infrastructure
- Handle all the events that the application can receive
- Add logs to the application

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
