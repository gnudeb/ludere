from dataclasses import dataclass

from ludere.core import Ludere


l = Ludere()
Register = l.register


@Register
@dataclass
class Config:
    x: int = 5

    def __post_init__(self):
        print("Config got instantiated!")


@Register
@dataclass
class App:
    config: Config

    def __post_init__(self):
        print(self.config.x)


if __name__ == '__main__':
    l.run()
