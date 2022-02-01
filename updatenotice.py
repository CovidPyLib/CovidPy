# This file is part of CovidPy v0.1.3
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

import os


oldversion = "0.1.2"
version = "0.1.3"

notice = """
# Copyright (c) 2022, CovidPyLib
# This file is part of CovidPy v{}.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.
"""

for root, dirs, files in os.walk("covidpy"):
    for file in files:
        try:
            f = open(f"covidpy\\{file}", "r+")
            f.seek(0)
            cont = f.read()
            if notice.format(oldversion) in cont:
                cont = cont.replace(notice.format(oldversion), notice.format(version))
                f.seek(0)
                f.write(cont)
                f.truncate()
                f.close()
            else:
                f.close()
        except:
            pass
