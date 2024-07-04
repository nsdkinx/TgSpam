# -*- coding: utf-8 -*-

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from .partner_proxy import PartnerProxy


PARTNER_PROXIES = [
    PartnerProxy(name='Proxyma', referral_link='https://proxyma.io/ru/register?ref=MWXT1EciwGHJvnao'),
    PartnerProxy(name='Marsproxies', referral_link='https://marsproxies.com/r/CsjZf11021FeXHo'),
    PartnerProxy(name='Proxy-Seller', referral_link='https://proxy-seller.com/?partner=662GXQOQUNO7BE'),
    PartnerProxy(name='Froxy', referral_link='https://froxy.com/?fpr=711nq'),
    PartnerProxy(name='AstroProxy', referral_link='https://astroproxy.com/r/fbda0148ebb5b55c5d556fbb908133f6?lang=ru'),
    PartnerProxy(name='ProxyMonster', referral_link='https://proxymonster.ru/?ref=3628'),
    PartnerProxy(name='Smartproxy', referral_link='https://dashboard.smartproxy.com/register?referral_code=dd46cdb63d7e582c3a032e5b185cb209b24fb428'),
    PartnerProxy(name='HydraProxy', referral_link='https://app.hydraproxy.com/aff=701/'),
    PartnerProxy(name='Proxy6', referral_link='https://proxy6.net/?r=253351'),
    PartnerProxy(name='Proxy-Cheap', referral_link='https://app.proxy-cheap.com/r/HQSeeH'),
    PartnerProxy(name='LTESpace', referral_link='https://ltespace.com/klh,jmhngbfvdcsxcfvgbhntjymkmjnhbgvfcds'),
    PartnerProxy(name='TheSafety', referral_link='https://thesafety.us/r/26762')
]


async def module_main():
    ui.paginate(_("MODULE-partner_proxies"))
    ui.print(_("MODULE-partner_proxies-banner"))
    ui.print_key_and_value(0, _("SETTINGS-back_to_menu"))
    for i, partner_proxy in enumerate(PARTNER_PROXIES, start=1):
        ui.print_key_and_value(i, partner_proxy.name, separator='.')
    print()

    selection_range = Range(0, len(PARTNER_PROXIES))
    selection = im.get_int_input(_("MODULE-partner_proxies-select_proxy"), number_range=selection_range)

    if selection == 0:
        return

    selected_partner_proxy = PARTNER_PROXIES[selection - 1]
    selected_partner_proxy.open_referral_link_in_browser()

    return
