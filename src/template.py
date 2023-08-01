from starlette.datastructures import URL
from starlette.templating import Jinja2Templates

from src.utils.relative_path import from_module_path_to

templates = Jinja2Templates(directory=from_module_path_to("templates"))
templates.env.globals['URL'] = URL