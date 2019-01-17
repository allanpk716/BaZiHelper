# -*- coding:utf-8 -*-
import sys
from datetime import datetime, time, timedelta
import ephem

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

def main():
    
    dt = datetime.strptime("2019/01/16 13:05:27", '%Y/%m/%d %H:%M:%S')
    dt = dt + timedelta(hours=-8)

    longit = float(116.347580909729)
    latit = float(25.25979470865568)
    elev = float(0)

    # get hour angle
    ha = hour_angle(dt, longit, latit, elev)

    # convert hour angle to timedelta from noon
    days = ha / 360
    if days > 0.5:
        days -= 0.5
    td = timedelta(days=days)

    # make solar time
    solar_time = datetime.combine(dt.date(), time(12)) + td
    print(solar_time)


if __name__ == '__main__':
    main()