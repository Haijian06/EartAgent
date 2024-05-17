# -*- coding: utf-8 -*-
""" Import all game_scripts modules in the package. """
from .Italy import ItalianTown,TownConfig
from .Wolf import WerewolfGame,GameConfig

__all__ = [
    "ItalianTown",
    "TownConfig",
    "WerewolfGame",
    "GameConfig",
]