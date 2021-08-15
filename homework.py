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

    def get_today_stats(self) -> float:
        """
        Возвращает количество денег/калорий в записях с
        сегодняшней датой.
        """
        amount = 0
        for records in self.records:
            if records.date == records.TODAY.date():
                amount += records.amount
            else:
                pass
        return amount

    def get_week_stats(self) -> float:
        """
        Возвращает количество денег/калорий в записях за
        предыдущие семь дней.
        """
        week_amount = 0
        week_length = dt.datetime.now().date() - dt.timedelta(days=7)
        for records in self.records:
            if (records.date <= dt.datetime.now().date()
                    and records.date >= week_length):
                week_amount += records.amount
        return week_amount


class Record:
    """
    Принимает данные записи, устанавливает значение даты по-умолчанию
    и переводит дату в необходимый формат.
    """

    DATE_FORMAT = '%d.%m.%Y'
    TODAY = dt.datetime.now()

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        else:
            self.date = self.TODAY.date()


class CaloriesCalculator(Calculator):
    """
    Производит операции с записями о еде.
    """

    def get_calories_remained(self):
        """
        Рассчитывает остаток по калориям  за сегодня.
        """
        calories = self.get_today_stats()
        balance = self.limit - calories
        if calories <= self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
            return 'Хватит есть!'

    def get_week_calories_remained(self):
        """
        Рассчитывает остаток по калориям  за семь дней.
        """
        calories = self.get_week_stats()
        balance = self.limit - calories
        if calories <= self.limit:
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
        'usd': ('USD', 'USD_RATE'),
        'eur': ('Euro', 'EURO_RATE'),
        'rub': ('руб', 'RUB_RATE')
        }
        sign, rate = self.currencies[currency]
        rates = getattr(self, rate)
        cash = self.get_today_stats()
        balance = self.limit - cash
        converted = round((abs(balance) / rates), 2)
        if cash < self.limit:
            return f'На сегодня осталось {converted} {sign}'
        elif cash == self.limit:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {converted} {sign}'

    def get_week_cash_remained(self, currency):
        """
        Рассчитывает остаток или долг по деньгам за семь дней
        и конвертирует их в необходимую валюту.
        """
        sign, rate = self.currencies[currency]
        rate = getattr(self, rate)
        cash = self.get_week_stats()
        balance = self.limit - cash
        converted = round((abs(balance) / rate), 2)
        if cash < self.limit:
            return f'На этой неделе осталось {converted} {sign}'
        elif cash == self.limit:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {converted} {sign}'
