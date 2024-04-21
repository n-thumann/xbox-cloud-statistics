from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Flag, auto
from typing import Iterator


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

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Game:
    id: str
    title: str
    image_url: str
    subscriptions: Subscription

    def __lt__(self, other) -> bool:
        if not isinstance(other, Game):
            raise TypeError

        return self.id < other.id


@dataclass(frozen=True)
class Measurement:
    server_time: datetime
    wait_time: int


@dataclass(frozen=True)
class RegionResult:
    _subscriptions: dict[Subscription, Measurement] = field(
        default_factory=lambda: defaultdict()
    )

    def __getitem__(self, subscription: Subscription) -> Measurement:
        return self._subscriptions[subscription]

    def __setitem__(self, subscription: Subscription, measurement: Measurement):
        self._subscriptions[subscription] = measurement

    def __iter__(self) -> Iterator[tuple[Subscription, Measurement]]:
        return iter(self._subscriptions.items())


@dataclass(frozen=True)
class GameResult:
    _regions: dict[Region, RegionResult] = field(
        default_factory=lambda: defaultdict(RegionResult)
    )

    def __getitem__(self, region: Region) -> RegionResult:
        return self._regions[region]

    def __iter__(self) -> Iterator[tuple[Region, RegionResult]]:
        return iter(self._regions.items())


@dataclass(frozen=True)
class Results:
    _games: dict[Game, GameResult] = field(
        default_factory=lambda: defaultdict(GameResult)
    )

    def __getitem__(self, game: Game) -> GameResult:
        return self._games[game]

    def __iter__(self) -> Iterator[tuple[Game, GameResult]]:
        return iter(sorted(self._games.items()))
