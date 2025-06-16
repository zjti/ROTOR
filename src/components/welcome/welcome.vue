<template>
  <div> 
  <div class="static-text">
    <h2>ROTOR</h2>
    <p>
      ROTOR 4.0 ist ein Fruchtfolgeplaner für den Ökologischen Landbau
      Ist eine Weiterentwicklung des bisher auf MS ACCESS basierende Version als internetbasierte Anwendung
    </p>

    <p>
      ROTOR dient zur Generierung und Bewertung von Fruchtfolgen im ökologischen Landbau. Dabei werden die N- Corg-, P-,
      und K-Bilanzen und Erträge standortspezifisch gerechnet. Dabei werden Effekte von Zwischenfrüchten,
      Bodenbearbeitung und Ernte von Nebenprodukten (z.B. Stroh) berücksichtigt.
    </p>
    <p>Da die Fruchtfolge ein wichtiges Werkzeug der Unkrautkontrolle darstellt, werden Verunkrautungsrisiken von
      perennierenden, winter- und sommerannuellen Unkrauttypen abgeschätzt.
      Es werden auch pythosanitäre Restriktionen berücksichtigt.</p>
    <p>
      Neu in ROTOR 4.0 ist u.a. eine Deckungsbeitagsberechnung und eine Kalkulation von halbmonatlichen
      Arbeitszeitspitzen in Anlehnung an KTBL (2011) LELF (2016)</p>
  </div>
  <v-row justify="center" align="center">
    <v-col cols="auto" class="px-2">
      <v-img src="../../assets/imgs/zalf.jpg" height="200" width='200' contain></v-img>
    </v-col>
    <v-col cols="auto" class="px-2">
      <v-img src="../../assets/imgs/logo_bol_bmleh.png" height="200" width='370' contain></v-img>
    </v-col>
    <v-col cols="auto" class="px-2">
      <v-img src="../../assets/imgs/wm_logo.png" height="200" width='290' contain></v-img>
    </v-col>
  </v-row>
  </div>
</template>

<style scoped>
.static-text {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-size: 1.4rem;
}

.static-text h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.static-text h3 {
  color: #34495e;
  margin: 25px 0 15px 0;
}

.static-text p {
  margin-bottom: 15px;
  color: #333;
}
</style>