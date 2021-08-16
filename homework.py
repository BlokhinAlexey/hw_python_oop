"""
Общий класс калькуляторов Calculator, отдельные калькуляторы для расчета
калорий и денег, CaloriesCalculator и CashCalculator, класс Record для
создания записей.
"""

import datetime as dt


class Calculator:
    """
    Предоставляет классам CashCalculator и CaloriesCalculator
    общие методы для хранения и обработки записей.
    """

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """
        Добавляет новую запись в список records.
        """
        self.records.append(record)

    def get_today_stats(self):
        """
        Возвращает количество денег/калорий в записях с
        сегодняшней датой.
        """
        today = dt.date.today()
        today_amount = sum([records.amount for records in self.records
                            if records.date == today])
        return today_amount

    def get_week_stats(self):
        """
        Возвращает количество денег/калорий в записях за
        предыдущие семь дней.
        """
        today = dt.date.today()
        week_length = today - dt.timedelta(days=7)
        week_amount = sum([records.amount for records in self.records
                          if today >= records.date >= week_length])
        return week_amount

    def get_balance(self, amount):
        """
        Возвращает разницу между лимитом и количеством
        денег/калорий.
        """
        balance = self.limit - amount
        return balance


class Record:
    """
    Принимает данные записи, устанавливает значение даты по-умолчанию
    и переводит дату в необходимый формат.
    """
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        else:
            self.date = dt.date.today()


class CaloriesCalculator(Calculator):
    """
    Производит операции с записями о еде.
    """
    def get_calories_remained(self):
        """
        Рассчитывает остаток по калориям  за сегодня.
        """
        calories = self.get_today_stats()
        balance = self.get_balance(calories)
        if balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
            return 'Хватит есть!'

    def get_week_calories_remained(self):
        """
        Рассчитывает остаток по калориям  за семь дней.
        """
        calories = self.get_week_stats()
        balance = self.get_balance(calories)
        if balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """
    Хранит информацию о курсах валют и
    производит операции с записями о деньгах.
    """
    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        """
        Рассчитывает остаток или долг по деньгам за сегодня
        и конвертирует их в необходимую валюту.
        """
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }
        sign, rate = currencies[currency]
        cash = self.get_today_stats()
        balance = self.get_balance(cash)
        converted = round((abs(balance) / rate), 2)
        if balance > 0:
            return f'На сегодня осталось {converted} {sign}'
        elif balance == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {converted} {sign}'

    def get_week_cash_remained(self, currency):
        """
        Рассчитывает остаток или долг по деньгам за семь дней
        и конвертирует их в необходимую валюту.
        """
        sign, rate = self.currencies[currency]
        cash = self.get_week_stats()
        balance = self.get_balance(cash)
        converted = round((abs(balance) / rate), 2)
        if balance > 0:
            return f'На этой неделе осталось {converted} {sign}'
        elif balance == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {converted} {sign}'
