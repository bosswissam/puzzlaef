"""
Backwards-compatible URLconf for existing django-registration
installs; this allows the standard ``include('registration.urls')`` to
continue working, but that usage is deprecated and will be removed for
django-registration 1.0. For new installs, use
``include('registration.backends.default.urls')``.

"""

import warnings

warnings.warn("include('puzzlaef.registration.urls') is deprecated; use include('puzzlaef.registration.backends.default.urls') instead.",
              PendingDeprecationWarning)

from puzzlaef.registration.backends.default.urls import *
