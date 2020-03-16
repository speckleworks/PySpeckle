from speckle.base.resource import ResourceBaseSchema
from pathlib import Path
import sys
import inspect
import pkgutil
from importlib import import_module


for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):

    imported_module = import_module('.' + name, package=__name__)
    
    if hasattr(imported_module, 'Schema'):
        setattr(sys.modules[__name__], name, imported_module.Schema)