from dotenv import load_dotenv
import os

load_dotenv()
if 'DJANGO_SETTINGS' in os.environ:
    if os.environ['DJANGO_SETTINGS'] == "dev":
        print("DEVELOPMENT SERVER")
        from .development_settings import *
    else:
        print("PRODUCTION SERVER")
        from .production_settings import *
else:
    print("PRODUCTION SERVER")
    from .production_settings import *
