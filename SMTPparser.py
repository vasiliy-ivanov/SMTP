import re, fileinput, sys, argparse, os
from datetime import datetime

class Date:

    @classmethod
    def __init__(self, MakeStarDate, MakeEndDate):
        #example date'2015 Mar 27', '%Y %b %d'
        self.start_date = datetime.strptime(*MakeStarDate)
        #print self.start_date
        #example date'2015 Mar 27', '%Y %b %d'
        self.end_date = datetime.strptime(*MakeEndDate)
    def all(self):
        return self.start_date, self.end_date

class MakeStarDate:

    def make_Start_Date(self, start_date):
        self.start_date = start_date
        return self.start_date, '%Y %b %d'

class MakeEndDate:
    def make_End_Date(self, end_date):
        self.end_date = end_date
        return self.end_date, '%Y %b %d'

class SMTPLogParserStrategy(object):

    def __init__(self, date, mail=None):
        self.date = date
        self.mail = mail

    def find_Mail(self, line):
        if self.mail in line:
            return True

    def compareTimeInLine(self, currentDateInLine):
        if self.date.start_date >= currentDateInLine >= self.date.end_date:
            return True

    def getID(self, line):
        pattern = '([ABCDEF0-9]{11})'
        ID = re.search(pattern, line)
        if ID: return ID.group(1)

    def getMail(self, line):
        pattern = '[ABCDEF0-9]{11}.*sasl_username=(.*)'
        mail = re.search(pattern, line)
        if mail: return mail.group(1)

    def getMailFrom(self, line):
        pattern = ('(from=<.*>)')
        mail_from = re.search(pattern, line)
        if mail_from: return mail_from.group(1)

    def getMailTo(self, line):
        pattern = ('(to=<.*>)')
        mail_to = re.search(pattern, line)
        if mail_to: return  mail_to.group(1)

    def getMailStatus(self, line):
        pattern = ('status=(\S*)')
        status_mail = re.search(pattern, line)
        if status_mail: return status_mail.group(1)

    def showStatMail(self):
        return self.numberOfLetters

class SMTPLogParser(object):

    def __init__(self, parse_strategy,mail=None):
        self.parse_strategy = parse_strategy
        # List for the result
        self.listOfStrings = []
        # Dictionary for prepear the result
        self.dicOfStrings = {}
        # Counter sent letters
        self.numberOfLetters = 0
        # Dictionary for the result
        self.result = {}

    def add_line_in_list(self, line):
        if self.parse_strategy.getID(line):
            if not self.parse_strategy.getID(line) in self.listOfStrings:
                self.listOfStrings.append(self.parse_strategy.getID(line))

    def add_line_in_dic(self, line):
        if self.parse_strategy.getID(line):
            if self.parse_strategy.getID(line) in self.dicOfStrings:
               self.dicOfStrings.setdefault(self.parse_strategy.getID(line), []).append(line)
            else:
               self.dicOfStrings.setdefault(self.parse_strategy.getID(line), []).append(line)

    def parse_the_complete_log(self, dic):
        for key, value in dic.items():
            for string in value:
                if parse.parse_strategy.getMailStatus(string):
                    if not key in self.result:
                        list = {'Status': parse.parse_strategy.getMailStatus(string)}
                        self.result[key] = list
                    else:
                        value_of_dictionary = self.result[key]
                        list = {'Status': parse.parse_strategy.getMailStatus(string)}
                        value_of_dictionary.update(list)
                        self.result[key] = value_of_dictionary

                if parse.parse_strategy.getMail(string):
                    if not key in self.result:
                        list = {'mail': parse.parse_strategy.getMail(string)}
                        self.result[key] = list
                    else:
                        value_of_dictionary = self.result[key]
                        list = {'mail': parse.parse_strategy.getMail(string)}
                        value_of_dictionary.update(list)
                        self.result[key] = value_of_dictionary


class ScanLogsInFolder:
    def scan(self):
        print 'scan file is: ', os.getcwd()
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file):
                print 'scan file', file

class ParametersArgumentParser(object):
    def __init__(self):
        #example date'2015 Mar 27', '%Y %b %d'
        parse = argparse.ArgumentParser()
        parse.add_argument("-start_date", type=str, dest='start')
        parse.add_argument("-end_date", type=str, dest='end')
        parse.add_argument("-user_mail", type=str, dest='mail')
        parse.add_argument("-scan_this_file", type=str, dest='file')
        parse.add_argument("-scan_all_files", type=str, dest='scan')
        self.args = parse.parse_args()


    def return_option(self):
        return self.args

class ActionsWithParametersArgumentParser(object):
    def __init__(self, ParametersArgumentParser, MakeStarDate, MakeEndDate):
        self.ParametersArgumentParser = ParametersArgumentParser
        self.MakeStarDate = MakeStarDate
        self.MakeEndDate = MakeEndDate

    def string_parameter_return(self):
        if not self.ParametersArgumentParser.return_option().start:
            start_date = self.MakeStarDate.make_Start_Date('2015 Jul 23')
        else:
            start_date = self.MakeStartDate((self.ParametersArgumentParser.return_option().start).replace('-', ' '))

        if not self.ParametersArgumentParser.return_option().end:
            end_date = self.MakeEndDate.make_End_Date('2015 Jul 23')
        else:
            end_date = self.EndDate((self.ParametersArgumentParser.return_option().end).replace('-', ' '))

        return start_date, end_date

MakeEndDate = MakeEndDate()
MakeStarDate = MakeStarDate()
MakeParametersArgumentParser = ParametersArgumentParser()
MakeActionsWithParametersArgumentParser = ActionsWithParametersArgumentParser(MakeParametersArgumentParser,
                                                                              MakeStarDate, MakeEndDate)


file_names = [MakeParametersArgumentParser.return_option().file if MakeParametersArgumentParser.return_option().file
              else 'maillog']

#file_names = [sys.argv[1] if len(sys.argv) > 1 else 'maillog']


start_date, end_date = MakeActionsWithParametersArgumentParser.string_parameter_return()

print start_date, end_date
make_parse = SMTPLogParserStrategy(Date(start_date, end_date))
parse = SMTPLogParser(make_parse)
for line in fileinput.input(file_names):
    currentDateInLine = datetime.strptime(line[0:11],'%Y %b %d')
    if make_parse.compareTimeInLine(currentDateInLine):
        parse.add_line_in_dic(line)

if __name__ == '__main__':

   parse.parse_the_complete_log(parse.dicOfStrings)
   for key in parse.result.items():
       print key

