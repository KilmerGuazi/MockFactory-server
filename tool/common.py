import time
import json
import datetime

TIME_FORMAT_1 = '%Y-%m-%d %H:%M:%S'


def dict2Object(sourceDict, targetClass):
    if isinstance(sourceDict, dict):
        sourceObject = targetClass()
        for key in sourceDict.keys():
            sourceObject.__setattr__(key, sourceDict[key])
        return sourceObject


class TimeTool:

    @staticmethod
    def timestamp2Date(time_format=TIME_FORMAT_1, timestamp=None):
        return time.strftime(time_format, timestamp)

    @staticmethod
    def date2Timestamp(date_str):
        data_sj = time.strptime(date_str, TIME_FORMAT_1)
        ms = int(time.mktime(data_sj)) * 1000
        return ms

    @staticmethod
    def timestamp():
        return int(time.time())

    @staticmethod
    def timestampMS():
        return int(round(time.time() * 1000))

    @staticmethod
    def getTimeOfDayOffset(dayOffset, h, m, s):
        today = datetime.date.today()
        dayOffset = today + datetime.timedelta(days=dayOffset)
        return datetime.datetime.combine(dayOffset, datetime.time(h, m, s))

    @staticmethod
    def getDateOfDayOffset(dayOffset, h, m, s):
        today = datetime.date.today()
        dayOffset = today + datetime.timedelta(days=dayOffset)
        return datetime.datetime.combine(dayOffset, datetime.time(h, m, s))


class DateQueryComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    TimeTool.date2Timestamp('2022-12-15 06:00:00')
