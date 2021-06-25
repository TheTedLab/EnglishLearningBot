from telegram.ext import MessageFilter


# Фильтры текста
class FilterRecord(MessageFilter):
    def filter(self, message):
        return 'Запись на занятие' in message.text


class FilterInfo(MessageFilter):
    def filter(self, message):
        return 'Подробнее' in message.text


class FilterServices(MessageFilter):
    def filter(self, message):
        return 'Услуги' in message.text


class FilterLevel(MessageFilter):
    def filter(self, message):
        return 'Узнать уровень' in message.text


class FilterYes(MessageFilter):
    def filter(self, message):
        return 'Да' in message.text


class FilterNo(MessageFilter):
    def filter(self, message):
        return 'Нет' in message.text


class FilterDigitOne(MessageFilter):
    def filter(self, message):
        return '1' in message.text


class FilterDigitTwo(MessageFilter):
    def filter(self, message):
        return '2' in message.text


class FilterDigitThree(MessageFilter):
    def filter(self, message):
        return '3' in message.text


class FilterDigitFour(MessageFilter):
    def filter(self, message):
        return '4' in message.text


filter_record = FilterRecord()
filter_info = FilterInfo()
filter_services = FilterServices()
filter_level = FilterLevel()
filter_yes = FilterYes()
filter_no = FilterNo()
filter_digit_one = FilterDigitOne()
filter_digit_two = FilterDigitTwo()
filter_digit_three = FilterDigitThree()
filter_digit_four = FilterDigitFour()
