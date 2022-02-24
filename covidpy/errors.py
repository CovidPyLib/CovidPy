# Copyright (c) 2022, CovidPyLib
# This file is part of CovidPy v0.1.4
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.


class InvalidDCC(Exception):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


class ImageFormatError(Exception):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


class DCCError(Exception):
    pass
