import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

ak = 'BwO3PehLpYTH4HXcQhFpj73Q4u5TAnos'
api_url = 'http://api.map.baidu.com/staticimage/v2'
# http://lbsyun.baidu.com/index.php?title=static

Deg_per_Pixel_of_zoom = [1.17743980920114, 0.58871990460057, 0.294359952300285, 0.147179976150142, 0.0735899880750712,
                 0.0367949940375356, 0.0183974970187678, 0.0091987485093839, 0.00459937425469195, 0.00229968712734597,
                 0.00114984356367299, 0.000574921781836494, 0.000287460890918247, 0.000143730445459123, 7.186522272956171e-05,
                 3.59326113647809e-05, 1.7966305682390398e-05, 8.98315284119521e-06, 4.49157642059761e-06]

def getBMapStaticImage(min_lon,max_lon,min_lat,max_lat,pix):
    deg_width = max_lon - min_lon
    deg_height = max_lat - min_lat
    center = (min_lon+max_lon)/2,(min_lat+max_lat)/2
    center_str = '%f,%f'%(center[0],center[1])
    Deg_per_Pixel_need = deg_width/pix if deg_width>deg_height else deg_height/pix
    zoom = (np.array(Deg_per_Pixel_of_zoom)>Deg_per_Pixel_need).sum()
    PARAMS = {'ak': ak,'center':center_str,'zoom':zoom,'width':pix,'height':pix }
    half_deg = Deg_per_Pixel_of_zoom[zoom - 1] * pix / 2
    lon_lim = [center[0]-half_deg,center[0]+half_deg]
    lat_lim = [center[1]-half_deg, center[1]+half_deg]
    r = requests.get(url = api_url, params = PARAMS)
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content))
        return im,lon_lim,lat_lim
    else:
        raise Exception('AK error or network error')

if __name__ == "__main__":
    min_lon = 116.310019
    min_lat = 39.998144
    max_lon = 116.32873
    max_lat = 40.012724
    pix = 700
    im,lon_lim,lat_lim= getBMapStaticImage(min_lon,max_lon,min_lat,max_lat,pix)
    from matplotlib._png import read_png

    plt.figure()
    plt.imshow(im,extent=lon_lim+lat_lim)
    plt.show()


