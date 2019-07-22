#!/usr/bin/env python

from datetime import datetime


def time_stamp():
    now = datetime.now()
    date = now.strftime("%d.%m.%Y %Hhr.%Mm.%Ss")
    return date
