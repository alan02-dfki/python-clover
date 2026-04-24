import logging

from ..decorator import clover

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@clover
def module_function(arg0, overridden_arg, kwarg0="kw0", overridden_kwarg="okw0"):
    log.info(f"module_function received: arg0={arg0}")
    log.info(f"module_function received: overridden_arg={overridden_arg}")
    log.info(f"module_function received: kwarg0={kwarg0}")
    log.info(f"module_function received: overridden_kwarg={overridden_kwarg}")


@clover(alias="mofu")
def other_module_function(arg):
    log.info(f"other_module_function received: arg={arg}")


class Dog:
    @clover
    def __init__(self, name="Poochi"):
        self.name = name

    @clover(alias="sniff")
    def a_long_function_name_describing_a_sniffing_action(self, obj):
        log.info(f"{self.name} is sniffing the {obj}")

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
    other_module_function()
    dog = Dog()
    dog.bark()
    Dog.dig()
    Dog.wag()
