import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.ticker as mticker

import cartopy 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import numpy as np

def plot_mapscatter(projection, axes_class, z, lon, lat, xlabel, ylabel, xlim, ylim, 
                    clim, title, ctitle, imgname,tickformat=None,cbticks=10,
                    nc=200,cmap=plt.cm.rainbow,symsize=0.1,extendkw='both', hardcopy=True,zoom=False):

    fig = plt.figure(figsize=(10,6.5), dpi= 150)
    minv, maxv  = clim

    # Label axes of a Plate Carree projection with a central longitude of 180:
    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(1, 1),
                    axes_pad=0.2,
                    cbar_location='bottom',
                    cbar_mode='single',
                    cbar_pad=0.25,
                    cbar_size='3%',
                    label_mode='')  # note the empty label_mode
    ax1 = axgr[0]
    ax1.set_global()
    ax1.add_feature(cfeature.COASTLINE)

    gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=False)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
    gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])

    # New code to manually draw labels
    xticks = [-180, -120, -60, 0, 60, 120, 180]
    yticks = [-90, -60, -30, 0, 30, 60, 90]
    ax1.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax1.set_yticks(yticks, crs=ccrs.PlateCarree())
    lon_formatter = LONGITUDE_FORMATTER
    lat_formatter = LATITUDE_FORMATTER
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.yaxis.set_major_formatter(lat_formatter)

    if zoom:
      ax1.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs=ccrs.PlateCarree(central_longitude=0))     

    p = ax1.scatter(lon,lat,s=symsize,c=z,vmin=clim[0],vmax=clim[1],
                       cmap=cmap,facecolor='1.0',edgecolor=None,lw=0)
    cbar = plt.colorbar(p, cax=axgr.cbar_axes[0],orientation='horizontal',format=tickformat,extend=extendkw)
        
    
    cbar.ax.set_title(ctitle)
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    if hardcopy:
      plt.savefig(imgname,dpi=200)
      plt.close()
      plt.clf()
      fig.clf()
      print(f'Saving figure: {imgname:s}')  
    else:    
      plt.show()  
    
