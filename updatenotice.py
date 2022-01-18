# This file is part of CovidPy v0.0.5.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

import os

version = "0.0.5"

notice  = f"""
# This file is part of CovidPy v{version}.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.
"""

for root, dirs, files in os.walk('covidpy'):
    for file in files:
        try:
            f = open(f'covidpy\\{file}', 'r+')
            cont = f.read()
            if cont.lstrip().startswith('# This file is part of CovidPy v'):
                cont = notice + cont[len(notice):]
                f.seek(0)
                f.write(cont)
                f.truncate()
                f.close()
            else:
                f.seek(0)
                f.write(notice)
                f.truncate()
                f.close() 
        except:
            pass