import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Interval, Polyline

NAME = 'curve'

class Schema(SpeckleObject):
    type: Optional[str] = "Curve"
    name: Optional[str] = "SpecklePolycurve"
    segments: List[dict] = []
    domain: Interval.Schema = Interval.Schema()
    degree: int = 0
    rational: bool = True
    periodic: bool = True
    points: List[float] = []
    weights: List[float] = []
    knots: List[float] = []
    displayValue: Optional[Polyline.Schema]
