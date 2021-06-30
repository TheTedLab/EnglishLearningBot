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


class FilterNineHour(MessageFilter):
    def filter(self, message):
        if message.text == '9:00':
            return '9:00' in message.text


class FilterTenHour(MessageFilter):
    def filter(self, message):
        if message.text == '10:00':
            return '10:00' in message.text


class FilterElevenHour(MessageFilter):
    def filter(self, message):
        if message.text == '11:00':
            return '11:00' in message.text


class FilterTwelveHour(MessageFilter):
    def filter(self, message):
        if message.text == '12:00':
            return '12:00' in message.text


class FilterThirteenHour(MessageFilter):
    def filter(self, message):
        if message.text == '13:00':
            return '13:00' in message.text


class FilterFourteenHour(MessageFilter):
    def filter(self, message):
        if message.text == '14:00':
            return '14:00' in message.text


class FilterFifteenHour(MessageFilter):
    def filter(self, message):
        if message.text == '15:00':
            return '15:00' in message.text


class FilterSixteenHour(MessageFilter):
    def filter(self, message):
        if message.text == '16:00':
            return '16:00' in message.text


class FilterSeventeenHour(MessageFilter):
    def filter(self, message):
        if message.text == '17:00':
            return '17:00' in message.text


class FilterEighteenHour(MessageFilter):
    def filter(self, message):
        if message.text == '18:00':
            return '18:00' in message.text


# Фильтры главного меню
filter_record = FilterRecord()
filter_info = FilterInfo()
filter_services = FilterServices()
filter_level = FilterLevel()

# Фильтры Да/Нет
filter_yes = FilterYes()
filter_no = FilterNo()

# Фильтры Услуг
filter_digit_one = FilterDigitOne()
filter_digit_two = FilterDigitTwo()
filter_digit_three = FilterDigitThree()
filter_digit_four = FilterDigitFour()

# Фильтры времени записи
filter_nine_hour = FilterNineHour()
filter_ten_hour = FilterTenHour()
filter_eleven_hour = FilterElevenHour()
filter_twelve_hour = FilterTwelveHour()
filter_thirteen_hour = FilterThirteenHour()
filter_fourteen_hour = FilterFourteenHour()
filter_fifteen_hour = FilterFifteenHour()
filter_sixteen_hour = FilterSixteenHour()
filter_seventeen_hour = FilterSeventeenHour()
filter_eighteen_hour = FilterEighteenHour()
