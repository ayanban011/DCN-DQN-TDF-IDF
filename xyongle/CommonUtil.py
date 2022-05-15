__author__ = 'xyongle'

import datetime
import time

class CommonString:

    @staticmethod
    def splitStr(value,splitChar=','):
        # return value.split()
        return value.split(splitChar,1)


class CommonParser:
    @staticmethod
    def getStrFromInt(value):
        return str(value)

    @staticmethod
    def getIntFromStr(value):
        return int(value)

    @staticmethod
    def getStrFrormLong(value):
        return str(value)

    @staticmethod
    def getLongFromStr(value):
        return long(value)

    @staticmethod
    def getStrFromDate(date=datetime.date.today(),format='%Y-%m-%d'):
        # date = datetime.date.today()
        return date.strftime(format)
        # return time.strftime('%Y-%m-%d',time.localtime(time_time))
    @staticmethod
    def getDateFromStr(str,format):
        #'%Y-%m-%d'
        return datetime.datetime.strptime(str,format)




if __name__ == '__main__':
    print CommonParser.getIntFromStr('12342312')