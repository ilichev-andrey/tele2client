from typing import Dict

from tele2client import containers


def cost2dict(cost: containers.LotCost) -> Dict:
    return cost._asdict()


def megabytes2gigabytes(megabytes):
    return megabytes / 1024
