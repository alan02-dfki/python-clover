import logging

from decorator import clover

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@clover
def module_function(arg0, overridden_arg, kwarg0="kw0", overridden_kwarg="okw0"):
    log.info(f"module_function received: arg0={arg0}")
    log.info(f"module_function received: overridden_arg={overridden_arg}")
    log.info(f"module_function received: kwarg0={kwarg0}")
    log.info(f"module_function received: overridden_kwarg={overridden_kwarg}")


class Dog:
    @clover
    def __init__(self, name="Poochi"):
        self.name = name

    @clover
    def bark(self, bark):
        log.info(f"{self.name} is barking: {bark}")

    @classmethod
    @clover
    def dig(cls, burrow):
        log.info(f"Dog is digging: {burrow}")

    @staticmethod
    @clover
    def wag(body_part):
        log.info(f"Animals with {body_part}s can wag their {body_part}.")


if __name__ == "__main__":
    module_function("arg0-from-code")
    dog = Dog()
    dog.bark()
    Dog.dig()
    Dog.wag()
