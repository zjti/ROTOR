
class ReproBase:
    
    std_bilanz_coefficent=0
    total_HE_coefficient = 0.35
    
    def __init__(self, ackerzahl,
                 primary_product_yield_dt_fm_per_ha, 
                 by_product_yield_dt_fm_per_ha = None,
                primary_product_residual_fraction=0,
                by_product_residual_fraction=1):
        
        self.ackerzahl = ackerzahl
        self.primary_product_residual_fraction = primary_product_residual_fraction
        self.by_product_residual_fraction = by_product_residual_fraction
        
        if by_product_yield_dt_fm_per_ha is None:
            self.by_product_yield_dt_fm_per_ha = primary_product_yield_dt_fm_per_ha * self.pp_bp_ratio 
        else:
            self.by_product_yield_dt_fm_per_ha  = by_product_yield_dt_fm_per_ha
            
        self.primary_product_yield_dt_fm_per_ha = primary_product_yield_dt_fm_per_ha
        
        
        
    def clamp_bilanz_coefficient(self, bilanz_coefficent):
        
        HE_Max = self.std_bilanz_coefficent * 1.5
        if self.ackerzahl < 50:
            HE_Min = self.std_bilanz_coefficent * self.ackerzahl / 100
        else:
            HE_Min = self.std_bilanz_coefficent * 0.5
        
        if self.std_bilanz_coefficent > 0:    
            return min( max( bilanz_coefficent, HE_Min ), HE_Max)
        else:
            return - min( max( bilanz_coefficent, abs(HE_Min) ), abs(HE_Max))
    
    def calc_humus_brutto_need(self):
        return 0
    
    def calc_humus_mehrer_leistung(self):
        return 0
    
    def calc_humus_ersatz_leistung_residuals(self):
        """
        Humusersatzleistung (HP) =
            TM-Ertrag HP [t TM*ha-a] * (1-Anteil HP abgefahren [%]) *
            Humuskoeffizient Gründüngung [HE t-1 TM]+
            TM-Ertrag HP [t TM*ha-a] * (1-Anteil HP abgefahren [%]) *
            Humuskoeffizient Stroh [HE t-1 TM] *0,75
        
        """
        ersatz_pp= (self.primary_product_yield_dt_fm_per_ha 
                * self.primary_product_residual_fraction 
                * self.humus_coefficent_gründung
                + 
                self.primary_product_yield_dt_fm_per_ha 
                * self.primary_product_residual_fraction 
                * self.humus_coefficent_stroh *0.75) * 0.1
        
        """
        Humusersatzleistung (NP) = TM-Ertrag Nebenprodukt [t TM *ha-1] 
                                * Humuskoeffizient Stroh [HE *t-1 TM] 
                                * (1-Anteil Nebenprodukt abgefahren [%])
                                + TM-Ertrag Nebenprodukt [t TM *ha-1] 
                                * Humuskoeffizient Gründüngung [HE *t-1 TM]
                                * (1-Anteil Nebenprodukt abgefahren [%])
        """
        ersatz_bp= (self.by_product_yield_dt_fm_per_ha 
                * self.by_product_residual_fraction 
                * self.humus_coefficent_gründung
                + 
                self.by_product_yield_dt_fm_per_ha 
                * self.by_product_residual_fraction 
                * self.humus_coefficent_stroh)  * 0.1
        
        return ersatz_bp + ersatz_pp
    
    def calc_humus_ersatz_leistung_fertilizer(self):
        """
        Humusersatzleistung organischer Dünger = Menge [t FM * ha-1] * TS-Gehalt [t TM * t-1 FM] * HE [HE * t-1 TM]
        """
        return 0
        
            
    def calc_humus_saldo(self):
        """
        Humussaldo [HE * ha-1] = Humusmehrerleistung + 
                                Humusbruttobedarf +
                                Humusersatzleistung (Stroh/Gründung) + 
                                Humusersatzleistung org. Dünger
        """
        S = self.calc_humus_mehrer_leistung()
        S-= self.calc_humus_brutto_need()
        S+= self.calc_humus_ersatz_leistung_residuals()
        S+= self.calc_humus_ersatz_leistung_fertilizer()
        return S
        

