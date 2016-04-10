#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
find out all the problems submitted but not solved in acm.tju.edu.cn.
users should input id and password at first.
"""
import getpass
import urllib.parse
import urllib.request

def main():
    user_id = input("Please input your id: ")
    # the input of password doesn't echo to console.
    password =getpass.getpass('Please input your password: ')
    postdata = urllib.parse.urlencode({
        "user_id" : user_id,
        "passwd" : password,
        "login" : "Login"
    }).encode('utf-8')
    url_prefix = "http://acm.tju.edu.cn/toj/list.php?vol="

    request = urllib.request.Request("http://acm.tju.edu.cn/toj/problem.html")
    problem = urllib.request.urlopen(request).read().decode('utf-8').split('\n')

    vol_list = [x for x in problem if x.find("Vol") != -1]
    vol_num = len(vol_list)

    to_solve = list()

    for i in range(1, vol_num):
        url = url_prefix + str(i)
        req = urllib.request.Request(url, postdata)
        r = urllib.request.urlopen(req)
        s = r.read().decode('utf-8', 'ignore')
        if s.find("Password error") != -1:
            raise Exception ("Login Failed!")
        if s.find("No such user") != -1 :
            raise Exception ("User doesn\'t exist!")
        if i == 1:
            print ("Login Success!")
        lines = s.split('\n')
        for item in lines:
            if item.startswith('p'):
                problem_status = item.split(',')
                if problem_status[1] == '2':
                    to_solve.append([problem_status[2], problem_status[3].replace('\\','').strip('"')])

    if len(to_solve) > 0:
        print ("Problem submitted but not solved:")
        print ('\n'.join( map(str, to_solve)))
    else:
        print ("You don\'t have any problem not solved.")

if __name__ == '__main__':
    main()
