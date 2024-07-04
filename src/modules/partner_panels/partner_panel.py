# -*- coding: utf-8 -*-

import webbrowser
from dataclasses import dataclass


@dataclass
class PartnerPanel:
    name: str
    referral_link: str

    def open_referral_link_in_browser(self):
        webbrowser.open(self.referral_link)
