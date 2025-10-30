#!/usr/bin/env python

import argparse
import asyncio
import logging
import sys

from src.app import main as run_bot


def _parse_args() -> argparse.Namespace:
    """
    Функция для обработки аргументов командной строки.
    """

    parser = argparse.ArgumentParser(
        description="Запуск Telegram-бота и управление уровнями логирования.",
    )
    parser.add_argument(
        "-v",
        dest="log_level",
        default="INFO",
        choices=[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ],
        help="Установить уровень логирования",
    )
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Немедленно запустить бота (start_polling).",
    )
    return parser.parse_args()


def _configure_logging(
    level_name: str,
) -> None:
    level = getattr(
        logging,
        level_name.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def _main(args: argparse.Namespace) -> int:
    """
    Основная функция запуска. Управляет логированием и действиями по флагам.
    """

    _configure_logging(args.log_level)

    if args.run_now:
        asyncio.run(run_bot())
        return 0

    print("Нечего выполнять. Укажите флаг --run-now для запуска бота.")
    return 0


if __name__ == "__main__":
    _args = _parse_args()
    sys.exit(
        _main(_args)
    )
