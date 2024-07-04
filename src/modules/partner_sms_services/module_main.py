# -*- coding: utf-8 -*-

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from .partner_sms_service import PartnerSmsService


PARTNER_SMS_SERVICES = [
    PartnerSmsService(name='SMS-Activate', referral_link='https://sms-activate.org/?ref=1453422'),
    PartnerSmsService(name='SMS-MAN', referral_link='https://sms-man.ru/?ref=uTem8vVcQdCj'),
    PartnerSmsService(name='VAK-SMS', referral_link='https://vak-sms.com/10378590-fbcb-44fc-b2ee-6bb2c3d7a026'),
    PartnerSmsService(name='Give-SMS', referral_link='https://give-sms.com/?ref=99032'),
    PartnerSmsService(name='365SMS', referral_link='https://365sms.org/?ref=170962'),
    PartnerSmsService(name='GrizzlySMS', referral_link='https://grizzlysms.com/registration?r=4390'),
    PartnerSmsService(name='OnlineSim', referral_link='https://onlinesim.io/?ref=2060536'),
    PartnerSmsService(name='sms-activation-service', referral_link='https://sms-activation-service.com/ru/?ref=1707876206'),
    PartnerSmsService(name='SMSCodes', referral_link='https://dashboard.smscodes.io/account/register?ref=StGroupUkraineAdm@gmail.com')
]


async def module_main():
    ui.paginate(_("MODULE-partner_sms_services"))
    ui.print(_("MODULE-partner_sms_services-banner"))
    ui.print_key_and_value(0, _("SETTINGS-back_to_menu"))
    for i, partner_proxy in enumerate(PARTNER_SMS_SERVICES, start=1):
        ui.print_key_and_value(i, partner_proxy.name, separator='.')
    print()

    selection_range = Range(0, len(PARTNER_SMS_SERVICES))
    selection = im.get_int_input(_("MODULE-partner_proxies-select_proxy"), number_range=selection_range)

    if selection == 0:
        return

    selected_partner_proxy = PARTNER_SMS_SERVICES[selection - 1]
    selected_partner_proxy.open_referral_link_in_browser()

    return
