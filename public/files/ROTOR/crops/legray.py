from ROTOR.utils import config
from ROTOR.utils import weather
from ROTOR.utils import datehelper



def calcLG(old_cuts ,spring_seeding=False):
    """
    old_cuts is uses to extract 'nutz'
    """
    LEGRAY_CONSTS['NFK'] = config.SOIL['NFK']['default']
    
    legray_state = get_lgstate_0()
    print(legray_state,'LEGRAY')


    start = datehelper.mmdd_to_day_index('1101')
    end = datehelper.mmdd_to_day_index('1231')

 
    for day_i in range(start,end):
        wd = {}
        wd['nied'] = weather.daily_weather['PRECIPITATION'][day_i]
        wd['stra'] = weather.daily_weather['RADIATION'][day_i]   * 0.0864 
        wd['tmit']  = weather.daily_weather['TEMPERATURE_AVG'][day_i]
        wd['tmin']  = weather.daily_weather['TEMPERATURE_MIN'][day_i]
        wd['tmax']  = weather.daily_weather['TEMPERATURE_MAX'][day_i]
        wd['day_of_year'] = day_i
        wd['month_of_year'] = datehelper.day_index_to_month(day_i)
        
        add_day(wd,legray_state,spring_seeding=spring_seeding)

    
    start = datehelper.mmdd_to_day_index('0101')
    end = datehelper.mmdd_to_day_index('1231')
    for day_i in range(start,end):
        wd = {}
        wd['nied'] = weather.daily_weather['PRECIPITATION'][day_i]
        wd['stra'] = weather.daily_weather['RADIATION'][day_i]   * 0.0864 
        wd['tmit']  = weather.daily_weather['TEMPERATURE_AVG'][day_i]
        wd['tmin']  = weather.daily_weather['TEMPERATURE_MIN'][day_i]
        wd['tmax']  = weather.daily_weather['TEMPERATURE_MAX'][day_i]
        wd['day_of_year'] = day_i
        wd['month_of_year'] = datehelper.day_index_to_month(day_i)
        
        add_day(wd,legray_state,spring_seeding=spring_seeding)
    
    # for r in wd['data']:
    #     add_day(r,legray_state, verbose=False,spring_seeding=spring_seeding )
        
    print(legray_state['cuts'])
    #(1, '0525', 3.926836982871826), (2, '0702', 3.981348652233907), (3, '0817', 4.0199544128050375), (4, '0928', 1.77122647532251)
    
    return legray_state['cuts']
    # schnitte={}
    # for n,date,menge in legray_state['cuts']:
    #     schnitte[str(n)] = {'yield': int(100*(menge*10))/100, 'nutz':'grünfutter'}
    #     if str(n) in old_cuts and 'nutz' in old_cuts[str(n)]:
    #         schnitte[str(n)]['nutz'] = old_cuts[str(n)]['nutz']
    
    # return schnitte
    

LEGRAY_CONSTS = {
                    'NFK':136.5,
                    'NFK_ratio_1.NOV': 0.5,
                    'GRENZ_TEMP':5.0,
                    'TRM_KOEFF_0_0':0.0, # A16
                    'TRM_KOEFF_0_1':0.0, # A17
                    'TRM_KOEFF_1_0':0.0, # A18
                    'TRM_KOEFF_1_1':0.0, # B17
                    'TRM_KOEFF_1_2':0.0, # B18
                    'TRM_KOEFF_2_1':1.0, # C17
                    'TRM_KOEFF_2_2':1.0, # C18
                       
                    'YIELD_GROWTH_VALUES':[0.031, 0.031, 0.026, 0.018],
                    'YIELD_MIN_CUT1':None,
                    'YIELD_MIN_CUT2':None,
                    'YIELD_MIN_CUT3':2.5,
                    'YIELD_MIN_CUT4':1,
                    'YIELD_RESERVE_CUT1':None,
                    'YIELD_RESERVE_CUT2':None,
                    'YIELD_RESERVE_CUT3':None,
                    'YIELD_RESERVE_CUT4':0.1,
                        
                    'GRUENLAND_TEMP_JAN':0.5,
                    'GRUENLAND_TEMP_FEB':0.75,
                    'TEMP_SUM':200, # I7
                        
                    'A': 100 , # L5
                    'T_OPT':25, # L6
                    'T_BASE':5, # L7
                    'DRY_TUNER':1,
                    'MZeig_Months':[11,12,1,2],
                    'PET_FUNC': lambda temp,rad : (93+rad)*(22+temp)/(150*(123+temp)),
    
                    'HETT_TARGETS': [285,453,643,457],
                    }

