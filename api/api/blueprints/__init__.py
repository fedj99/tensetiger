from . import api, errors, frontend, misc

# Import all submodules and re-export them so that the following works:
# import blueprints
#
# blueprints.api # Works, as the api module has been imported and initialized here
#
# Otherwise, calling blueprints.api will not import the module properly
__all__ = ["api", "misc", "frontend", "errors"]
