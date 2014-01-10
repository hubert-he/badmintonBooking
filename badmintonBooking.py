#!/usr/bin/env python
# coding: UTF-8
import httplib2
import urllib
import sys
import datetime
import time
import re

headers_login = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    }

def usage():
    print "Auto Booking for Badminton Reserve System at Realsil"
    print "Usage: badminton yourID  yourPassword [date] [timeFrom] [timeTo]"
    print "For Instance: badminton hubert_he xxxxxxxx "
    print "Driven by hubert_he@realsil.com.cn"

def myUrlEncode(str_list):
    url_string = ''
    flag = 0
    for mapElem in str_list:
        if flag == 0:
            flag = 1
        else:
            url_string += '&'
        url_string += urllib.urlencode(mapElem)
    return url_string

def login_OK(http):
    url = 'http://badminton.realsil.com.cn/'
    body_login = [
        {'__EVENTTARGET':''}, \
        {'__EVENTARGUMENT':''}, \
        {'__VIEWSTATE':'/wEPDwUKLTk2NzE1NjQzMWRkxxpqhFucj4cgOllJls9SHLYUAQ8='}, \
        {'__EVENTVALIDATION':'/wEWBwKfkcKABALEhISFCwKd+7qdDgLz04jBBQLixcWPCwLRjbyLDwKC3IeGDLCgXQlRlHvcS8MVRJxFufeC0UWR'}, \
        {'txtName':'hubert_he'}, \
        {'txtPwd': 'your password'}, \ # 个人密码输入位置
        {'ddlDomain':'realsil.com.cn'}, \
        {'btnLogin':'登录'} \
        ]
    response, content = http.request(url, 'POST', headers=headers_login, body=myUrlEncode(body_login))
    return response
def checkBookingOK(str):
    Booked_Warning = ur"该时间段已经被预定"
    Booked_OK = ur"一人一天最多预定1小时"
    Time_Overflow = ur"一人一周最多预定4小时"
    p = re.compile(Booked_OK)
    a = p.search(str)
    if a:
        return 0
    p = re.compile(Booked_Warning)
    a = p.search(str)
    if a:
        return 1
    p = re.compile(Time_Overflow)
    a = p.search(str)
    if a:
        return 2
    return -1

def Booking(http, path, header_list, body_list, log_msg):
    url = 'http://badminton.realsil.com.cn'
    people_num = len(header_list)
    j = 0
    for i in range(0,people_num):
        response, content = http.request(url + path, 'POST', headers=header_list[j], body=body_list[j])
        if response.status == 302:
            response, content = http.request(url + path, 'POST', headers=header_list[j], body=body_list[j])
            retCode = checkBookingOK(unicode(content, "utf-8"))
            if(retCode >= 0):
                if(retCode == 1) and (body_list[j].find('rbtnSite=A&') < 0): #change to A
                    log_msg.write("302: retCode = 1 change to A\n")
                    body_list[j] = body_list[j].replace('rbtnSite=B&','rbtnSite=A&')
                else:
                    log_msg.write("%s : retCode = %d\n" %(header_list[j]['Cookie'], retCode))
                    del header_list[j]
                    del body_list[j]
            else:
                j += 1
        else:
            retCode = checkBookingOK(unicode(content, "utf-8"))
            #print body_list[j]
            if(retCode >= 0):
                if(retCode == 1) and (body_list[j].find('rbtnSite=A&') < 0): #change to A
                    log_msg.write("%s: retCode = 1 change to A\n" %(header_list[j]['Cookie']))
                    body_list[j] = body_list[j].replace('rbtnSite=B&','rbtnSite=A&')
                else:
                    log_msg.write("%s: retCode = %d\n" %(header_list[j]['Cookie'], retCode))
                    del header_list[j]
                    del body_list[j]
            else:
                j += 1
    

