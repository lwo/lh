#!/usr/bin/env python
#
# lineair.py --file [csv]
#
# CSV opbouw: datum, extra_aflossing, tarief, correctie

import calendar
import csv
import datetime
import decimal
import getopt
import sys


def calculate(f):
    afgelost = 0
    aflossing = 0
    jaar = 0
    looptijd = 0
    maand = 0
    schuld = 0
    tarief = 0

    print(
    'extra_aflossing,jaar,datum,maand,maanden_over,tarief,rente,aflossing,afgelost,schuld_begin_maand,schuld,lasten')

    with open(f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        for items in reader:
            _datum = get_date(items[0])
            _extra_aflossing = items[1]
            _tarief = get_decimal(items[2])
            _schuld = get_decimal(items[3])
            _looptijd = get_int(items[4])
            if _looptijd:
                looptijd = _looptijd
            if _schuld:
                schuld = get_decimal(_schuld)
                aflossing = get_decimal(schuld / looptijd)
            datum = _datum
            maand += 1
            maanden_over = 1 + looptijd - maand
            if maand % 12 == 1:
                jaar += 1
                _jaar = str(jaar)
            else:
                _jaar = ''

            if _tarief:
                tarief = _tarief

            schuld_begin_maand = schuld
            afgelost += aflossing
            schuld -= aflossing
            rente = get_decimal((schuld_begin_maand / 1200) * tarief)
            lasten = get_decimal(rente + aflossing)
            if _extra_aflossing == '-1':
                _extra_aflossing = int(schuld)
            if schuld < 0:
                schuld = 0
            if rente < 0:
                rente = 0
            if lasten < 0:
                lasten = 0
            if aflossing < 0:
                aflossing = 0

            print(
                '{},{},{:%d-%m-%Y},{},{},{}%,{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(_extra_aflossing,
                                                                                               _jaar, datum, maand,
                                                                                               maanden_over,
                                                                                               tarief,
                                                                                               rente,
                                                                                               aflossing, afgelost,
                                                                                               schuld_begin_maand,
                                                                                               schuld, lasten))

            if schuld < 1:
                sys.exit(0)

            if _extra_aflossing:
                extra_aflossing = get_decimal(_extra_aflossing)
                afgelost += extra_aflossing
                monthrange = calendar.monthrange(datum.year, datum.month)[1]
                voor = get_decimal(((float(datum.day)) / monthrange) * rente)
                rente_correctie = get_decimal(((schuld_begin_maand - extra_aflossing) / 1200) * tarief)
                na = get_decimal(((float(monthrange - datum.day)) / monthrange) * rente_correctie)
                correctie = rente - voor - na
                schuld -= (get_decimal(extra_aflossing + correctie))
                aflossing = get_decimal(schuld / (maanden_over - 1))

def get_int(s):
    if s:
        return int(s)
    else:
        return 0


def get_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def get_decimal(s):
    if s:
        return round(decimal.Decimal(s), 2)
    else:
        return decimal.Decimal(0)


def add_months(start_date, months=1):
    month = start_date.month - 1 + months
    year = int(start_date.year + month / 12)
    month = month % 12 + 1
    day = min(start_date.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)


def usage():
    print('Usage: lineair.py --file [file to csv]')


def main(argv):
    f = None

    try:
        opts, args = getopt.getopt(argv, 'f:h', ['file=', 'help'])
    except getopt.GetoptError as e:
        print("Opt error: " + e.msg)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-f', '--file'):
            f = arg
        else:
            print("Unknown argument: " + opt)
            sys.exit(1)

    assert f
    calculate(f)


if __name__ == '__main__':
    main(sys.argv[1:])
