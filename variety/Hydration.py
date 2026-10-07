# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (c) 2026, Federico Bagattoni <federicobagattoni61@gmail.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import os
import json
import datetime


class HydrationManager:
    def __init__(self, options):
        self.options = options
        self.water_file = os.path.expanduser("~/.config/variety/hydration.json")
        self._water_amount = self.load_data()

    @property
    def water_amount(self):
        return self._water_amount

    @property
    def daily_goal(self):
        return float(self.options.water_daily_goal)

    @property
    def log_amount(self):
        return float(self.options.water_log_amount)

    @property
    def interval(self):
        return int(self.options.water_reminder_interval)

    def load_data(self):
        try:
            if os.path.exists(self.water_file):
                with open(self.water_file, "r") as f:
                    data = json.load(f)
                    if data.get("date") == datetime.date.today().isoformat():
                        return data.get("amount", 0.0)
        except Exception as e:
            print(f"Failed to load water data: {e}")
        return 0.0

    def save_data(self):
        data = {"date": datetime.date.today().isoformat(), "amount": self._water_amount}
        with open(self.water_file, "w") as f:
            json.dump(data, f)

    def log_drink(self):
        self._water_amount += self.log_amount
        self._water_amount = round(self._water_amount, 2)
        self.save_data()
