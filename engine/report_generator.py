import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import json
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import seaborn as sns

class PDFReportGenerator:
    """Generates professional PDF reports for investor due diligence"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for professional reports"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.darkblue
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12
        )
        
        # Metric style
        self.metric_style = ParagraphStyle(
            'CustomMetric',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.darkgreen
        )
    
    def generate_investor_report(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame, 
                                price_df: pd.DataFrame, waterfall_df: pd.DataFrame) -> bytes:
        """Generate comprehensive investor due diligence report"""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Title page
        story.extend(self.create_title_page())
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.extend(self.create_executive_summary(company_df, protocol_df))
        story.append(Spacer(1, 20))
        
        # Investment Overview
        story.extend(self.create_investment_overview(protocol_df))
        story.append(Spacer(1, 20))
        
        # Risk Analysis
        story.extend(self.create_risk_analysis(company_df, protocol_df))
        story.append(Spacer(1, 20))
        
        # Portfolio Analysis
        story.extend(self.create_portfolio_analysis(company_df))
        story.append(Spacer(1, 20))
        
        # Technical Details
        story.extend(self.create_technical_details(protocol_df, waterfall_df))
        story.append(Spacer(1, 20))
        
        # Compliance & Regulatory
        story.extend(self.create_compliance_section())
        story.append(Spacer(1, 20))
        
        # Appendices
        story.extend(self.create_appendices(price_df, company_df))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_title_page(self) -> List:
        """Create professional title page"""
        elements = []
        
        # Main title
        elements.append(Paragraph("$BRICS Investment Report", self.title_style))
        elements.append(Spacer(1, 30))
        
        # Subtitle
        elements.append(Paragraph("Comprehensive Due Diligence Report", self.subtitle_style))
        elements.append(Spacer(1, 40))
        
        # Report details
        report_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"Report Date: {report_date}", self.body_style))
        elements.append(Paragraph("Internal Risk & Yield Engine", self.body_style))
        elements.append(Paragraph("Prepared for Investor Due Diligence", self.body_style))
        
        elements.append(Spacer(1, 60))
        
        # Disclaimer
        disclaimer = """
        <b>Disclaimer:</b> This report is for informational purposes only. 
        Past performance does not guarantee future results. $BRICS involves 
        credit risk and is not suitable for all investors. Please consult 
        with your financial advisor.
        """
        elements.append(Paragraph(disclaimer, self.body_style))
        
        return elements
    
    def create_executive_summary(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.subtitle_style))
        
        # Key metrics
        total_exposure = company_df['total_exposure'].sum()
        num_obligors = len(company_df)
        avg_yield = company_df['yield'].mean()
        apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
        brics_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
        
        summary_text = f"""
        <b>Investment Overview:</b><br/>
        • Total Portfolio Exposure: ${total_exposure:,.0f}<br/>
        • Number of Obligors: {num_obligors}<br/>
        • Average Portfolio Yield: {avg_yield:.1f}%<br/>
        • Target APY: {apy:.1f}%<br/>
        • Current $BRICS Price: ${brics_price:.3f}<br/><br/>
        
        <b>Key Investment Highlights:</b><br/>
        • Sovereign guarantee protection<br/>
        • Monthly yield distribution<br/>
        • Real-time risk monitoring<br/>
        • Regulatory compliance<br/>
        • No leverage or borrowing<br/>
        • $10,000 minimum investment
        """
        
        elements.append(Paragraph(summary_text, self.body_style))
        
        return elements
    
    def create_investment_overview(self, protocol_df: pd.DataFrame) -> List:
        """Create investment overview section"""
        elements = []
        
        elements.append(Paragraph("Investment Overview", self.subtitle_style))
        
        # Extract key metrics
        apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
        capital_eff = protocol_df[protocol_df['metric'] == 'capital_efficiency']['value'].iloc[0]
        weighted_pd = protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]
        overcollateralization = protocol_df[protocol_df['metric'] == 'overcollateralization']['value'].iloc[0]
        
        overview_text = f"""
        <b>How $BRICS Works:</b><br/>
        1. Banks pool trade receivables from investment-grade corporates (30-180 day tenor)<br/>
        2. CDS contracts transfer credit risk to the protocol for regulatory capital relief<br/>
        3. $BRICS tokenizes the super-senior tranche (76% of notional)<br/>
        4. Investors receive monthly CDS premiums + sovereign yield<br/>
        5. Redemption via token burn distributes yield pro rata<br/><br/>
        
        <b>Key Metrics:</b><br/>
        • Target APY: {apy:.1f}%<br/>
        • Capital Efficiency: {capital_eff:.1f}x<br/>
        • Portfolio PD: {weighted_pd*100:.1f}%<br/>
        • Overcollateralization: {overcollateralization*100:.1f}%<br/>
        """
        
        elements.append(Paragraph(overview_text, self.body_style))
        
        return elements
    
    def create_risk_analysis(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame) -> List:
        """Create risk analysis section"""
        elements = []
        
        elements.append(Paragraph("Risk Analysis", self.subtitle_style))
        
        # Risk metrics
        avg_pd = company_df['avg_pd'].mean()
        industry_diversity = company_df['industry'].nunique()
        credit_rating_dist = company_df['credit_rating'].value_counts()
        
        risk_text = f"""
        <b>Portfolio Risk Profile:</b><br/>
        • Average Portfolio PD: {avg_pd*100:.1f}%<br/>
        • Industry Diversity: {industry_diversity} sectors<br/>
        • Credit Rating Distribution: {', '.join([f'{rating}: {count}' for rating, count in credit_rating_dist.items()])}<br/><br/>
        
        <b>Risk Mitigation:</b><br/>
        • Sovereign guarantee (first-loss protection)<br/>
        • Overcollateralization (2-10%)<br/>
        • Institutional underwriting buffer<br/>
        • Monthly redemption mechanism<br/>
        • Real-time risk monitoring<br/>
        """
        
        elements.append(Paragraph(risk_text, self.body_style))
        
        return elements
    
    def create_portfolio_analysis(self, company_df: pd.DataFrame) -> List:
        """Create portfolio analysis section"""
        elements = []
        
        elements.append(Paragraph("Portfolio Analysis", self.subtitle_style))
        
        # Portfolio statistics
        total_exposure = company_df['total_exposure'].sum()
        avg_yield = company_df['yield'].mean()
        top_obligors = company_df.nlargest(5, 'total_exposure')
        
        portfolio_text = f"""
        <b>Portfolio Statistics:</b><br/>
        • Total Exposure: ${total_exposure:,.0f}<br/>
        • Average Yield: {avg_yield:.1f}%<br/>
        • Number of Obligors: {len(company_df)}<br/><br/>
        
        <b>Top 5 Obligors by Exposure:</b><br/>
        """
        
        for _, row in top_obligors.iterrows():
            portfolio_text += f"• {row['company']}: ${row['total_exposure']:,.0f} ({row['yield']:.1f}% yield)<br/>"
        
        elements.append(Paragraph(portfolio_text, self.body_style))
        
        return elements
    
    def create_technical_details(self, protocol_df: pd.DataFrame, waterfall_df: pd.DataFrame) -> List:
        """Create technical details section"""
        elements = []
        
        elements.append(Paragraph("Technical Implementation", self.subtitle_style))
        
        # Cash flow waterfall
        waterfall_text = """
        <b>Cash Flow Waterfall:</b><br/>
        """
        
        for _, row in waterfall_df.iterrows():
            waterfall_text += f"• {row['description']}: {row['percentage']*100:.1f}%<br/>"
        
        waterfall_text += """
        <br/><b>AI/ML Risk Models:</b><br/>
        • XGBoost for credit risk scoring<br/>
        • Lévy copula for tail risk aggregation<br/>
        • Real-time risk monitoring<br/>
        • Dynamic portfolio optimization<br/>
        """
        
        elements.append(Paragraph(waterfall_text, self.body_style))
        
        return elements
    
    def create_compliance_section(self) -> List:
        """Create compliance section"""
        elements = []
        
        elements.append(Paragraph("Compliance & Regulatory", self.subtitle_style))
        
        compliance_text = """
        <b>Regulatory Compliance:</b><br/>
        • Basel III Capital Requirements: Compliant<br/>
        • KYC/AML Procedures: Active<br/>
        • Data Protection (POPIA): Compliant<br/>
        • Financial Services Provider License: Active<br/><br/>
        
        <b>Audit & Reporting:</b><br/>
        • Monthly compliance reports<br/>
        • Real-time audit trails<br/>
        • Regulatory reporting to FSCA<br/>
        • Professional indemnity insurance<br/>
        """
        
        elements.append(Paragraph(compliance_text, self.body_style))
        
        return elements
    
    def create_appendices(self, price_df: pd.DataFrame, company_df: pd.DataFrame) -> List:
        """Create appendices section"""
        elements = []
        
        elements.append(Paragraph("Appendices", self.subtitle_style))
        
        # Appendix A: Price History
        elements.append(Paragraph("Appendix A: $BRICS Price History", self.subtitle_style))
        price_stats = f"""
        • 90-Day High: ${price_df['high'].max():.3f}<br/>
        • 90-Day Low: ${price_df['low'].min():.3f}<br/>
        • Average Price: ${price_df['close'].mean():.3f}<br/>
        • Price Volatility: {(price_df['high'].max() - price_df['low'].min()):.3f}<br/>
        """
        elements.append(Paragraph(price_stats, self.body_style))
        
        # Appendix B: Complete Obligor List
        elements.append(Paragraph("Appendix B: Complete Obligor List", self.subtitle_style))
        
        obligor_text = ""
        for _, row in company_df.iterrows():
            obligor_text += f"• {row['company']}: ${row['total_exposure']:,.0f} | {row['yield']:.1f}% yield | {row['avg_pd']*100:.1f}% PD<br/>"
        
        elements.append(Paragraph(obligor_text, self.body_style))
        
        return elements

# Initialize global instance
pdf_generator = PDFReportGenerator() 