from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def isValid(self, value) -> bool:
        ...


class ValidatorAggregate(Validator):
    def __init__(self, validators=None):
        if validators is None:
            validators = []

        self.validators = set()
        for validator in validators:
            self.validators.add(validator)

    def add_validator(self, validator: Validator):
        self.validators.add(validator)

    def remove_validator(self, validator: Validator):
        self.validators.remove(validator)

    def isValid(self, value):
        for validator in self.validators:
            if not validator.isValid(value):
                return False
        return True


class ValidatorInt(Validator):
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def isValid(self, value: int) -> bool:
        if type(value) != int:
            return False

        return self.min_value <= value <= self.max_value


class ValidatorFloat(Validator):
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def isValid(self, value: int) -> bool:
        if type(value) != float:
            return False

        return self.min_value <= value <= self.max_value
