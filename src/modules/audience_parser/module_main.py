# -*- coding: utf-8 -*-

import logging
import itertools
import random
import traceback

from modules._base.parameters.parameters_verifier import ParametersVerifier
from modules._base.parameters.parameters_verifier import (
    ParametersVerifyingResult,
    NeedToEditParameters,
    NeedToExitModule
)

from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from core.filesystem.container import files
from core.settings.container import settings
from core.taskpool import TaskPoolExecutor

from .parameters import AudienceParserParameters
from .audience_saver import AudienceSaver
from .simple_parsing_worker import SimpleParsingWorker
from .deep_parser import DeepParser

logger = logging.getLogger(__name__)


async def module_main():
    while True:
        ui.paginate(_('MODULE-audience_parser'))
        parameters = AudienceParserParameters.ask_user()
        verifying_result = await ParametersVerifier.ask_to_verify_parameters(parameters)
        if verifying_result == NeedToExitModule:  # noqa
            return
        elif verifying_result == NeedToEditParameters:
            continue
        else:
            break

    file = files.audience_bases_folder / f'{parameters.audience_base.value}.txt'
    audience_saver = AudienceSaver(file)
    # accounts = itertools.cycle(verifying_result.accounts)
    accounts = verifying_result.accounts
    spinner = 'point'
    status = ui.console.status(_("MODULE-audience_parsing-now_parsing_status"), spinner=spinner)
    status.start()

    if not parameters.deep_parsing.value:
        # Simple parsing
        accounts = itertools.cycle(accounts)
        workers = []
        for chat in parameters.chats.value:
            account = next(accounts)
            workers.append(SimpleParsingWorker(chat, account, parameters, audience_saver))
    else:
        # Deep parsing
        deep_parser = DeepParser(accounts, parameters.chats.value, parameters, audience_saver)
        try:
            await deep_parser.start_working()
        except BaseException as e:
            logger.exception('Error in deep parser.')
            ui.log(_('MODULE-audience_parser-error').format(f'{type(e).__name__}: {str(e)}'))

        status.stop()

        if not audience_saver.all_participants:
            try:
                audience_saver.file.unlink()
            except:
                pass
        else:
            ui.log(
                _("MODULE-audience_parser-saved_audience").format(len(audience_saver.all_participants), file)
            )
        ui.log('Выполнение задачи завершено!')
        ui.console.input('\n' + _('MODULE-base-press_enter_to_exit'))

        return

    task_pool = TaskPoolExecutor(
        max_size=settings.concurrency_limit, collect_results=True
    )
    async with task_pool:
        for worker in workers:
            await task_pool.submit(worker.start_working)

    status.stop()

    if not audience_saver.all_participants:
        try:
            audience_saver.file.unlink()
        except:
            pass
    else:
        ui.log(
            _("MODULE-audience_parser-saved_audience").format(len(audience_saver.all_participants), file)
        )
    ui.log('Выполнение задачи завершено!')
    ui.console.input('\n' + _('MODULE-base-press_enter_to_exit'))
