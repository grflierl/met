p_levels=[10,30,100,250,500,850,1000]
gfsrange={}
gfsrange['T']=[
    [10,175,240,10,"black"],
    [20,175,240,10,"black"],
    [30,175,240,10,"black"],
    [100,180,250,10,"black"],
    [250,190,250,10,"black"],
    [500,220,280,10,"black"],
    [850,220,320,10,"black"],
    [1000,220,325,10,"black"]
    ]
gfsrange['speed']=[
    [10,0.0,120.0,10.0,"white"],
    [20,0.0,120.0,10.0,"white"],
    [30,0.0,120.0,10.0,"white"],
    [100,0.0,120.0,10.0,"white"],
    [250,0.0,120.0,10.0,"white"],
    [500,0.0,100.0,10.0,"white"],
    [850,0.0,100.0,10.0,"white"],
    [1000,0.0,100.0,10.0,"white"]
    ]
gfsrange['phi']=[
    [10,27000,32000,1000,"black"],
    [20,23000,27300,1000,"black"],
    [30,20800,24500,100,"black"],
    [100,14200,17000,100,"black"],
    [250,8900,11101,100,"black"],
    [500,4550,6050,50,"black"],
    [850,750,1700,50,"black"],
    [1000,-600,480,50,"black"]
    ]
gfsrange['slp']=[
    [1000,900,1100,50,"black"],
    ]
gfsrange['o3']=[
    [30,1e-6,1e-5,1e-6,"white"],
    ]
cnt=np.array(range(0,len(p)))
gfsr=[]
gfsx=gfsrange[field]
px=list(p)
for j in range(0,len(gfsx)):
    gfsr.append(px.index(gfsx[j][0]))
print gfsr
#for j in range(0,len(p_levels)):
#    gfsr.append(cnt[p==p_levels[j]][0])

ncnames={
    "T":"Temperature_isobaric",
    "speed":"u-component_of_wind_isobaric",
    "phi":"Geopotential_height_isobaric",
    "o3":"Ozone_Mixing_Ratio_isobaric",
    "slp":"Pressure_reduced_to_MSL_msl"}