class ReproHumusMehrer(ReproBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
    def calc_bilanz_coefficient(self):
        """
        Bilanzkoeffizient = Ertrag [dt TM/ha]*TS-Gehalt/Standardertrag [dt TM/ha] * Standard-Bilanzkoeffizient [HE/ha]
        """
        B = self.primary_product_yield_dt_fm_per_ha / self.std_primary_product_yield_dt_fm_per_ha * self.std_bilanz_coefficent
        return self.clamp_bilanz_coefficient(B)
    
    def calc_humus_mehrer_leistung(self):
        return self.calc_bilanz_coefficient()
    

class ReproHumusZehrer(ReproBase):
    
    bp_pp_ratio = 1 # default_value for : by_product_yield_dt_fm / primary_product_yield_dt_fm 
    N_content_seed_kg_per_kg = 0.1
    N_content_by_product_kg_per_dt_FM = 1.1
    N_content_primary_product_kg_per_dt_FM = 1.1
    legum_fraction = 0
    SYMB_N_FIX = 0.5
    EWR_N_fraction_FM = 0.1 # REPRO : TM_EWR*NG_EWR
    
    
    def __init__(self,
                 total_N_from_fertilizer_kg_per_ha,  
                 N_avail_from_fertilizer_kg_per_ha ,
                 N_imission_kg_per_ha,
                 seed_kg_per_ha,
                 *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.seed_kg_per_ha = seed_kg_per_ha
        self.N_imission_kg_per_ha = N_imission_kg_per_ha
        self.N_avail_from_fertilizer_kg_per_ha = N_avail_from_fertilizer_kg_per_ha
        self.total_N_from_fertilizer_kg_per_ha = total_N_from_fertilizer_kg_per_ha
        
    def calc_N_removal_kg_per_ha(self):
        
        """
        N-Entzug = Frischmasseertrag Hauptprodukt [t/ha] * Trockenmassegehalt Hauptprodukt [t TM/t FM] * N-Gehalt Hauptprodukt [kg N/dt] *0.1 [t/dt] + Frischmasseertrag Nebenprodukt [t FM/ha] * Trockenmassegehalt Nebenprodukt [t TM/ t FM]* N-Gehalt Nebenprodukt [kg N/ dt TM] *0.1 [t/dt]
        """
        N_removal = self.primary_product_yield_dt_fm_per_ha * self.N_content_primary_product_kg_per_dt_FM 
        N_removal += self.by_product_yield_dt_fm_per_ha * self.N_content_by_product_kg_per_dt_FM 
        return N_removal
    
    def calc_N_supply_kg_per_ha(self  ):
        
        return (self.N_avail_from_fertilizer_kg_per_ha 
                + self.calc_N_fixation_kg_per_ha() 
                + self.N_from_seeding_kg_per_ha()
                + self.N_imission_kg_per_ha)
    
    def N_from_seeding_kg_per_ha(self):
        return self.seed_kg_per_ha * self.N_content_seed_kg_per_kg
    
    def calc_N_fixation_kg_per_ha(self):
        if self.legum_fraction == 0:
            return 0
        
        fix_E = (self.calc_N_removal_kg_per_ha() 
                 * self.legum_fraction
                 * self.SYMB_N_FIX)
        fix_EWR =  (self.primary_product_yield_dt_fm_per_ha 
                    * self.legum_fraction 
                    * self.SYMB_N_FIX 
                    * self.EWR_N_fraction_FM)
        
        return max( min(fix_E , self.NS_MAX_E), self.NS_MIN_E) + max( min(fix_EWR , self.NS_MAX_EWR), self.NS_MIN_EWR)
        
    def calc_system_utilization_rate(self):
        if self.ackerzahl < 20 :
            return 0.45
        if self.ackerzahl >= 100:
            return 0.85
        return  0.005*self.ackerzahl+0.35
    
    def calc_bilanz_coefficient(self):
        """
        Bilanzkoeffizient für humuszehrende Fruchtart =
                        (N-Entzug[kg N/ha]-N-Zufuhr[kg N/ha]
                        *Systemverwertungsrate)
                        /(N-Gehalt im Stalldung*Systemverwertungsrate_Stalldung)
                        *Humifizierungskoeffizient der organ. TM von Stalldung [HE/ha]
                        
         (`N_Entzug_HP_NP_kg_N.ha-1`-`N_Zufuhr_kg_N.ha-1`*Systemverwertungsrate)/
         (`N_Gehalt_Stalldung_kg_N.t-1_TM`*Systemverwertungsrate) 
         *`Humifizierungskoeffizient_der_organ._TM_Stalldung_HE.t-1_TM`
                        
        """
        B = (self.calc_N_removal_kg_per_ha()
                - self.calc_N_supply_kg_per_ha() 
                * self.calc_system_utilization_rate()) 
        
        B /= (self.total_N_from_fertilizer_kg_per_ha * self.calc_system_utilization_rate()) 
        B *= self.total_HE_coefficient
        
        return B
    
    def calc_humus_brutto_need(self):
        return - self.clamp_bilanz_coefficient(self.calc_bilanz_coefficient())
    
    