from speckle.base.resource import ResourceBaseSchema, SCHEMAS
from speckle.resources.objects import SpeckleObject

from pathlib import Path
import sys
import inspect
import pkgutil
from importlib import import_module

setattr(sys.modules[__name__], "SpeckleObject", SpeckleObject)

for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):

    imported_module = import_module('.' + name, package=__name__)
    
    if hasattr(imported_module, 'Schema'):
        SCHEMAS[name] = imported_module.Schema
        setattr(sys.modules[__name__], name, imported_module.Schema)