# -*- coding: utf-8 -*-
"""
populate_db.py

For populating demo database
data.

Created on Oct. 20, 2017
by Jiayao
"""
import os
import numpy as np

def add_user(username, password, email, first_name, last_name,
             student=None, tutor=None, hourly_rate=0,
             bio='', course_code='COMP3297',
             course_name='Software Engineering', tag='Software Engineering',
             wallet_balance=-1, avator='default_avator.png'):
    from account.models import (User, Student, Tutor)
    if wallet_balance < 0:
        wallet_balance = np.random.randint(1, 300) * 10

    user = User.objects.create_user(username, email, password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    wallet_balance=wallet_balance,
                                    avator=avator)
    if student is not None:
        Student.objects.get_or_create(user=user)

    if tutor is not None:
        from account.models import (SubjectTag, Course)
        course = Course.objects.get_or_create(course_code=course_code, course_name=course_name)[0]
        st = SubjectTag.objects.get_or_create(tag=tag)[0]
        if hourly_rate is None:
            hourly_rate = np.random.randint(1, 300) * 10
        t = Tutor(user=user, tutor_type=tutor, bio=bio,
                  hourly_rate=hourly_rate)
        t.save()
        t.tags.add(st)
        t.courses.add(course)
        t.save()

    return user

def populate_user():
    users = []
    users.append(add_user(
        'georgem', 'georgem', 'georgem@cs.hku.hk', 'George',
        'Mitcheson', None, 'CT', 0,
        r'Before joining HKU, George accumulated many years of experience in large-scale software engineering and in R&D for real-time systems. He has headed or contributed to development of a wide range of systems spanning fields such as scientific computation, telecommunications, database management systems, control systems and autonomous robotics. This work was carried out principally in Europe and the USA. Between the two he taught for several years at the University of Puerto Rico.'))

    users.append(add_user(
        'clwang', 'choli', 'clwang@cs.hku.hk', 'Cho-Li', 'Wang', None,
        'PT', None,
        r"Professor Cho-Li Wang received his B.S. degree in Computer Science and Information Engineering from National Taiwan University in 1985. He obtained his M.S. and Ph.D. degrees in Computer Engineering from University of Southern California in 1990 and 1995 respectively. He is currently a professor at the Department of Computer Science. Professor Wang's research interests include parallel architecture, software systems for Cluster and Grid computing, and virtualization techniques for Cloud computing. Recently, he starts working on software transaction memory for multicore/GPU clusters and multi-kernel operating systems for future single-chip manycore processor. Professor Wang has published more than 130 papers in various peer reviewed journals and conference proceedings. He is/was on the editorial boards of several international journals, including IEEE Transactions on Computers (TC), Multiagent and Grid Systems (MGS), Journal of Information Science and Engineering (JISE), International Journal of Pervasive Computing and Communications (JPCC), ICST Transactions on Scalable Information Systems (SIS). He was the program chair for Cluster’03, CCGrid'09, InfoScale’09, and ICPADS’09, ISPA’11, FCST’11, FutureTech’12, and Cluster2012; and the General Chair for IPDPS2012. He has also served as program committee members for numerous international conferences, including IPDPS, CCGrid, Cloud, CloudCom, Grid, HiPC, ICPP, and ICPADS. Professor Wang is the primary investigator of China 863 project 'Hong Kong University Grid Point' (2006-2011). The HKU Grid point consists of 3004 CPU cores (31.45 Teraflops), which offers parallel computing services for the China National Grid (CNGrid) and is used as a testbed for Cloud-related systems development. He has been invited to give keynote and plenary talk related to Distributed JVM design and Cloud Computing at various international conferences.", 'COMP3230', 'Operating Systems'))

    users.append(add_user(
        'ckchui', 'kit', 'ckchui@cs.hku.hk', 'Kit', 'Chui', 1, None))

    users.append(add_user(
        'azero', 'azero', 'alphazero@deepmind.com', 'Alpha', 'Go',
        1, 'PT', np.iinfo(np.int32).max,
        r'I learn by myself and I learnt so well. No human beats me.'))

    return users


def populate():
    users = populate_user()
    return [users]


if __name__ == '__main__':
    populate()
