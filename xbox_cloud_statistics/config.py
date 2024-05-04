import operator
import os
from functools import reduce

from common.config import Config
from common.models import Game, Subscription


class BackendConfig(Config):
    def __init__(self):
        super().__init__()

        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")

        self.f2p_token = os.environ.get("F2P_TOKEN")
        self.gpu_token = os.environ.get("GPU_TOKEN")

        self._validate()

    def _validate(self):
        super()._validate()

        if not self.client_id or not self.client_secret:
            raise Exception(
                "Environment variables CLIENT_ID and CLIENT_SECRET are required"
            )

        all_subscriptions = reduce(
            operator.or_, [game.subscriptions for game in self.games]
        )

        if (Subscription.F2P in all_subscriptions) ^ bool(self.f2p_token):
            raise Exception(
                "F2P games and environment variable "
                "F2P_TOKEN need to be specified mutally"
            )

        if (Subscription.GPU in all_subscriptions) ^ bool(self.gpu_token):
            raise Exception(
                "GPU games and environment variable "
                "GPU_TOKEN need to be specified mutally"
            )

    @property
    def f2p_games(self) -> list[Game]:
        return [game for game in self.games if Subscription.F2P in game.subscriptions]

    @property
    def gpu_games(self) -> list[Game]:
        return [game for game in self.games if Subscription.GPU in game.subscriptions]
