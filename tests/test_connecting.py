import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from evdsts.base.connecting import Connector

#! to be impelemented as old tests become too complicated

connector = Connector()

# print(connector.get_main_categories())
# print(connector.get_sub_categories(25))
# print(connector.get_groups("bie_altingr", raw=True))
print(connector.get_series("TP.ALTINGR.ZCEYREK", start_date="01.01.2025"))
