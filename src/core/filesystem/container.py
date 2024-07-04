# -*- coding: utf-8 -*-

from dataclasses import dataclass
from .manager import FilesystemManager
from core.localization.interface import _

manager = FilesystemManager()


@dataclass
class FilesContainer:
    """
    Contains the file and folder directory structure.
    The instance of it is created here to create the structure
    if it does not exist implicitly.
    Fields of the instance of this class are Path objects
    of the corresponding file/folder
    """
    base_accounts_folder = manager.create_folder(_("FOLDER-accounts"))

    accounts_folder = manager.create_folder(base_accounts_folder / _("FOLDER-accounts-in_work"))
    accounts_after_check_folder = manager.create_folder(base_accounts_folder / _("FOLDER-accounts_after_check"))

    alive_accounts_folder = manager.create_folder(accounts_after_check_folder / _("FOLDER-accounts-alive"))
    dead_accounts_folder = manager.create_folder(accounts_after_check_folder / _("FOLDER-accounts-dead"))
    temp_sb_accounts_folder = manager.create_folder(accounts_after_check_folder / _("FOLDER-accounts-temporary_spamblock"))
    et_sb_accounts_folder = manager.create_folder(accounts_after_check_folder / _("FOLDER-accounts-eternal_spamblock"))

    audience_bases_folder = manager.create_folder(_("FOLDER-audience_bases"))
    settings_folder = manager.create_folder(_("FOLDER-settings"))
    reports_folder = manager.create_folder(_("FOLDER-reports"))

    proxy_file = manager.create_file(settings_folder / _("FILE-proxy"))
    settings_file = manager.create_file(settings_folder / _("FILE-settings_file"))
    license_key_file = manager.create_file(settings_folder / _("FILE-license_key"))

    spammer_content_folder = manager.create_folder(_("FOLDER-spammer_content_folder"))


files = FilesContainer()
