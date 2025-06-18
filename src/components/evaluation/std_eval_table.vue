<template>
  <div>
    <table style="width :100%">
      <thead>
        <tr>
    <th colspan="3"  ></th>
    <th colspan="8" style="text-align: center">Stickstof-, Humus-, P- und K-Bilanzen</th>
    <th colspan="3" style="text-align: center">Verunkrautungsindices</th>
  </tr>
        <tr>
          <th> Fruchtart </th>
          <th> Ertrag</th>
          <th> Deckungbeitrag</th>
          <th> Fixierung</th>
          <th> Düngung</th>
          <th> Abfuhr</th>
          <th> Auswasch.</th>
          <th> Saldo</th>
          <th> Humus</th>
          <th> Phosphor</th>
          <th> Kalium</th>

          <th> Mehrj.</th>
          <th> Win.</th>
          <th> Som.</th>
          
        </tr>
        <tr>
          <th>  </th>
          <th style="text-align: center"> dt/ha</th>
          <th style="text-align: center"> €/ha</th>
          <th style="text-align: center" colspan="5"> kg N/ha</th>
          
          <th style="text-align: center"> kg C/ha</th>
          <th style="text-align: center"> kg P/ha</th>
          <th style="text-align: center"> kg K/ha</th>

          <th> </th>
          <th style="text-align: center" colspan="2"> annuelle</th>
          
          
        </tr>
      </thead>
      <tbody>
        
        <tr v-for="n in NJahre" :key="n" class="ma-0 pa-0">

          <td style="text-align: left">
            {{ L(FF[n].crop) }}
          </td>
          <td><mv_dsp :obj="FF[n]" akey="yield_dt_fm_per_ha" /> </td>  
          <td><mv_dsp :obj="FF[n]" akey="cropeconomy.gross_margin_eur_per_ha" /> </td>          
          <td><mv_dsp :obj="FF[n]" akey="N_fix" /></td>
          <td> <mv_dsp :obj="FF[n]" akey="N_from_fert" /></td>   
          <td> <mv_dsp :obj="FF[n]" akey="N_removal" /> </td>       
          <td> <mv_dsp :obj="FF[n]" akey="N_leach" /> </td>
          
          <td> <mv_dsp :obj="FF[n]" akey="N_balance" /></td>          
          <td> <mv_dsp :obj="FF[n]" akey="cropeval.humus" /></td>
          <td> <mv_dsp :obj="FF[n]" akey="P_balance" /> </td>
          <td> <mv_dsp :obj="FF[n]" akey="K_balance" /></td>
          <td> <mv_dsp :obj="FF[n]" akey="kraut_mj" /></td>
          <td> <mv_dsp :obj="FF[n]" akey="kraut_w" /></td>
          <td> <mv_dsp :obj="FF[n]" akey="kraut_s" /></td>
        </tr>
        <tr></tr>
        <tr><td>Mittelwerte der Fruchtfolge</td>

          <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_yield_dt_fm_per_ha"/> </td>
          <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="economy.ff_gross_margin_eur_per_ha"/> </td>
          
          <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_N_fix"/> </td>
            <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_N_from_fert"/> </td>
              <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_N_removal"/> </td>
                <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_N_leach"/> </td>
                  <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_N_balance"/> </td>

          <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_humus"/> </td>
            <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_P_balance"/> </td>
              <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_K_balance"/> </td>
                <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_kraut_mj"/> </td>
                  <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_kraut_w"/> </td>
                    <td> <mv_dsp :obj="{'MODELVALUES':FF['FF_META']}"  akey="ff_eval.mean_kraut_s"/> </td>

          
        </tr>
        
      </tbody>
    </table>

  </div>
</template>

<script setup>

import { globalStore } from "@/utils/globalstore";

const FF = globalStore.get("FF");
const NJahre = globalStore.get("FFOLGE_NJAHRE")
</script>

<style scoped>
table, th, td {
  border: 0px solid black;
}
table td {
    text-align: center;
  }
  
  /* Keep headers aligned left (or center if you prefer) */
  table th {
    text-align: left; /* or center */
  }

</style>