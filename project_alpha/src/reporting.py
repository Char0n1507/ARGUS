from fpdf import FPDF
from datetime import datetime
from project_alpha.src.database import ForensicDB
import os

class ThreatReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Project Alpha: Daily Threat Intelligence Briefing', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_daily_report():
    db = ForensicDB()
    df = db.get_recent(limit=100)
    
    pdf = ThreatReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title Info
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Generated On: {now}", ln=True)
    pdf.cell(200, 10, f"Total Alerts Analyzed: {len(df)}", ln=True)
    
    pdf.ln(10)
    
    # High Level Stats
    if not df.empty:
        avg_score = df['score'].mean()
        top_country = df['country'].mode()[0] if not df['country'].empty else "Unknown"
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Executive Summary:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"- Average Threat Score: {avg_score:.4f}", ln=True)
        pdf.cell(200, 10, f"- Primary Attack Origin: {top_country}", ln=True)
        
        pdf.ln(10)
        
        # Detailed Table
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 10, "Time", 1)
        pdf.cell(30, 10, "Country", 1)
        pdf.cell(20, 10, "Score", 1)
        pdf.cell(100, 10, "Summary", 1)
        pdf.ln()
        
        pdf.set_font("Arial", size=8)
        for _, row in df.head(20).iterrows():
            pdf.cell(40, 10, str(row['human_time']), 1)
            pdf.cell(30, 10, str(row['country']), 1)
            pdf.cell(20, 10, f"{row['score']:.4f}", 1)
            # Truncate summary
            summary = (row['raw_summary'][:50] + '..') if len(row['raw_summary']) > 50 else row['raw_summary']
            pdf.cell(100, 10, summary, 1)
            pdf.ln()
    else:
        pdf.cell(200, 10, "No threats detected in the database.", ln=True)

    filename = f"Threat_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(filename)
    return filename

if __name__ == "__main__":
    print("Generating Report...")
    fname = generate_daily_report()
    print(f"Report generated: {fname}")
