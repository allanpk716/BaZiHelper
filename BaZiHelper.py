# -*- coding:utf-8 -*-
import  sxtwl
import sys
from datetime import datetime, timedelta, time
import pytz
import ephem
import subprocess
type = sys.getfilesystemencoding()

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
Week = ["日", "一", "二", "三", "四", "五", "六"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]

# calc_Y 年 
# calc_M 月 
# calc_D 日 
# calc_T 时辰，也就是小时数 
def Calc_BaZi(calc_Y, calc_M, calc_D, calc_T):
    lunar = sxtwl.Lunar()
    day = lunar.getDayBySolar(calc_Y, calc_M, calc_D)
    # 年
    NL_year = Gan[day.Lyear2.tg] + Zhi[day.Lyear2.dz]
    # 月
    NL_mon = Gan[day.Lmonth2.tg] + Zhi[day.Lmonth2.dz]
    # 日
    NL_day = Gan[day.Lday2.tg] + Zhi[day.Lday2.dz]
    # 时辰
    gz = lunar.getShiGz(day.Lday2.tg, calc_T)
    NL_Time = Gan[gz.tg] + Zhi[gz.dz]
    return NL_year + NL_mon + NL_day + NL_Time

# %Y/%m/%d %H:%M:%S
def hour_angle(dt, longit, latit, elev):
    obs = ephem.Observer()
    obs.date = dt.strftime('%Y/%m/%d %H:%M:%S')
    obs.lon = longit
    obs.lat = latit
    obs.elevation = elev
    sun = ephem.Sun()
    sun.compute(obs)
    # get right ascention
    ra = ephem.degrees(sun.g_ra) - 2 * ephem.pi

    # get sidereal time at greenwich (AA ch12)
    jd = ephem.julian_date(dt)
    t = (jd - 2451545.0) / 36525
    theta = 280.46061837 + 360.98564736629 * (jd - 2451545) \
            + .000387933 * t**2 - t**3 / 38710000

    # hour angle (AA ch13)
    ha = (theta + longit - ra * 180 / ephem.pi) % 360
    return ha

# %Y/%m/%d %H:%M:%S
def CalcSolarTime(dt, longit, latit, elev):
    # get hour angle
    ha = hour_angle(dt, longit, latit, elev)
    # convert hour angle to timedelta from noon
    days = ha / 360
    if days > 0.5:
        days -= 0.5
    td = timedelta(days=days)
    # make solar time
    solar_time = datetime.combine(dt.date(), time(12)) + td
    return solar_time

def CalcShuXing(strBaZi):
    baziExe = "D:\\Work_Space\\My\\BaziEval\\Release\\Bazi.exe"
    revCommand = " -e " + strBaZi

    out_code = 0
    try:
        out_bytes = subprocess.check_output(baziExe + revCommand)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output       # Output generated before error
        out_code  = e.returncode   # Return code
    out_text = out_bytes.decode('gbk',errors='replace')
    return out_text

def Calc(pickdate, picktime, latit, longit, ipadd, timezone, countryCode):
    tt = pytz.country_timezones(countryCode)
    tz = pytz.timezone(tt[0])
    # 从本地时间转换为 UTC 时间
    dtstr = pickdate + " " + picktime + ":01"
    dt = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
    dt = tz.localize(dt)
    dt = datetime.utcfromtimestamp( dt.timestamp() )
    # 输入 UTC，计算太阳时，默认的海拔输入0
    solarTime = CalcSolarTime(dt, float(longit), float(latit), float(0))

    strBaZi = Calc_BaZi(solarTime.year, solarTime.month, solarTime.day, solarTime.hour)

    shuxing = CalcShuXing(strBaZi)

    return solarTime, strBaZi, shuxing
    