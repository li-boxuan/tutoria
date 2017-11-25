# -*- coding: utf-8 -*-
"""
scheduler.py 

Created on Nov. 12, 2017
by Boxuan
"""
import argparse
import os
import sys
import random
from scheduler.models import Session
from django.utils import timezone
from dateutil import parser
from datetime import timedelta
from wallet.models import Transaction
from django.core.mail import send_mail
from account.models import User

def begin_all_sessions(time):
    print("begin all sessions, time = ", time)
    # get all sessions start at specific time
    sessions = Session.objects.filter(start_time=time)
    
    for session in sessions:
        #print("\nsession.id = ", session.id)
        records = session.bookingrecord_set.all()
        for record in records:
            if record.status == record.INCOMING:
                record.status = record.ONGOING
                record.save()
                #print("set record (id: ", record.id, ") status from INCOMING to ONGOING")
        #print("set session from ", session.status, " to ", session.CLOSED)
        session.status = session.CLOSED
        session.save()


def end_all_sessions(time):
    print("end all sessions, time = ", time)
    # get all sessions end at specific time
    sessions = Session.objects.filter(end_time=time)

    for session in sessions:
        #end sessions which just finish
        #print("\nsession.id = ", session.id)
        records = session.bookingrecord_set.all()
        for record in records:
            if record.status == record.ONGOING:
                record.status = record.FINISHED
                record.save()
                #print("set record (id: ", record.id, ") status from ONGOING to FINISHED")
                # only Private Tutor session has transaction
                if session.tutor.tutor_type == session.tutor.PRIVATE_TUTOR:
                    transaction = record.transaction
                    receiver = transaction.receiver
                    amount = transaction.amount
                    commission = transaction.commission

                    # tutor receives tuition fee
                    receiver.user.wallet_balance += amount
                    receiver.user.save()
                    
                    # send email to tutor about balance change
                    content = "Please check on Tutoria, your session " + str(session.id)
                    content += " has finished and your wallet balance has changed from "
                    content += str(receiver.user.wallet_balance - amount) + " to "
                    content += str(receiver.user.wallet_balance)
                    send_mail('Session Finished & Balance Change', content, 'noreply@hola-inc.top', [receiver.email], False)

                    # (todo) company receives commission
                    myTutor = User.objects.get(username='mytutors')
                    myTutor.wallet_balance += commission
                    myTutor.save()
                    #print("transaction id = ", transaction.id, "transfer tuition fee = ", amount, " to tutor = ", receiver)

                # send email to student (review reminder)
                content = "Please check on Tutoria, your session " + str(session.id)
                content += " has finished and you can give a comment to the tutor at "
                content += "http://127.0.0.1:8000/tutor/" + str(session.tutor.id) + "/review"
                send_mail('Session Finished, Please give your comment', content, 'noreply@hola-inc.top', [record.student.email], False)

    lock_time_bound = time + timedelta(days=1)
    print("lock_time_bound = ", lock_time_bound)
    sessions = Session.objects.filter(start_time__gt=time, start_time__lt=lock_time_bound)
    for session in sessions:
        if session.status == session.BOOKABLE:
            print(session)
            session.status = session.CLOSED
            session.save()


def run(flag, time):
    # parse the time string to datetime format
    time = parser.parse(time)
    # make timezone aware
    time = timezone.make_aware(time, timezone.get_current_timezone())
    if (flag):
        begin_all_sessions(time)
    else:
        end_all_sessions(time)

def run_range(start_time, end_time):
    start_time = parser.parse(start_time)
    start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
    end_time = parser.parse(end_time)
    end_time = timezone.make_aware(end_time, timezone.get_current_timezone())
    time = start_time
    while time <= end_time:
        end_all_sessions(time)
        begin_all_sessions(time)
        time += timedelta(minutes=30)

def help():
    print("call run(flag, time) to start/end all sessions")
    print("example: run(True, \"Nov 17 2017 9:00AM\") means begin all sessions")

    print("\n\n================================")
    print("call run_range(start_time, end_time) to go over the range")
    print("example: run_range(\"Nov 17 2017 0:00AM\", \"Nov 17 2017 11:30PM\") would begin & end all sessions in the day in turn")

if __name__ == '__main__':
    run(True, "Nov 17 2017 9:00AM")
    ## create ArgumentParser() object
    #parser = argparse.ArgumentParser()
    ## add argument
    #parser.add_argument('--flag', required=True, help='True: begin_all_sessions; False: end_all_sessions')
    #parser.add_argument('--time', required=True, help='Type in a time')
    #
    ## parse argument
    #try:
    #    args = parser.parse_args()
    #except:
    #    parser.print_help()
    #    raise
    #run(args.flag, args.time)
