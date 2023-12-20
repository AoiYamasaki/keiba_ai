import numpy as np

def ecliptic_to_equatorial(ecl_lon, ecl_lat, obliquity):
    """
    黄道座標から赤道座標への変換
    :param ecl_lon: 黄道経度（度）
    :param ecl_lat: 黄道緯度（度）
    :param obliquity: 黄道傾斜角（度）
    :return: 赤道座標（赤経、赤緯）（度）
    """
    # ラジアンに変換
    ecl_lon_rad = np.radians(ecl_lon)
    ecl_lat_rad = np.radians(ecl_lat)
    obliquity_rad = np.radians(obliquity)

    # 赤道座標への変換
    ra_rad = np.arctan2(np.sin(ecl_lon_rad) * np.cos(obliquity_rad) - np.tan(ecl_lat_rad) * np.sin(obliquity_rad), np.cos(ecl_lon_rad))
    dec_rad = np.arcsin(np.sin(ecl_lat_rad) * np.cos(obliquity_rad) + np.cos(ecl_lat_rad) * np.sin(obliquity_rad) * np.sin(ecl_lon_rad))

    # 度に変換
    ra = np.degrees(ra_rad)
    dec = np.degrees(dec_rad)

    return ra, dec

def equatorial_to_ecliptic(ra, dec, obliquity):
    """
    赤道座標から黄道座標への変換
    :param ra: 赤経（度）
    :param dec: 赤緯（度）
    :param obliquity: 黄道傾斜角（度）
    :return: 黄道座標（黄道経度、黄道緯度）（度）
    """
    # ラジアンに変換
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    obliquity_rad = np.radians(obliquity)

    # 黄道座標への変換
    ecl_lon_rad = np.arctan2(np.sin(ra_rad) * np.cos(obliquity_rad) + np.tan(dec_rad) * np.sin(obliquity_rad), np.cos(ra_rad))
    ecl_lat_rad = np.arcsin(np.sin(dec_rad) * np.cos(obliquity_rad) - np.cos(dec_rad) * np.sin(obliquity_rad) * np.sin(ra_rad))

    # 度に変換
    ecl_lon = np.degrees(ecl_lon_rad)
    ecl_lat = np.degrees(ecl_lat_rad)

    return ecl_lon, ecl_lat