if __name__ == "__main__":
    try:
        book_where = sys.argv[1]
    except:
        book_where = 'B'
    try:
        book_date = sys.argv[6]
    except:
        #print "Default: date = Tomorrow, timeFrom=19:00, timeTo=20:00"
        today = datetime.datetime.today() + datetime.timedelta(days = 7)
        book_date = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    try:
        freq1=float(sys.argv[5])
    except:
        freq1 = 2
    log_input = open('log_booking.txt', 'w+')
    log_input.write(book_date + '\n')
    
    body_booking_lan = [
    {'__EVENTTARGET':''}, \
    {'__EVENTARGUMENT':''}, \
    {'ctl00_TreeView1_ExpandState': 'nn'}, \
    {'ctl00_TreeView1_SelectedNode':'ctl00_TreeView1t0'}, \
    {'ctl00_TreeView1_PopulateLog':''}, \
    {'__VIEWSTATE':'/wEPDwUKMTM1NjM2OTkwNA9kFgJmD2QWAgIDD2QWBgIBDw8WAh4EVGV4dAUJ5ZKM5oyv5Y2OZGQCBQ88KwAJAgAPFgYeDU5ldmVyRXhwYW5kZWRkHgxTZWxlY3RlZE5vZGUFEWN0bDAwX1RyZWVWaWV3MXQwHglMYXN0SW5kZXgCAmQIFCsAA2QUKwACFgQeCFNlbGVjdGVkZx4IRXhwYW5kZWRnZBQrAAIWAh8FZ2RkAgcPZBYCAgoPD2QWAh4Hb25jbGljawUOcmV0dXJuIENoZWNrKClkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ9jdGwwMCRUcmVlVmlldzEPan5Gs2wxoxICWLylgdgffgp2NQ=='}, \
    {'__EVENTVALIDATION':'/wEWEALP6fOwCAK8oLzOAwKD8sfKAwKArvrvDQK+ronwCALhk8+aCALj79TjDALk79TjDAKFgu21CgLkpaCSDALoisfzBgLuqfOvDgLvqfOvDgKxxtnBAgKWzOzCBgKi5rTDBh6afx6aLCsLZRoKcd1plU2pDG+s'}, \
    {'ctl00$cp1$Date': book_date}, \
    {'ctl00$cp1$hfWeek': '50'}, \
    {'ctl00$cp1$hfIsAdmin': '0'}, \
    {'ctl00$cp1$hfX': '30'}, \
    {'ctl00$cp1$hfY': '650'}, \
    {'ctl00$cp1$txtTimeFrom':'18:00'}, \
    {'ctl00$cp1$txtTimeTo':'19:00'}, \
    {'ctl00$cp1$txtRemark': ''}, \
    {'ctl00$cp1$rbtnSite':'B'}, \
    {'ctl00$cp1$btnSave':'确定'} \
    ]
    body_booking_he = [
    {'__EVENTTARGET':''}, \
    {'__EVENTARGUMENT':''}, \
    {'ctl00_TreeView1_ExpandState': 'nn'}, \
    {'ctl00_TreeView1_SelectedNode':'ctl00_TreeView1t0'}, \
    {'ctl00_TreeView1_PopulateLog':''}, \
    {'__VIEWSTATE':'/wEPDwUKMTM1NjM2OTkwNA9kFgJmD2QWAgIDD2QWBgIBDw8WAh4EVGV4dAUJ5ZKM5oyv5Y2OZGQCBQ88KwAJAgAPFgYeDU5ldmVyRXhwYW5kZWRkHgxTZWxlY3RlZE5vZGUFEWN0bDAwX1RyZWVWaWV3MXQwHglMYXN0SW5kZXgCAmQIFCsAA2QUKwACFgQeCFNlbGVjdGVkZx4IRXhwYW5kZWRnZBQrAAIWAh8FZ2RkAgcPZBYCAgoPD2QWAh4Hb25jbGljawUOcmV0dXJuIENoZWNrKClkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ9jdGwwMCRUcmVlVmlldzEPan5Gs2wxoxICWLylgdgffgp2NQ=='}, \
    {'__EVENTVALIDATION':'/wEWEALP6fOwCAK8oLzOAwKD8sfKAwKArvrvDQK+ronwCALhk8+aCALj79TjDALk79TjDAKFgu21CgLkpaCSDALoisfzBgLuqfOvDgLvqfOvDgKxxtnBAgKWzOzCBgKi5rTDBh6afx6aLCsLZRoKcd1plU2pDG+s'}, \
    {'ctl00$cp1$Date': book_date}, \
    {'ctl00$cp1$hfWeek': '50'}, \
    {'ctl00$cp1$hfIsAdmin': '0'}, \
    {'ctl00$cp1$hfX': '30'}, \
    {'ctl00$cp1$hfY': '650'}, \
    {'ctl00$cp1$txtTimeFrom':'19:00'}, \
    {'ctl00$cp1$txtTimeTo':'20:00'}, \
    {'ctl00$cp1$txtRemark': ''}, \
    {'ctl00$cp1$rbtnSite':'B'}, \
    {'ctl00$cp1$btnSave':'确定'} \
    ]
    body_booking_zhu = [
    {'__EVENTTARGET':''}, \
    {'__EVENTARGUMENT':''}, \
    {'ctl00_TreeView1_ExpandState': 'nn'}, \
    {'ctl00_TreeView1_SelectedNode':'ctl00_TreeView1t0'}, \
    {'ctl00_TreeView1_PopulateLog':''}, \
    {'__VIEWSTATE':'/wEPDwUKMTM1NjM2OTkwNA9kFgJmD2QWAgIDD2QWBgIBDw8WAh4EVGV4dAUJ5ZKM5oyv5Y2OZGQCBQ88KwAJAgAPFgYeDU5ldmVyRXhwYW5kZWRkHgxTZWxlY3RlZE5vZGUFEWN0bDAwX1RyZWVWaWV3MXQwHglMYXN0SW5kZXgCAmQIFCsAA2QUKwACFgQeCFNlbGVjdGVkZx4IRXhwYW5kZWRnZBQrAAIWAh8FZ2RkAgcPZBYCAgoPD2QWAh4Hb25jbGljawUOcmV0dXJuIENoZWNrKClkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ9jdGwwMCRUcmVlVmlldzEPan5Gs2wxoxICWLylgdgffgp2NQ=='}, \
    {'__EVENTVALIDATION':'/wEWEALP6fOwCAK8oLzOAwKD8sfKAwKArvrvDQK+ronwCALhk8+aCALj79TjDALk79TjDAKFgu21CgLkpaCSDALoisfzBgLuqfOvDgLvqfOvDgKxxtnBAgKWzOzCBgKi5rTDBh6afx6aLCsLZRoKcd1plU2pDG+s'}, \
    {'ctl00$cp1$Date': book_date}, \
    {'ctl00$cp1$hfWeek': '50'}, \
    {'ctl00$cp1$hfIsAdmin': '0'}, \
    {'ctl00$cp1$hfX': '30'}, \
    {'ctl00$cp1$hfY': '650'}, \
    {'ctl00$cp1$txtTimeFrom':'20:00'}, \
    {'ctl00$cp1$txtTimeTo':'21:00'}, \
    {'ctl00$cp1$txtRemark': ''}, \
    {'ctl00$cp1$rbtnSite':'B'}, \
    {'ctl00$cp1$btnSave':'确定'} \
    ]
    
    headers_lan = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=wind_lan; domain=RS; LoginNotes=wind_lan' \
    }
    headers_he = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=hubert_he; domain=RS; LoginNotes=hubert_he' \
    }
    headers_zhu = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=luke_zhu; domain=RS; LoginNotes=luke_zhu' \
    }
    headers_du = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=baoguo_du; domain=RS; LoginNotes=baoguo_du' \
    }
    headers_peng = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=knightness_peng; domain=RS; LoginNotes=knightness_peng' \
    }
    headers_wei = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=bright_wei; domain=RS; LoginNotes=bright_wei' \
    }
    headers_gao = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=Tony_gao; domain=RS; LoginNotes=Tony_gao' \
    }
    headers_lu = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=sherbet_lu; domain=RS; LoginNotes=sherbet_lu' \
    }
    headers_huang = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=stephen_huang; domain=RS; LoginNotes=stephen_huang' \
    }
    headers_gu = { \
    'Content-type': 'application/x-www-form-urlencoded', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', \
    'Host': 'badminton.realsil.com.cn', \
    'Connection': 'keep-alive', \
    'Cookie': 'LoginName=michael_gu; domain=RS; LoginNotes=michael_gu' \
    }
    
    body_lan = myUrlEncode(body_booking_lan)
    body_he = myUrlEncode(body_booking_he)
    body_zhu = myUrlEncode(body_booking_zhu)
    booking_body_list =[body_lan, body_he, body_zhu]
    
    #booking_headers_list =[headers_lan, headers_he, headers_gao]
    booking_headers_list =[headers_he, headers_du, headers_peng]
    #booking_headers_list =[headers_he]
    #booking_body_list =[body_he]	
    http = httplib2.Http()
    res = login_OK(http)
    if res.status == 302:
        #TODO: Cookie set from  First Request
        path = res['location']
        if True:
            curr =datetime.datetime.now()
            mins = curr.minute
            hours = curr.hour
            while(hours <= 9 and (mins < 2 or mins > 57)):
                curr =datetime.datetime.now()
                hours = curr.hour
                mins = curr.minute
                if len(booking_headers_list) != 0:
                    Booking(http, path, booking_headers_list, booking_body_list, log_input)
                else:
                    log_input.write("Over Done\n")
                    http.request('http://badminton.realsil.com.cn/', headers={'Connection': 'close'})
                    sys.exit(0)
        else: # old code
            for i in range(0,180000):
                if len(booking_headers_list) != 0:
                    Booking(http, path, booking_headers_list, booking_body_list, log_input)
                else:
                    log_input.write("Over Done\n")
                    http.request('http://badminton.realsil.com.cn/', headers={'Connection': 'close'})
                    sys.exit(0)
                time.sleep(0.008)
    else:
        log_input.write("\n ERROR: 302\n")
    log_input.write("\nTimeOut\n")
    http.request('http://badminton.realsil.com.cn/', headers={'Connection': 'close'})
    sys.exit(0)
    
    
    
