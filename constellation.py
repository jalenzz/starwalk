from skyfield.api import Topos, load
from datetime import datetime
import pytz
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import get_constellation

class ConstellationCalculator:
    def __init__(self, bst_file='de421.bsp'):
        self.planets = load(bst_file)

    def get_ra_dec(self, latitude, longitude, elevation_angle, azimuth_angle):
        """获取指定位置的赤经和赤纬

        :param latitude: 纬度
        :param longitude: 经度
        :param elevation_angle: 仰角
        :param azimuth_angle: 方位角 正北方向为 0 度，顺时针方向为正

        :return: 赤经和赤纬
        """

        # 用户的当前时间，添加时区信息
        current_time = datetime.now(pytz.utc)

        # 创建一个天文观察点
        topos = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

        # 获取当前时间的儒略日
        ts = load.timescale()
        t = ts.from_datetime(current_time)

        # 创建一个天文台对象
        earth = self.planets['earth']
        observatory = earth + topos

        # 观察指定的仰角和方位角
        ra, dec, distance = observatory.at(t).from_altaz(alt_degrees=elevation_angle, az_degrees=azimuth_angle).radec()

        return ra, dec

    def get_constellation_name(self, latitude, longitude, elevation_angle, azimuth_angle):
        """获取指定位置的星座

        :param latitude: 纬度
        :param longitude: 经度
        :param elevation_angle: 仰角
        :param azimuth_angle: 方位角 正北方向为 0 度，顺时针方向为正
        :return: 星座
        :rtype: str
        """

        # 创建一个 SkyCoord 对象
        ra, dec = self.get_ra_dec(latitude, longitude, elevation_angle, azimuth_angle)
        coord = SkyCoord(ra.hours, dec.degrees, unit=u.deg)

        # 获取星座
        constellation = get_constellation(coord)

        return constellation


def main():
    constellation_calculator = ConstellationCalculator()

    latitude = float(input("输入纬度："))
    longitude = float(input("输入经度："))
    elevation_angle = float(input("输入仰角："))
    azimuth_angle = float(input("输入方位角（正北方向为 0 度，顺时针方向为正）："))

    print(constellation_calculator.get_constellation_name(latitude, longitude, elevation_angle, azimuth_angle))


if __name__ == '__main__':
    main()
