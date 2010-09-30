import sys; sys.path.insert(0, "../../../mezzanine/")

from mezzanine.project_template.settings import *

from django.utils.translation import ugettext_lazy as _

MEZZANINE_ADMIN_MENU_ORDER = (
    (_("Content"), ("pages.Page", "blog.BlogPost", "blog.Comment",)),
    (_("Shop"), ("shop.Product", "shop.ProductOption", "shop.DiscountCode", 
        "shop.Sale", "shop.Order")),
    (_("Site"), ("auth.User", "auth.Group", "sites.Site", 
        "redirects.Redirect",)),
)

# Main Django settings.
DEBUG = False
DEV_SERVER = False
MANAGERS = ADMINS = ()
TIME_ZONE = ""
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LANGUAGE_CODE = "en"
SITE_ID = 1
USE_I18N = False
SECRET_KEY = "%(SECRET_KEY)s"
INTERNAL_IPS = ("127.0.0.1",)

# Database.
DATABASE_ENGINE = ""
DATABASE_NAME = ""
DATABASE_USER = ""
DATABASE_PASSWORD = ""
DATABASE_HOST = ""
DATABASE_PORT = ""

# Paths.
import os
project_path = os.path.dirname(os.path.abspath(__file__))
project_dir = project_path.split(os.sep)[-1]
MEDIA_URL = "/site_media/"
MEDIA_ROOT = os.path.join(project_path, MEDIA_URL.strip("/"))
TEMPLATE_DIRS = (os.path.join(project_path, "templates"),)
ROOT_URLCONF = "%s.urls" % project_dir
CACHE_MIDDLEWARE_KEY_PREFIX = project_dir

# Apps/
INSTALLED_APPS.insert(0, "cartridge.shop")

TEMPLATE_CONTEXT_PROCESSORS += (
    "cartridge.shop.context_processors.shop_globals",
)

MIDDLEWARE_CLASSES += (
    "cartridge.shop.middleware.SSLRedirect",
)

# Local settings.
try:
    from local_settings import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG

command = ""
if len(sys.argv) >= 2:
    command = sys.argv[1]

if command == "runserver" and PACKAGE_NAME_GRAPPELLI in INSTALLED_APPS:
    # Adopted from django.core.management.commands.runserver - easiest way 
    # so far to actually get all the media for grappelli working with the dev 
    # server is to hard-code the host:port to ``ADMIN_MEDIA_PREFIX``, so 
    # here we check for a custom host:port before doing this.
    addrport = ""
    if len(sys.argv) > 2:
        addrport = sys.argv[2]
    if not addrport:
        addr = ""
        port = "8000"
    else:
        try:
            addr, port = addrport.split(":")
        except ValueError:
            addr, port = "", addrport
    if not addr:
        addr = "127.0.0.1"
    ADMIN_MEDIA_PREFIX = "http://%s:%s%s" % (addr, port, ADMIN_MEDIA_PREFIX)

db_engine = DATABASE_ENGINE.split(".")[-1]
if db_engine == "sqlite3" and "/" not in DATABASE_NAME:
    # If the sqlite DB name doesn't contain a path, assume it's in the 
    # project directory and add the path to it.
    DATABASE_NAME = os.path.join(project_path, DATABASE_NAME)
elif db_engine == "mysql":
    # Required MySQL collation for tests.
    TEST_DATABASE_COLLATION = "utf8_general_ci"
elif db_engine.startswith("postgresql") and not globals().get("TIME_ZONE", 1):
    # Specifying a blank time zone to fall back to the system's time zone
    # will break table creation in Postgres so remove it.
    del TIME_ZONE