def get_lgstate_0():
    return {'Boden': LEGRAY_CONSTS['NFK'] * LEGRAY_CONSTS['NFK_ratio_1.NOV'],
               'TRM' : 0.0,
               'GTS_T_sum':0.0,
               'GTS_W_tag':False,
               'HETT': 0.0,
               'last_cut':0,
               'cur_growth':0.0 ,
               'cuts':[]
           }


def add_day(weather_of_the_day, legray_state , verbose=True , spring_seeding = False):
    # weather_of_the_day['nied'] = weather_of_the_day['PRECIPITATION'] 
    # weather_of_the_day['stra'] = weather_of_the_day['RADIATION']   * 0.0864 
    # weather_of_the_day['tmit'] = weather_of_the_day['TEMPERATURE_AVG'] 
    # weather_of_the_day['tmin'] = weather_of_the_day['TEMPERATURE_MIN'] 
    # weather_of_the_day['tmax'] = weather_of_the_day['TEMPERATURE_MAX'] 
    # weather_of_the_day['Datum'] = weather_of_the_day['SDAY'] 
    # weather_of_the_day['monat'] = int( weather_of_the_day['SDAY'][:2] )
    
    if legray_state['last_cut'] == 2  and spring_seeding:
        return

    
    #Boden $C
    Boden = legray_state['Boden']
    # NS $D
    NS = weather_of_the_day['nied']
    #MZeig = WENN(ODER(MONAT(A7)=1;MONAT(A7)=2;MONAT(A7)=11;MONAT(A7)=12);1;0) 
    #MZeig $E
    MZeig = weather_of_the_day['month_of_year'] in LEGRAY_CONSTS['MZeig_Months']
    #NSkorr =WENN(UND(D7<Algorithmen!$A$17;E7=0);0;D7)
    #NSkorr $F
    NSkorr = 0 if NS < LEGRAY_CONSTS['TRM_KOEFF_0_1'] and MZeig == 0 else NS
    
    #TRM_KF =WENN(S6>Algorithmen!$B$18;Algorithmen!$C$18;WENN(S6>Algorithmen!$B$17;Algorithmen!$C$17;1))
    #TRM_KF $G
    TRM_KF = 1
    if legray_state['TRM'] > LEGRAY_CONSTS['TRM_KOEFF_1_2'] :
        TRM_KF = LEGRAY_CONSTS['TRM_KOEFF_2_2'] 
    elif legray_state['TRM'] > LEGRAY_CONSTS['TRM_KOEFF_1_1'] :
        TRM_KF = LEGRAY_CONSTS['TRM_KOEFF_2_1']
        
    # Wvor1 = C7+F7
    # Wvor1  $H
    Wvor1 = NSkorr + Boden
        
    #PET = =(93+AK7)*(22+O7)/(150*(123+O7))
    #PET $I  (O = TEMP, AK = RAD)
    PET = LEGRAY_CONSTS['PET_FUNC'] ( temp = weather_of_the_day['tmit'], rad = weather_of_the_day['stra'])
    
    # $J
    # =H7-(I7*G7)
    Wvor1_minus_PET =  Wvor1 - (TRM_KF*PET)
    
    # $K
    # =WENN(J7<0;H7;I7*G7)
    ETM = Wvor1 if Wvor1_minus_PET < 0 else TRM_KF * PET
    # print(Wvor1, PET,Wvor1_minus_PET, ETM)
    
    # $L
    #=H7-K7
    Wvor2 = Wvor1 - ETM
    
    # $M
    # =WENN(L8>Algorithmen!$A$8;Algorithmen!$A$8;L8)
    Wvor3 = LEGRAY_CONSTS['NFK']  if Wvor2 > LEGRAY_CONSTS['NFK'] else Wvor2
    legray_state['Boden'] = Wvor3
    # $P
    # =WENN(O7>Algorithmen!$F$5;K7;0)
    transpi = ETM if weather_of_the_day['tmit'] > LEGRAY_CONSTS['GRENZ_TEMP'] else 0
    
    # # $AH
    # # =WENN(SUMME($AF$7:$AF15)>Algorithmen!$I$7;1;0)
    # GTSWTAG = LEGRAY_CONSTS['TEMP_SUM']
    
    # $Q
    # =WENN($AH7=1;P7;0)
    abfr_gts_etm = transpi if legray_state['GTS_W_tag'] else 0
    
    # $R
    # =WENN($AH8=1;I8;0)
    abfr_gts_pet = Wvor2 if legray_state['GTS_W_tag'] else 0
    
    # $AD
    # WTag =WENN(P198>0;AH198;0)
    W_tag = legray_state['GTS_W_tag'] if transpi>0 else False
    
    # $AF
    # GTS_T =WENN(O130>0;WENN(ODER(MONAT(A130)=11;MONAT(A130)=12);0;WENN(MONAT(A130)=1;Algorithmen!$I$5;WENN(MONAT(A130)=2;Algorithmen!$I$6; WENN(MONAT(A130)=3;1;1))))*O130;0)
    GTS_T = max(weather_of_the_day['tmit'],0)
    if  weather_of_the_day['month_of_year'] in [11,12]:
        GTS_T=0
    elif weather_of_the_day['month_of_year'] in [1]:
        GTS_T *= LEGRAY_CONSTS['GRUENLAND_TEMP_JAN']
    elif weather_of_the_day['month_of_year'] in [2]:
        GTS_T *= LEGRAY_CONSTS['GRUENLAND_TEMP_FEB']
    
    legray_state['GTS_T_sum'] += GTS_T
    if legray_state['GTS_T_sum'] >= LEGRAY_CONSTS['TEMP_SUM']:
        legray_state['GTS_W_tag'] = True
        
    # $AL
    # AI = tmin ; AJ = tmax
    # tmp_al =((WENN($AI232>=Algorithmen!$L$7;$AI232;0,00001)+WENN($AJ232>Algorithmen!$L$6;Algorithmen!$L$6;$AJ232))/2)-Algorithmen!$L$7
    tmp_al = weather_of_the_day['tmin'] if weather_of_the_day['tmin'] >= LEGRAY_CONSTS['T_BASE'] else 0
    tmp_al += LEGRAY_CONSTS['T_OPT'] if weather_of_the_day['tmax'] >= LEGRAY_CONSTS['T_OPT'] else weather_of_the_day['tmax']
    tmp_al = tmp_al / 2 - LEGRAY_CONSTS['T_BASE']
    
    
    # $AM
    # TT =WENN(AL227>=0;AL227;0,000001)
    TT = tmp_al if tmp_al > 0 else 0.000001
    
    # $AN
    # ETT =WENN(AH203>0;(1/(1/AM203+1/(AK203*Algorithmen!$L$5))*WENN($AH203<>$AD203;Algorithmen!$L$8;1));0)
    ETT = 0
    if legray_state['GTS_W_tag']:
        #ETT = 1/(1/AM203+1/(AK203*Algorithmen!$L$5))*WENN($AH203<>$AD203;Algorithmen!$L$8;1)
        DRY_TUNER = LEGRAY_CONSTS['DRY_TUNER'] if W_tag != legray_state['GTS_W_tag'] else 1
        ETT = 1 / (1/TT+ 1/(weather_of_the_day['stra'] *  LEGRAY_CONSTS['A'])) * DRY_TUNER
        
        # print('ETT',ETT,'TT',TT)
    
    if spring_seeding:
        if int( weather_of_the_day['day_of_year'] ) > 165:
            legray_state['HETT'] += ETT
    else:
        legray_state['HETT'] += ETT
    
    cur_cut_HETT_target = 1e10
    if legray_state['last_cut']<4:
        cur_cut_HETT_target = sum(LEGRAY_CONSTS['HETT_TARGETS'][:legray_state['last_cut']+1])
    
    
    if legray_state['HETT'] > cur_cut_HETT_target:
        legray_state['last_cut']+=1
        if verbose :
            print('cut',legray_state['last_cut'],weather_of_the_day['day_of_year'], legray_state['cur_growth'])
        legray_state['cuts'] += [(legray_state['last_cut'],weather_of_the_day['day_of_year'], legray_state['cur_growth'])]
        if legray_state['last_cut'] == 4:
            return 
        
        legray_state['cur_growth'] = 0.0
    
    if legray_state['GTS_W_tag'] and legray_state['last_cut']<4:
        if spring_seeding:
            if int( weather_of_the_day['day_of_year'] ) > 165: # 15.MAY
                legray_state['cur_growth'] += abfr_gts_etm * LEGRAY_CONSTS['YIELD_GROWTH_VALUES'][ legray_state['last_cut' ]]
        else:
            legray_state['cur_growth'] += abfr_gts_etm * LEGRAY_CONSTS['YIELD_GROWTH_VALUES'][ legray_state['last_cut' ]]
    
    
