from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Flag, auto
from typing import Iterator


class Model(ABC):
    @abstractmethod
    def to_dict(self) -> dict | list:
        pass


@dataclass(frozen=True)
class Region:
    name: str
    url: str


class Subscription(Flag):
    F2P = auto()
    GPU = auto()

    @classmethod
    def from_string(cls, value: str):
        return cls._member_map_.get(value)


@dataclass(frozen=True)
class Game(Model):
    id: str
    title: str
    image_url: str
    subscriptions: Subscription

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "image_url": self.image_url}

    def __lt__(self, other) -> bool:
        if not isinstance(other, Game):
            raise TypeError

        return self.id < other.id


@dataclass(frozen=True)
class Measurement(Model):
    server_time: datetime
    wait_time: int

    def to_dict(self) -> dict:
        return {int(self.server_time.timestamp()): self.wait_time}


@dataclass(frozen=True)
class RegionResult(Model):
    _subscriptions: dict[Subscription, Measurement] = field(
        default_factory=lambda: defaultdict(Measurement)
    )

    def __getitem__(self, subscription: Subscription) -> Measurement:
        return self._subscriptions[subscription]

    def __iter__(self) -> Iterator[tuple[Subscription, Measurement]]:
        return iter(self._subscriptions.items())

    def to_dict(self) -> list[Subscription] | dict[Subscription, Measurement]:
        return {
            subscription_type: measurement for subscription_type, measurement in self
        }


@dataclass(frozen=True)
class GameResult(Model):
    _regions: dict[Region, RegionResult] = field(
        default_factory=lambda: defaultdict(RegionResult)
    )

    def __getitem__(self, region: Region) -> RegionResult:
        return self._regions[region]

    def __iter__(self) -> Iterator[tuple[Region, RegionResult]]:
        return iter(self._regions.items())

    def to_dict(self) -> dict:
        return {region.name: region_result for region, region_result in self}


@dataclass(frozen=True)
class Results(Model):
    _games: dict[Game, GameResult] = field(
        default_factory=lambda: defaultdict(GameResult)
    )

    def __getitem__(self, game: Game) -> GameResult:
        return self._games[game]

    def __iter__(self) -> Iterator[tuple[Game, GameResult]]:
        return iter(sorted(self._games.items()))

    def to_dict(self) -> dict:
        return {game.id: game_result for game, game_result in self}
