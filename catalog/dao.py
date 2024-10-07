from core.dao import BaseDAO
from catalog.models import Ruler


class RulerDAO(BaseDAO):
    model = Ruler
