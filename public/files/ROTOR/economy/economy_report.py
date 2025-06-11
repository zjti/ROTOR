
from ROTOR.ff.ffolge import FFolge
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class EconomyReport:
    
    def __init__(self, ffolge : FFolge):
        self.ffolge= ffolge
    
    def get_report_bytes(self):
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),       # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),                # All text left-aligned
            ('GRID', (0, 0), (-1, -1), 1, colors.black),        # Grid lines
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header font bold
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),        # Body font normal
            ('FONTSIZE', (0, 0), (-1, 0), 8),   # Smaller font for header
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Regular size for body            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),              # Header padding
            ('TOPPADDING', (0, 0), (-1, 0), 8),
        ])
        
        print('xxx')
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph("ROTOR Ökonomie", styles["Heading1"]))
        elements.append(Spacer(1, 12))

        pdf = SimpleDocTemplate("/report.pdf", pagesize=A4)


        data = [
            ["","Wert","Einheit"],
            ["Dieselpreis",  f"{self.ffolge.ff_economy.get_diesel_eur_per_l()}","eur/l"],
        ]
        table = Table(data, colWidths=[200, 150, 150])
        table.setStyle(table_style)
        elements.append(table)

        
        elements.append(Paragraph("Deckungsbeitrag", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        data = [["Fruchtart","DB","DB/AKh"]]
        for i,crop in enumerate(self.ffolge.crops):
            if crop:
                data += [[   f" {i+1} : {crop.crop_data.crop_code}", 
                            f"{crop.economy.get_gross_margin_eur_per_ha() :.2f} €/ha",
                            f" {crop.economy.get_gross_margin_per_man_hour_eur_per_h() :.2f} €/AKh"]]
                
        table2 = Table(data, colWidths=[200, 150, 150])
        table2.setStyle(table_style)
        elements.append(Spacer(1, 12))
        elements.append(table2)

        elements.append(Paragraph("Leistunge/Kosten", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        data = [["Fruchtart","Leistungen","Maschinenkosten","Dieselkosten","Saatgutkosten","Sonstige Kosten"]]

        for i,crop in enumerate(self.ffolge.crops):
            if crop:
                data += [[  f" {i+1} : {crop.crop_data.crop_code}", 
                            f"{crop.economy.get_sum_leistung_eur_per_ha() :.2f} €/ha",
                            f"{crop.economy.get_sum_machine_cost_eur_per_ha() :.2f} €/ha",
                            f"{crop.economy.get_sum_diesel_cost_eur_per_ha() :.2f} €/ha" ,
                            f"{crop.economy.get_seed_cost_eur_per_ha() :.2f} €/ha" ,
                            f"{crop.economy.get_extra_cost_eur_per_ha() :.2f} €/ha" ,
                         ]]
                
        table3 = Table(data, colWidths=[100, 400/5, 400/5, 400/5, 400/5])
        table3.setStyle(table_style)
        elements.append(Spacer(1, 12))
        elements.append(table3)


        elements.append(Paragraph("Leistungen", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        data = [["Fruchtart","Erzeugerpreis","Ertrag Menge","Verkauf","Sonstige\nLeistungen" ,"Summe Leistungen"]]

        for i,crop in enumerate(self.ffolge.crops):
            if crop:
                data += [[  f" {i+1} : {crop.crop_data.crop_code}", 
                            f"{crop.economy.get_price_yield_eur_per_dt_fm() :.2f} €/dt FM",
                            f"{crop.calc_yield_dt_fm_per_ha() :.2f} dt FM/ha",
                            f"{crop.economy.get_yield_leistung_eur_per_ha() :.2f} €/ha" ,
                            f"{crop.economy.get_other_leistung_eur_per_ha() :.2f} €/ha" ,
                            f"{crop.economy.get_sum_leistung_eur_per_ha() :.2f} €/ha" ,
                         ]]
                
        table4 = Table(data, colWidths=[100, 400/5, 400/5, 400/5, 400/5, 400/5])
        table4.setStyle(table_style)
        elements.append(Spacer(1, 12))
        elements.append(table4)
        

        pdf.build(elements)
        
        
        with open("/report.pdf", "rb") as f:
            file_bytes = f.read()

        return file_bytes
        
               