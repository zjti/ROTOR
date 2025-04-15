def mk_FF(ff, CROP_OPTS, SOIL, FERTILIZER):
    
    R = {}
    print('a',ff)
    for k,v in ff.items():
        ki = int(k)
        if ki > 1:
            precrop = ff[str(ki-1)]
        if ki == 1:
            precrop = ff[str(len(ff))]

        precrop_copts = None
        if 'crop' in precrop and precrop['crop'] in CROP_OPTS:
            precrop_copts = CROP_OPTS[precrop['crop']]
        
        
        R[k] = {}
        
        if 'crop' in v and v['crop'] in CROP_OPTS:
            copts = CROP_OPTS[v['crop']]
            # 'DUNG': {'value': True}, 
            if 'DUNG' in copts and copts['DUNG']['value'] == True:
                R[k]['dung_opt'] = True
            # stroh_opt <=  'WN_WEIZEN': {'STROH': {'value': True} }
            if 'STROH' in copts and copts['STROH']['value'] == True:
                R[k]['stroh_opt'] = True
                R[k]['anbau_opts_avail'] = True
            # zw_opt <=  'ZW_VOR': {'value': True},
            if 'ZW_VOR' in copts and copts['ZW_VOR']['value'] == True:
                if precrop_copts:
                    if 'ZW_NACH' in precrop_copts and precrop_copts['ZW_NACH']['value'] == True:
                        R[k]['zw_opt'] = True    
                        R[k]['anbau_opts_avail'] = True
                else:
                    R[k]['zw_opt'] = True
                    R[k]['anbau_opts_avail'] = True

            #has_herbst_gabe <= ...HAS_HERBST_GABE
            if 'HAS_HERBST_GABE' in copts and copts['HAS_HERBST_GABE']['value'] == True:
                R[k]['has_herbst_gabe'] = True
            
            
        
        

    return R

