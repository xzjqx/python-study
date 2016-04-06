# -*- encoding:utf-8 -*-
__author__ = 'lanzao'

from OutboxAnalysis import OutboxAnalysis
from Userlogin import Userlogin


def menu():
    print"""
	Select What You Want:
	0. Quit
	1. Search People Who have Most Comments
	2. Search All te Comments of a User
	3. Sign in WeiBo
  """


def menuChoice():
    choice = raw_input("Input Your Selection(0/1/2/3): ")
    while choice != '0':
        if choice == '3':
            username = raw_input("Input WeiBo Account: ")
            password = raw_input("Input Password: ")
            pagecount = raw_input("Input the desired number of pages:")
            o = Userlogin()
            o.userlogin(username=username, password=password,
                        pagecount=pagecount)
            print "Done!"
            choice = raw_input("Input Your Selection(0/1/2/3): ")
        elif choice == '1':
            num = raw_input("How Many?: ")
            o = OutboxAnalysis()
            o.getMost(num)
            choice = raw_input("Input Your Selection(0/1/2/3): ")
        elif choice == '2':
            name = raw_input("Who Do You Wnat: ")
            o = OutboxAnalysis()
            o.getUser(name)
            choice = raw_input("Input Your Selection(0/1/2/3): ")
        else:
            print """choice=%s""" % choice
            print "Input Error!!!"
            choice = raw_input("Input Your Selection(0/1/2/3): ")

menu()
menuChoice()
