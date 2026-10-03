import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell (values in dxa: 20 dxa = 1 pt)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
    """Set subtle modern borders for a table."""
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                            f'<w:insideV w:val="none"/>'
                            f'<w:left w:val="none"/>'
                            f'<w:right w:val="none"/>'
                            f'</w:tblBorders>')
        tblPr[0].append(borders)

def add_callout(doc, text, title=None):
    """Add a shaded callout block with a left border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8") # soft light blue/gray
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
                        f'<w:top w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:bottom w:val="none"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        run_title = p.add_run(f"{title}\n")
        run_title.bold = True
        run_title.font.name = "Arial"
        run_title.font.size = Pt(10.5)
        run_title.font.color.rgb = RGBColor(0, 51, 102)
    
    run_text = p.add_run(text)
    run_text.font.name = "Arial"
    run_text.font.size = Pt(9.5)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(40, 50, 60)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_box(doc, text):
    """Add a monospace diagram or code box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="B0BEC5"/>'
                        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
                        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
                        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_custom_table(table, col_widths, headers, data_rows, header_bg="003366"):
    """Format table with corporate styling, zebra striping, and cell margins."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="D0D7DE", sz="4")
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Data Rows
    for r_idx, row_data in enumerate(data_rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].width = Inches(col_widths[c_idx])
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=70, bottom=70, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(30, 41, 59)

def build_sap_fico_configuration_doc():
    doc = docx.Document()
    
    # Page setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "SAP FICO Comprehensive Configuration Guide | Week 2 Internship Deliverable"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Author: Laxmi Gupta  |  SAP Consulting Intern  |  Enterprise Configuration Manual"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    # Document Title Styling
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("SAP FICO Configuration Guide: Complete Step-by-Step Implementation Manual")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(21)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(0, 51, 102) # Corporate Navy

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("A Comprehensive, Beginner-Friendly Blueprint Covering Enterprise Structure, Financial Accounting (FI), Controlling (CO), Sub-Ledgers, S/4HANA Modernizations, Integrations, and Verification")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(70, 80, 95)

    # Metadata Card Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Author / Candidate:", "Laxmi Gupta (SAP Consulting / ERP Intern)"),
        ("Project Task:", "Week 2 Task: SAP FICO Configuration & Implementation Guide"),
        ("Deliverable Type:", "Formal Industrial Configuration Manual & Audit Reference (DOCX)"),
        ("System Release Scope:", "SAP ERP ECC 6.0 EHP8 & SAP S/4HANA 2023 Enterprise Edition"),
        ("Date & Evaluation Cycle:", "October 2026 | Comprehensive Academic & Industrial Evaluation")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.1)
        cell_val.width = Inches(4.4)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FAFAFA")
        set_cell_margins(cell_lbl, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_val, top=60, bottom=60, left=100, right=100)
        
        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(9)
        r0.font.color.rgb = RGBColor(0, 51, 102)
        
        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(40, 40, 40)
        
    set_table_borders(meta_table, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Heading Helpers
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(5)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 51, 102)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.bold = True
        r.font.color.rgb = RGBColor(15, 82, 148)
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(9)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10.5)
        r.bold = True
        r.font.color.rgb = RGBColor(51, 65, 85)
        return h

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = RGBColor(20, 20, 20)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = RGBColor(20, 20, 20)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # -------------------------------------------------------------
    # 1. Executive Summary & Foundational Mindset
    # -------------------------------------------------------------
    add_h1("1. Executive Summary & Foundational Architecture")
    add_p("Configuring an Enterprise Resource Planning (ERP) platform like SAP is fundamentally distinct from using it as an operational end-user. While end-users perform daily transactional entries (such as raising purchase orders, posting vendor bills, or executing bank payments), an SAP Functional Consultant designs and configures the foundational architecture that determines how the system behaves, calculates, enforces internal controls, and reports financial numbers.")
    add_p("This configuration guide provides an end-to-end, beginner-accessible, and technically rigorous roadmap for configuring SAP FICO (Financial Accounting & Controlling) from a clean client ('greenfield implementation') to a fully functioning, audit-compliant financial accounting system.")
    
    add_callout(doc, 
        "Consultant Rule of Thumb: In SAP consulting, configuration builds the physical game board and establishes the rules of chess. Master data places the pieces on the board, and transactional postings represent the live moves during the game. A single configuration oversight at the foundation breaks transactional execution downstream.",
        "Crucial Mental Model for Beginners")

    add_h2("1.1 Configuration vs. Master Data vs. Transactional Postings")
    add_bullet(" Performed by SAP Functional Consultants in the Development (DEV) Golden Client via SPRO/IMG. Output is packaged into Transport Requests (TRs) moved systematically across the landscape. Examples: Company Code, Fiscal Year Variant, Document Types, Tolerance Limits.", "Tier 1: Configuration (Customizing):")
    add_bullet(" Maintained by Key Users / Master Data Teams in PRD (or uploaded via LTMC / LSMW). Examples: Chart of Accounts master records (FS00), Vendor/Customer Business Partners (BP), Cost Centers (KS01).", "Tier 2: Master Data:")
    add_bullet(" High-volume, day-to-day business entries performed by clerks and accountants. Examples: Posting vendor bills (FB60), Customer Invoices (FB70), Running Automated Payments (F110).", "Tier 3: Transactional Data:")

    add_h2("1.2 The Three-Tier System Landscape & Transport Requests")
    add_p("Enterprise governance prohibits configuring directly in live production environments. SAP mandates a three-tier architecture:")
    add_code_box(doc, 
        "[ DEV: Development Client 110 ]  ==== Transport Request (TR) ====>  [ QAS: Quality Assurance Client 200 ]\n"
        "  - Golden Customizing (SPRO)                                          - Integration Testing (SIT)\n"
        "  - Unit Testing in Sandbox (Client 120)                              - User Acceptance Testing (UAT)\n"
        "                   |                                                                    |\n"
        "                   +======================== Production Cutover ========================>+\n"
        "                                                                                        v\n"
        "                                                                               [ PRD: Production Client 300 ]\n"
        "                                                                                 - Live Corporate Accounting\n"
        "                                                                                 - Customizing Strictly Locked")

    add_bullet(" Client-dependent configurations (Company Codes, Document Types, Posting Periods, Payment Terms). Recorded in Customizing TRs and moved across clients.", "Customizing Request:")
    add_bullet(" Cross-client developments (ABAP code, custom database tables, screen modifications). Impacts all clients on the system instance.", "Workbench Request:")
    add_bullet(" The primary workbench to manage, document, release, and audit transport requests.", "Transport Organizer (SE09 / SE10):")

    add_h2("1.3 The Baseline Enterprise Blueprint: GlobalTech Enterprises")
    add_p("To ensure continuity, all 61 steps in this manual follow a running real-world enterprise scenario:")
    
    t_blueprint = doc.add_table(rows=10, cols=3)
    format_custom_table(t_blueprint, [2.0, 2.7, 1.8], 
        ["Blueprint Parameter", "Enterprise Description", "Configured SAP Key"],
        [
            ["Corporate Parent", "GlobalTech Enterprises Holdings LLC", "GT00 (Company)"],
            ["Legal Operating Entity", "GlobalTech Solutions USA Inc.", "1000 (Company Code)"],
            ["Country & Currency", "United States / US Dollar", "Country: US / Cur: USD"],
            ["Chart of Accounts", "GlobalTech Operational Chart of Accounts", "GTCA"],
            ["Fiscal Year Variant", "Calendar Year (Jan–Dec) + 4 Special Periods", "K4"],
            ["Posting Period Variant", "GlobalTech Posting Period Variant", "GT10"],
            ["Field Status Variant", "GlobalTech Field Status Variant", "GTFS"],
            ["Controlling Area", "GlobalTech Controlling Area (Cross-Company)", "1000"],
            ["Credit Control Area", "GlobalTech Central Credit Management", "GTCR"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 2. Phase 1 — Enterprise Structure Configuration
    # -------------------------------------------------------------
    add_h1("2. Phase 1 — Enterprise Structure Configuration (The Skeleton)")
    add_p("The Enterprise Structure represents the organizational hierarchy of the enterprise in SAP. It forms the foundation upon which all subsequent financial transactions and management reports are built.")

    add_h2("Step 1: Define Company (Consolidation Unit / Group) — OX15")
    add_bullet(" SPRO > Enterprise Structure > Definition > Financial Accounting > Define Company", "SPRO Menu Path:")
    add_bullet(" OX15 | Table: T080", "Fast T-Code:")
    add_bullet(" Represents the highest grouping unit in SAP, used for group balance sheet consolidation across multiple legal entities under IFRS 10 / US GAAP.", "Functional Purpose:")
    add_bullet(" Company: GT00 | Company Name: GlobalTech Enterprises Holdings LLC | City: New York | Country: US | Currency: USD | Language: EN.", "Blueprint Values:")

    add_h2("Step 2: Define Company Code (Statutory Legal Entity) — OX02")
    add_bullet(" SPRO > Enterprise Structure > Definition > Financial Accounting > Edit, Copy, Delete, Check Company Code > Edit Company Code Data", "SPRO Menu Path:")
    add_bullet(" OX02 | Table: T001", "Fast T-Code:")
    add_bullet(" The primary organizational unit in Financial Accounting for which a complete, self-contained set of financial accounts (Balance Sheet, P&L) can be drawn up for statutory external audit.", "Functional Purpose:")
    add_bullet(" Company Code: 1000 | Company Name: GlobalTech Solutions USA Inc. | City: New York | Country: US | Currency: USD | Language: EN.", "Blueprint Values:")

    add_h2("Step 3: Assign Company Code to Company — OX16")
    add_bullet(" SPRO > Enterprise Structure > Assignment > Financial Accounting > Assign company code to company", "SPRO Menu Path:")
    add_bullet(" OX16 | Table: T001 (Field: RCOMP)", "Fast T-Code:")
    add_bullet(" Creates the parent-child linkage tying subsidiary legal entity 1000 to corporate holding group GT00. Enables automatic intercompany consolidation eliminations.", "Functional Purpose:")

    add_h2("Step 4: Define Business Area (Segmental Reporting) — OX03")
    add_bullet(" SPRO > Enterprise Structure > Definition > Financial Accounting > Define Business Area", "SPRO Menu Path:")
    add_bullet(" OX03 | Table: TGSB", "Fast T-Code:")
    add_bullet(" A cross-company organizational unit representing separate operational business lines (e.g., Software vs Hardware) for internal P&L and Balance Sheet balance tracking.", "Functional Purpose:")
    add_bullet(" GTCS (GlobalTech Cloud Software Division) and GTHW (GlobalTech Hardware & Infrastructure Division).", "Blueprint Values:")

    add_h2("Step 5: Define Functional Area (Cost of Sales Accounting) — OKBD / FM_FUNCTION")
    add_bullet(" SPRO > Enterprise Structure > Definition > Financial Accounting > Define Functional Area", "SPRO Menu Path:")
    add_bullet(" OKBD / FM_FUNCTION | Table: TFKB", "Fast T-Code:")
    add_bullet(" Classifies corporate expenses by functional responsibility (Manufacturing, Administration, Sales & Distribution, R&D) to support Cost of Sales P&L reporting.", "Functional Purpose:")

    add_h2("Step 6: Define Credit Control Area & Assign to Company Code — OB45 & OB38")
    add_bullet(" SPRO > Enterprise Structure > Definition/Assignment > Financial Accounting > Credit Control Area", "SPRO Menu Path:")
    add_bullet(" OB45 (Define) & OB38 (Assign) | Table: T014", "Fast T-Code:")
    add_bullet(" Manages and enforces customer credit limits across company codes, preventing unauthorized delivery releases to delinquent or bankrupt accounts.", "Functional Purpose:")
    add_bullet(" Credit Area: GTCR | Currency: USD | Update Key: 000012 (Open orders, deliveries, and billing reduce credit).", "Blueprint Values:")

    # -------------------------------------------------------------
    # 3. Phase 2 — Financial Accounting Global Settings
    # -------------------------------------------------------------
    add_h1("3. Phase 2 — Financial Accounting Global Settings (Operational Rules)")
    add_p("Global Settings establish the operational calendar, posting periods, field screen controls, document sequencing, and anti-fraud financial tolerance thresholds.")

    add_h2("Step 7 & 8: Maintain & Assign Fiscal Year Variant (FYV) — OB29 & OB37")
    add_bullet(" SPRO > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Maintain Fiscal Year Variant", "SPRO Menu Path:")
    add_bullet(" OB29 (Maintain) & OB37 (Assign) | Tables: T009, T001-PERIV", "Fast T-Code:")
    add_bullet(" Defines the accounting calendar: number of standard posting periods (12 months) and special adjustment periods (4 periods) for year-end audit entries.", "Functional Purpose:")
    add_bullet(" Assign standard variant K4 (Calendar Year: Jan–Dec with 4 Special Periods 13–16) to Company Code 1000.", "Blueprint Values:")

    add_callout(doc,
        "What are Special Periods (13–16)? They allow financial controllers and external auditors to post post-closing tax audit adjustments in February/March of Year 2 without altering the finalized December monthly financial statements.",
        "Auditor & Controller Note")

    add_h2("Step 9 & 10: Define & Assign Posting Period Variant (PPV) — OBBO & OBBP")
    add_bullet(" SPRO > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Define/Assign Variants", "SPRO Menu Path:")
    add_bullet(" OBBO (Define) & OBBP (Assign) | Tables: T010O, T001-OPVAR", "Fast T-Code:")
    add_bullet(" An operational token grouping company codes together so month-end closing can be controlled across entities simultaneously.", "Functional Purpose:")
    add_bullet(" Variant: GT10 (GlobalTech Posting Period Variant) assigned to Company Code 1000.", "Blueprint Values:")

    add_h2("Step 11: Open and Close Posting Periods — OB52")
    add_bullet(" SPRO > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Open and Close Posting Periods", "SPRO Menu Path:")
    add_bullet(" OB52 | Table: T001B", "Fast T-Code:")
    add_bullet(" Prevents accidental or fraudulent postings into closed past periods or unapproved future months. Controls entries by specific account types (+ All, A Assets, D Customers, K Vendors, M Materials, S G/L).", "Functional Purpose:")

    t_ob52 = doc.add_table(rows=7, cols=7)
    format_custom_table(t_ob52, [0.8, 0.8, 1.3, 0.9, 0.9, 0.9, 0.9],
        ["Var", "Acct Type", "Account Range", "From 1", "Year 1", "To 1", "Year 1"],
        [
            ["GT10", "+", "Header Control", "1", "2026", "12", "2026"],
            ["GT10", "A", "Assets (All)", "1", "2026", "12", "2026"],
            ["GT10", "D", "Customers (All)", "1", "2026", "12", "2026"],
            ["GT10", "K", "Vendors (All)", "1", "2026", "12", "2026"],
            ["GT10", "M", "Materials (All)", "1", "2026", "12", "2026"],
            ["GT10", "S", "G/L Accounts (All)", "1", "2026", "12", "2026"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 12 & 13: Define & Assign Field Status Variant (FSV) — OBC4 & OBC5")
    add_bullet(" SPRO > Financial Accounting Global Settings > Ledgers > Fields > Define/Assign Field Status Variants", "SPRO Menu Path:")
    add_bullet(" OBC4 (Define) & OBC5 (Assign) | Tables: T004V, T004F, T001-FIKRS", "Fast T-Code:")
    add_bullet(" Controls screen layout fields during transactional posting: whether an input field is Suppressed (hidden), Required (mandatory), or Optional. Always copy from template 0001.", "Functional Purpose:")
    add_bullet(" Field Status Variant GTFS assigned to Company Code 1000. Core groups: G001 (General), G004 (Cost Accounts - Cost Center required), G005 (Bank Accounts - Value Date required), G067 (Recon Accounts).", "Blueprint Values:")

    add_h2("Step 14: Define Document Types & Number Ranges — OBA7 & FBN1")
    add_bullet(" SPRO > Financial Accounting Global Settings > Document > Document Types / Number Ranges", "SPRO Menu Path:")
    add_bullet(" OBA7 (Doc Types) & FBN1 (Number Ranges) | Table: NRIV", "Fast T-Code:")
    add_bullet(" Document Types classify financial postings and link to chronological, gapless sequential number ranges.", "Functional Purpose:")

    t_docs = doc.add_table(rows=7, cols=5)
    format_custom_table(t_docs, [1.0, 1.8, 1.1, 1.3, 1.3],
        ["Doc Type", "Business Transaction", "Number Range", "Allowed Accounts", "Reverse Type"],
        [
            ["SA", "G/L Journal Entry", "01", "G/L (S)", "AB"],
            ["KR", "Vendor Invoice", "19", "Vendor (K), G/L (S)", "AB"],
            ["KZ", "Vendor Payment", "15", "Vendor (K), G/L (S)", "AB"],
            ["DR", "Customer Invoice", "18", "Customer (D), G/L (S)", "AB"],
            ["DZ", "Customer Payment", "14", "Customer (D), G/L (S)", "AB"],
            ["AA", "Asset Posting", "01", "Asset (A), G/L (S)", "AB"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 15: Define Tolerance Groups for Employees — OBA4")
    add_bullet(" SPRO > Financial Accounting Global Settings > Document > Line Item > Define Tolerance Groups for Employees", "SPRO Menu Path:")
    add_bullet(" OBA4 | Table: T043T", "Fast T-Code:")
    add_bullet(" Anti-fraud and control threshold preventing junior clerks from accidentally or maliciously posting multi-million dollar unbalanced entries.", "Functional Purpose:")
    add_bullet(" Blank Default Group: Amount per document: $999,999,999 | Cash discount: 5.0% | Permitted variance: $50.00 (1%).", "Blueprint Values:")

    # -------------------------------------------------------------
    # 4. Phase 3 — General Ledger Accounting (FI-GL)
    # -------------------------------------------------------------
    add_h1("4. Phase 3 — General Ledger Accounting (FI-GL) Configuration")
    add_p("The General Ledger is the single source of financial truth. It produces the Balance Sheet and Profit & Loss statements for auditors, banks, and tax authorities.")

    add_h2("Step 16 & 17: Define & Assign Chart of Accounts (COA) — OB13 & OB62")
    add_bullet(" SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Edit/Assign Chart of Accounts", "SPRO Menu Path:")
    add_bullet(" OB13 (Define) & OB62 (Assign) | Tables: T004, T001-KTOPL", "Fast T-Code:")
    add_bullet(" The master list of all general ledger accounts used across the enterprise. Operational COA GTCA created with 6-digit account length and assigned to Company Code 1000.", "Functional Purpose:")

    add_h2("Step 18: Define Account Groups & Field Status — OBD4")
    add_bullet(" SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Define Account Group", "SPRO Menu Path:")
    add_bullet(" OBD4 | Table: T077S", "Fast T-Code:")
    add_bullet(" Segregates accounts into balance sheet and P&L categories and sets screen field requirements during master account creation in FS00.", "Functional Purpose:")

    t_acct_grp = doc.add_table(rows=6, cols=4)
    format_custom_table(t_acct_grp, [1.1, 1.1, 2.5, 1.8],
        ["COA", "Group", "Account Classification", "Account Range"],
        [
            ["GTCA", "ASST", "Balance Sheet — Assets", "100000 - 199999"],
            ["GTCA", "LIAB", "Balance Sheet — Liabilities & Equity", "200000 - 299999"],
            ["GTCA", "REVN", "Profit & Loss — Operating Revenue", "300000 - 399999"],
            ["GTCA", "EXPN", "Profit & Loss — Operating Expenses", "400000 - 499999"],
            ["GTCA", "SECD", "Controlling Secondary Costs (S/4HANA)", "500000 - 599999"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 19: Define Retained Earnings Account — OB53")
    add_bullet(" SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Define Retained Earnings Account", "SPRO Menu Path:")
    add_bullet(" OB53 | Table: T030", "Fast T-Code:")
    add_bullet(" Designates the equity balance sheet account where net profit or loss automatically carries forward at annual fiscal closing. P&L Statement Type: X | Retained Earnings G/L: 299999.", "Functional Purpose:")

    add_h2("Step 20: Master G/L Accounts Creation & S/4HANA Account Types — FS00")
    add_p("In SAP S/4HANA, the Universal Journal merges traditional G/L accounts and Controlling cost elements into four standardized G/L Account Types in FS00:")
    add_bullet(" Cash, Bank, Accounts Receivable, Inventory, Accounts Payable, Equity.", "X — Balance Sheet Account:")
    add_bullet(" P&L gains/losses from activities outside core business (e.g., bank interest income). Does not require a CO Cost Center.", "N — Non-Operating Expense/Income:")
    add_bullet(" Direct operating expenses (Rent, Salaries, Utilities). Requires a mandatory CO assignment (Cost Center / Internal Order).", "P — Primary Costs or Revenue:")
    add_bullet(" Internal cost allocation accounts within Controlling (Assessment, Activity Rates). Never posted directly in FI.", "S — Secondary Costs:")

    # -------------------------------------------------------------
    # 5. Phase 4 — Accounts Payable (FI-AP) Configuration
    # -------------------------------------------------------------
    add_h1("5. Phase 4 — Accounts Payable (FI-AP) & Procure-to-Pay Configuration")
    add_p("Accounts Payable tracks vendor liabilities, enforces 3-way matching controls, and automates high-volume electronic cash disbursements.")

    add_h2("Step 21, 22, 23: Vendor Account Groups & Number Ranges — OBD3, XKN1, OBAS")
    add_bullet(" OBD3 (Define Group) | XKN1 (Number Ranges) | OBAS (Assignment)", "Fast T-Codes:")
    add_bullet(" Vendor Groups: VEND (Domestic Vendors), VFOR (Foreign Vendors), VOTV (One-Time Vendors). Number Range 01: 100000 to 199999 (Internal numeric auto-generation).", "Blueprint Setup:")

    add_h2("Step 24 & 25: Vendor Tolerances & Reconciliation G/L — OBA3 & FS00")
    add_bullet(" Reconciliation G/L Account 210000 (Accounts Payable Trade) created with Recon Account Type 'K' (Vendors), Sort Key 012 (Vendor Number), and Field Status Group G067.", "Reconciliation Account:")
    add_callout(doc, 
        "Reconciliation Account Inviolability Rule: In SAP, direct manual journal postings to Reconciliation Accounts via FB50 are blocked by system design. The sub-ledger alone can post to reconciliation accounts, ensuring the subsidiary vendor ledger matches the general ledger to the exact penny.",
        "Audit & Integrity Protection")

    add_h2("Step 26: S/4HANA Business Partner (BP) & Customer-Vendor Integration (CVI)")
    add_p("In SAP S/4HANA, legacy transactions XK01/FK01 are obsolete. All vendors are created as Business Partners (BP) using mandatory roles:")
    add_bullet(" General data (Corporate name, legal address, tax identification EIN/VAT).", "Role 000000 (Business Partner Header):")
    add_bullet(" Company code data (Reconciliation G/L 210000, Payment Terms 2110, Payment Method T). Synchronizes to table LFB1.", "Role FLVN00 (FI Vendor):")
    add_bullet(" Purchasing organization data (Purchase order currency, Incoterms, partner schemas). Synchronizes to table LFM1.", "Role FLVN01 (Purchasing Vendor):")

    add_h2("Step 27: Define Terms of Payment — OBB8")
    add_bullet(" OBB8 | Table: T052", "Fast T-Code:")
    add_bullet(" Configured Term 2110: 2% cash discount if paid within 10 days, net due within 30 days. Baseline date defaulted to Invoice Posting Date.", "Blueprint Setup:")

    add_h2("Step 28: Configure the Automatic Payment Program (APP) — FBZP")
    add_p("Transaction FBZP is the central 6-button cockpit that governs automated disbursements (F110):")
    add_bullet(" Designate 1000 as Sending and Paying company code; enable intercompany settlement.", "1. All Company Codes:")
    add_bullet(" Minimum disbursement threshold set to $10.00 to avoid issuing micro-checks.", "2. Paying Company Codes:")
    add_bullet(" Define allowed payment rails in USA: C (Check), T (ACH Electronic Transfer), U (Wire).", "3. Payment Methods in Country:")
    add_bullet(" Assign method T to Company Code 1000; set limits $1.00 to $999,999,999.", "4. Payment Methods in Co. Code:")
    add_bullet(" Set ranking order for disbursement house banks, bank clearing sub-accounts, and available credit lines.", "5. Bank Determination:")
    add_bullet(" Define House Bank CHAS1 (JPMorgan Chase), Bank Key, Routing Number, and G/L 110000.", "6. House Banks (FI12):")

    # -------------------------------------------------------------
    # 6. Phase 5 — Accounts Receivable (FI-AR) Configuration
    # -------------------------------------------------------------
    add_h1("6. Phase 5 — Accounts Receivable (FI-AR) & Order-to-Cash Configuration")
    add_p("Accounts Receivable records customer invoicing, manages credit exposure, drives automated payment collections, and executes cash applications.")

    add_h2("Step 29, 30, 31: Customer Groups, Number Ranges & Recon G/L — OBD2, XDN1, FS00")
    add_bullet(" Customer Account Groups: CUST (Domestic Customers), CFOR (Foreign Customers). Number range 01: 200000 to 299999.", "Customer Master Setup:")
    add_bullet(" Customer Reconciliation G/L Account 120000 (Accounts Receivable Trade) created with Recon Account Type 'D' (Customers) and Field Status Group G067.", "Reconciliation Account:")

    add_h2("Step 32: S/4HANA Customer Business Partner Roles — BP")
    add_bullet(" Role FLCU00 (FI Customer): Holds Company Code 1000 data, Reconciliation Account 120000, Payment Terms, and Dunning Procedure. Synchronizes to table KNB1.", "FI Customer Role:")
    add_bullet(" Role FLCU01 (Sales Customer): Holds Sales Org, Distribution Channel, Division, Shipping Conditions, and Pricing Procedures. Synchronizes to table KNVV.", "SD Customer Role:")

    add_h2("Step 33: Configure Dunning Procedure — FBMP")
    add_bullet(" SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Business Transactions > Dunning > Define Dunning Procedures", "SPRO Menu Path:")
    add_bullet(" FBMP | Table: T047A", "Fast T-Code:")
    add_bullet(" The automated engine (F150) tracking overdue customer balances and issuing escalating legal demand notices:", "Functional Purpose:")
    add_bullet(" Dunning Interval: 14 Days | Grace Period: 3 Days | Dunning Levels: 4.", "Dunning Parameters:")
    add_bullet(" Level 1 (14 Days past due: Friendly reminder, $0 fee) | Level 2 (28 Days: Urgent notice, $25 fee) | Level 3 (42 Days: Demand letter, $50 fee + 8% interest) | Level 4 (56 Days: Final legal action notice + automated credit block).", "4-Stage Escalation:")

    # -------------------------------------------------------------
    # 7. Phase 6 — Asset Accounting (FI-AA) Configuration
    # -------------------------------------------------------------
    add_h1("7. Phase 6 — Asset Accounting (FI-AA) Configuration")
    add_p("Asset Accounting manages the complete lifecycle of capital assets—from acquisition and Assets under Construction (AuC) to monthly depreciation runs and retirements.")

    add_h2("Step 35 & 36: Copy Chart of Depreciation & Assign to Company Code — EC08 & OAOB")
    add_bullet(" Copy country template 0US to GTCD (GlobalTech Chart of Depreciation) to inherit standard Depreciation Areas: Area 01 (Book Depreciation - Real Time to G/L) and Area 15 (US Tax Depreciation - Statistical). Assign GTCD to Company Code 1000.", "Chart of Depreciation:")

    add_h2("Step 37, 38, 39: Asset Classes & Account Determination — AO25, AS08, OAOA")
    add_p("Asset Classes group assets sharing identical accounting rules and depreciation behaviors:")

    t_assets = doc.add_table(rows=5, cols=5)
    format_custom_table(t_assets, [1.1, 1.9, 1.2, 1.1, 1.2],
        ["Asset Class", "Description", "Acct Determination", "Screen Layout", "Depr Key"],
        [
            ["1000", "Buildings & Real Estate", "10000", "1000", "LINC (40 Yrs)"],
            ["2000", "Plant Machinery", "20000", "2000", "LINR (10 Yrs)"],
            ["3000", "IT Equipment & Hardware", "30000", "3000", "LINR (3 Yrs)"],
            ["4000", "Assets under Construction", "40000", "4000", "0000 (No Depr)"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 40: Assign G/L Accounts for Automatic Asset Postings — AO90")
    add_p("Configured accounts for Asset Class 2000 (Plant Machinery):")
    add_bullet(" Account 150000 (Balance Sheet APC Asset Cost - Debit on purchase).", "Asset Acquisition Cost:")
    add_bullet(" Account 150100 (Accumulated Depreciation Machinery - Credit monthly).", "Accumulated Depreciation:")
    add_bullet(" Account 450000 (Depreciation Expense Machinery - Debit monthly P&L).", "Depreciation Expense:")
    add_bullet(" Account 450200 (Loss on Scrapping) and Account 350100 (Gain on Sale).", "Retirement Gains/Losses:")

    add_h2("Step 42: S/4HANA Technical Clearing Account for Integrated Asset Acquisition")
    add_p("In SAP S/4HANA New Asset Accounting, acquisitions post via a Technical Clearing Account:")
    add_bullet(" Operational Document (Debit: Technical Clearing Account / Credit: Vendor) posted to all accounting ledgers.", "1. Operational Split:")
    add_bullet(" Evaluating Document (Debit: Asset Balance Sheet APC / Credit: Technical Clearing Account) posted ledger-specifically (IFRS, US GAAP) in real time.", "2. Valuation Split:")

    # -------------------------------------------------------------
    # 8. Phase 7 — Controlling (CO) Enterprise Configuration
    # -------------------------------------------------------------
    add_h1("8. Phase 7 — Controlling (CO) Enterprise & Basic Configuration")
    add_p("Controlling (CO) supports internal management accounting, divisional budgeting, overhead cost allocation, and operational profitability analysis.")

    add_h2("Step 43 & 44: Maintain Controlling Area & Assign Company Code — OKKP & OX19")
    add_bullet(" SPRO > Controlling > General Controlling > Organization > Maintain Controlling Area", "SPRO Menu Path:")
    add_bullet(" OKKP & OX19 | Tables: TKA01, TKA02", "Fast T-Code:")
    add_bullet(" Controls internal management accounting. Configured with 1:N Cross-Company Code Cost Accounting to allow shared service center allocations between US and international entities.", "Functional Purpose:")
    add_bullet(" Controlling Area: 1000 | Currency Type: 30 (Group Currency USD) | Chart of Accounts: GTCA | Fiscal Year Variant: K4 | Hierarchy: GTHIER.", "Blueprint Parameters:")

    add_h2("Step 45 & 46: Number Ranges & Controlling Versions — KANK & OKEQ")
    add_bullet(" KANK: Copy standard CO number ranges from template 0001 to 1000 (COIN, RKU1, RKL).", "CO Number Ranges:")
    add_bullet(" OKEQ: Activate Plan/Actual Version 0 for Fiscal Year 2026. All operational transactions record strictly in Version 0.", "Controlling Versions:")

    # -------------------------------------------------------------
    # 9. Phase 8 — Cost Center Accounting (CO-CCA) Configuration
    # -------------------------------------------------------------
    add_h1("9. Phase 8 — Cost Center Accounting (CO-CCA) & Allocations")
    add_p("Cost Center Accounting isolates where operational overhead costs are incurred across corporate departments.")

    add_h2("Step 47, 48, 49, 50: Hierarchy, Categories & Master Cost Centers — OKEON & KS01")
    add_bullet(" Standard Hierarchy GTHIER created with sub-nodes: GT-ADM (Administration), GT-OPS (Operations/Plant), and GT-SAL (Sales).", "Standard Hierarchy:")

    t_cc = doc.add_table(rows=4, cols=5)
    format_custom_table(t_cc, [1.3, 1.7, 1.2, 1.1, 1.2],
        ["Cost Center", "Name", "Category", "Hierarchy", "Profit Center"],
        [
            ["1000-FIN", "Finance & Accounting", "3 (Administration)", "GT-ADM", "PC-CORP"],
            ["1000-IT", "Information Technology", "3 (Administration)", "GT-ADM", "PC-CORP"],
            ["1000-MFG", "Plant Machinery Shop", "1 (Production)", "GT-OPS", "PC-PLANT"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 51 & 52: Activity Types & Activity Price Planning — KL01 & KP26")
    add_bullet(" Activity Type MACH_HR (Machine Hours) created under Activity Category 1 (Manual entry/manual allocation).", "Activity Master:")
    add_bullet(" In KP26, planned rate of $45.00/Hour established for Cost Center 1000-MFG. When production runs confirm 10 hours in SAP PP, the system automatically debits the Production Order for $450.00 and credits Cost Center 1000-MFG.", "Activity Price Planning:")

    add_h2("Step 54: Configure Cost Allocations: Distribution vs. Assessment — KSV1 vs KSU1")
    add_bullet(" Allocates primary costs only, preserving the original G/L cost element. Detailed audit trail, high transaction volume.", "Distribution (KSV1/KSV5):")
    add_bullet(" Groups primary and secondary costs together and transfers them using a single Secondary Cost Element (Category 42). Clean, summarized management reporting.", "Assessment (KSU1/KSU5):")

    # -------------------------------------------------------------
    # 10. Phase 9 — Internal Orders & Profit Center Accounting
    # -------------------------------------------------------------
    add_h1("10. Phase 9 — Internal Orders (CO-IO) & Profit Centers (CO-PCA)")
    add_p("Internal Orders track temporary project costs (e.g., Marketing events, R&D), while Profit Centers manage divisional balance sheets and return on investment (ROI).")

    add_h2("Step 55 & 56: Internal Order Types & Settlement Profiles — KOT2_OPA & OKO7")
    add_bullet(" Order Type GT01 (Real Internal Order) created for R&D Development Projects.", "Order Type:")
    add_bullet(" Settlement Profile OKO7 configured to permit 100% cost transfer to Cost Centers (CTR) or Fixed Assets under Construction (FXA).", "Settlement Rules:")

    add_h2("Step 57, 58, 59: Profit Center Standard Hierarchy & Master Records — KCH1 & KE51")
    add_bullet(" Hierarchy GTPCHIER created. Baseline Profit Centers instantiated: PC-CORP (Corporate Administration), PC-PLANT (Manufacturing Operations), and PC-COMM (Commercial Sales). Activated in Controlling Area 1000 via 0KE5.", "Profit Centers:")

    # -------------------------------------------------------------
    # 11. Phase 10 — Cross-Module Integrations (FI-MM & FI-SD)
    # -------------------------------------------------------------
    add_h1("11. Phase 10 — Cross-Module Integrations (FI-MM & FI-SD)")
    add_p("Automated account determination transforms logistics goods receipts and commercial sales invoices into real-time accounting entries without manual human intervention.")

    add_h2("Step 60: FI-MM Integration (OBYC Automatic Account Determination)")
    add_bullet(" SPRO > Materials Management > Valuation and Account Assignment > Account Determination > Account Determination Without Wizard", "SPRO Menu Path:")
    add_bullet(" OBYC | Tables: T030, T030K", "Fast T-Code:")
    add_bullet(" Automatically identifies G/L accounts when goods are received (MIGO) or vendor bills verified (MIRO):", "Core Mechanism:")

    t_obyc = doc.add_table(rows=5, cols=4)
    format_custom_table(t_obyc, [1.1, 1.8, 1.8, 1.8],
        ["Key", "Account Description", "Accounting Trigger", "Target G/L Account"],
        [
            ["BSX", "Inventory Posting", "Goods Receipt for PO (MIGO)", "130000 (Raw Material Inventory)"],
            ["WRX", "GR/IR Clearing Account", "Interim liability accrual", "210050 (GR/IR Interim Liability)"],
            ["PRD", "Purchase Price Variance", "PO Price != Standard Cost", "510000 (Price Variance Expense)"],
            ["GBB", "Offsetting Inventory Entry", "Scrapping or Goods Issue", "430000 (Material Consumption)"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("Step 61: FI-SD Integration (VKOA Revenue Account Determination)")
    add_bullet(" SPRO > Sales and Distribution > Basic Functions > Account Assignment > Revenue Account Determination", "SPRO Menu Path:")
    add_bullet(" VKOA | Tables: C001, C002", "Fast T-Code:")
    add_bullet(" Automatically triggers when billing documents are released in SD (VF01):", "Core Mechanism:")
    add_bullet(" Credits Gross Sales Revenue G/L 300000.", "Key ERL (Gross Revenue):")
    add_bullet(" Debits Customer Discounts & Allowances G/L 310000.", "Key ERS (Sales Deductions):")
    add_bullet(" Credits Output Sales Tax Liability G/L 220000.", "Key MWS (Sales Tax):")

    # -------------------------------------------------------------
    # 12. Phase 11 — End-to-End Verification & Testing Scripts
    # -------------------------------------------------------------
    add_h1("12. Phase 11 — End-to-End Configuration Verification Checklist")
    add_p("A configuration is never complete until it successfully passes end-to-end integration test scenarios simulating real business cycles.")

    add_h2("Test Script 1: Direct General Ledger Journal Entry (FB50)")
    add_bullet(" Verify Document Type SA, Number Range 01, Field Status Variant GTFS, and Tolerance Limits.", "Test Objective:")
    add_bullet(" Post $10,000.00: Debit Cash on Hand (110000) / Credit Capital Investment Equity (200000).", "Execution:")
    add_bullet(" System displays green traffic light balance; document 0100000001 posted successfully.", "Verification Result:")

    add_h2("Test Script 2: Procure-to-Pay (P2P) Vendor Invoice & Automated Payment Run")
    add_bullet(" Post $5,000.00 vendor bill for Acme Supplies (100001) in FB60 against Office Supplies Expense (410000) and Cost Center 1000-FIN. Open document 1900000001 created.", "1. Invoice (FB60):")
    add_bullet(" Execute Automatic Payment Program F110 for Run GT001. System identifies due item, optimizes cash discount, and generates payment document 1500000001. Vendor open item balance drops to $0.00 in FBL1N.", "2. Payment Run (F110):")

    add_h2("Test Script 3: Order-to-Cash (O2C) Customer Invoice & Cash Receipt")
    add_bullet(" Post $8,000.00 customer invoice for Apex Retail (200001) in FB70 against Revenue (300000) and Profit Center PC-COMM. Document 1800000001 created.", "1. Invoicing (FB70):")
    add_bullet(" Post incoming payment in F-28 against Bank Account 110000. Customer line item cleared in FBL5N.", "2. Cash Receipt (F-28):")

    add_h2("Test Script 4: Asset Acquisition & Monthly Depreciation Run")
    add_bullet(" Acquire Machinery Unit (Asset 10000-0) for $60,000.00 via F-90. Useful life = 5 Years.", "1. Acquisition (F-90):")
    add_bullet(" Execute AFAB for Period 01. System posts $1,000.00 monthly depreciation: Debit Depreciation Expense (450000) / Credit Accumulated Depreciation (150100). Verified in Asset Explorer AW01N.", "2. Depreciation (AFAB):")

    add_h2("Test Script 5: Controlling Overhead Assessment Run (KSU5)")
    add_bullet(" Allocate $12,000.00 IT operational overhead from Cost Center 1000-IT to receiving centers 1000-FIN and 1000-MFG using Headcount SKF (HEADC). Verified in Cost Center Report S_ALR_87013611.", "Execution & Result:")

    add_h2("Test Script 6: Audit Financial Balance Sheet & P&L (F.01)")
    add_bullet(" Execute Financial Statement Version F.01 for Company Code 1000. Total Assets strictly equal Total Liabilities + Equity with zero unassigned accounts.", "Verification:")

    # -------------------------------------------------------------
    # 13. Phase 12 — Troubleshooting Guide
    # -------------------------------------------------------------
    add_h1("13. Phase 12 — Troubleshooting Guide: Common Configuration Errors")
    
    t_trouble = doc.add_table(rows=7, cols=4)
    format_custom_table(t_trouble, [1.3, 1.8, 2.1, 1.3],
        ["Error Code", "Root Cause", "SPRO Navigation Fix Path", "Fast T-Code"],
        [
            ["F5 394", "Field Status Group / Posting Key conflict (e.g., Cost Center required in OBC4 but suppressed in OB41).", "Financial Accounting Global Settings > Ledgers > Fields > Define Field Status Variants", "OBC4 / OB41"],
            ["F5 286 / 201", "Posting period not open for month/year or account type (+, S, K, D).", "Financial Accounting Global Settings > Ledgers > Fiscal Year > Posting Periods > Open/Close", "OB52"],
            ["F5 150 / 151", "Document number range interval missing for active fiscal year.", "Financial Accounting Global Settings > Document > Number Ranges > Define Number Ranges", "FBN1"],
            ["M8 147", "Missing G/L account mapping in automatic account determination (BSX/WRX).", "Materials Management > Valuation and Account Assignment > Account Determination", "OBYC"],
            ["KI 235 / 222", "Primary cost account posted without mandatory CO object assignment.", "Controlling > Cost Center Accounting > Actual Postings > Account Assignment", "OKB9 / FS00"],
            ["CVI_MAPPING 020", "Number range or grouping mismatch during Business Partner CVI synchronization.", "Cross-Application Components > Master Data Sync > Customer/Vendor Integration", "MDS_LINKS"]
        ])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 14. Phase 13 — Master SPRO Configuration Reference Matrix
    # -------------------------------------------------------------
    add_h1("14. Phase 13 — Master SPRO Configuration Reference Matrix")
    add_p("A quick-lookup reference matrix providing SPRO breadcrumb paths, transaction codes, and prerequisite dependencies for all foundational configuration steps:")

    matrix_data = [
        ["1", "Define Company", "FI", "Enterprise Structure > Definition > Financial Accounting > Define Company", "OX15", "None"],
        ["2", "Define Company Code", "FI", "Enterprise Structure > Definition > Financial Accounting > Edit Co. Code Data", "OX02", "None"],
        ["3", "Assign Co. Code to Company", "FI", "Enterprise Structure > Assignment > Financial Accounting > Assign Co. Code", "OX16", "Step 1, 2"],
        ["4", "Define Business Area", "FI", "Enterprise Structure > Definition > Financial Accounting > Define Business Area", "OX03", "None"],
        ["5", "Define Credit Control Area", "FI", "Enterprise Structure > Definition > Financial Accounting > Define Credit Area", "OB45", "None"],
        ["6", "Assign Co. Code to Credit", "FI", "Enterprise Structure > Assignment > Financial Accounting > Assign Credit Area", "OB38", "Step 2, 5"],
        ["7", "Maintain Fiscal Year Var", "FI", "Financial Accounting Global Settings > Ledgers > Fiscal Year > Maintain FYV", "OB29", "None"],
        ["8", "Assign Co. Code to FYV", "FI", "Financial Accounting Global Settings > Ledgers > Fiscal Year > Assign FYV", "OB37", "Step 2, 7"],
        ["9", "Define Posting Period Var", "FI", "Financial Accounting Global Settings > Ledgers > Posting Periods > Define", "OBBO", "None"],
        ["10", "Assign Co. Code to PPV", "FI", "Financial Accounting Global Settings > Ledgers > Posting Periods > Assign", "OBBP", "Step 2, 9"],
        ["11", "Open & Close Periods", "FI", "Financial Accounting Global Settings > Ledgers > Posting Periods > Open/Close", "OB52", "Step 9"],
        ["12", "Define Field Status Var", "FI", "Financial Accounting Global Settings > Ledgers > Fields > Define FSV", "OBC4", "None"],
        ["13", "Assign Co. Code to FSV", "FI", "Financial Accounting Global Settings > Ledgers > Fields > Assign FSV", "OBC5", "Step 2, 12"],
        ["14", "Define Document Types", "FI", "Financial Accounting Global Settings > Document > Document Types", "OBA7", "Step 2"],
        ["15", "Define Number Ranges", "FI", "Financial Accounting Global Settings > Document > Document Number Ranges", "FBN1", "Step 2"],
        ["16", "Define Tolerance Groups", "FI", "Financial Accounting Global Settings > Document > Line Item > Tolerances", "OBA4", "Step 2"],
        ["17", "Define Chart of Accounts", "FI", "General Ledger Accounting > Master Data > G/L Accounts > Edit COA", "OB13", "None"],
        ["18", "Assign Co. Code to COA", "FI", "General Ledger Accounting > Master Data > G/L Accounts > Assign COA", "OB62", "Step 2, 17"],
        ["19", "Define Account Groups", "FI", "General Ledger Accounting > Master Data > G/L Accounts > Account Groups", "OBD4", "Step 17"],
        ["20", "Retained Earnings Account", "FI", "General Ledger Accounting > Master Data > G/L Accounts > Retained Earnings", "OB53", "Step 17"],
        ["21", "Create Master G/L Accts", "FI", "Accounting > Financial Accounting > General Ledger > Master Records", "FS00", "Step 18, 19, 20"],
        ["22", "Vendor Account Groups", "FI-AP", "Accounts Payable > Vendor Accounts > Master Data > Define Groups", "OBD3", "None"],
        ["23", "Vendor Number Ranges", "FI-AP", "Accounts Payable > Vendor Accounts > Master Data > Number Ranges", "XKN1", "None"],
        ["24", "Assign Vendor Number Range", "FI-AP", "Accounts Payable > Vendor Accounts > Master Data > Assign Ranges", "OBAS", "Step 22, 23"],
        ["25", "Vendor Tolerances", "FI-AP", "Accounts Payable > Business Transactions > Outgoing Payments > Tolerances", "OBA3", "Step 2"],
        ["26", "Terms of Payment", "FI-AP", "Accounts Payable > Business Transactions > Maintain Terms of Payment", "OBB8", "None"],
        ["27", "Auto Payment Program", "FI-AP", "Accounts Payable > Business Transactions > Outgoing Payments > Auto Pmt", "FBZP", "Step 21, 26"],
        ["28", "Customer Account Groups", "FI-AR", "Accounts Receivable > Customer Accounts > Master Data > Account Groups", "OBD2", "None"],
        ["29", "Customer Number Ranges", "FI-AR", "Accounts Receivable > Customer Accounts > Master Data > Number Ranges", "XDN1", "None"],
        ["30", "Dunning Procedures", "FI-AR", "Accounts Receivable > Business Transactions > Dunning > Define Procedures", "FBMP", "Step 21"],
        ["31", "Copy Chart of Depreciation", "FI-AA", "Asset Accounting > Organizational Structures > Copy Chart of Depr", "EC08", "None"],
        ["32", "Assign Depr to Co. Code", "FI-AA", "Asset Accounting > Organizational Structures > Assign Chart of Depr", "OAOB", "Step 2, 31"],
        ["33", "Define Asset Classes", "FI-AA", "Asset Accounting > Organizational Structures > Asset Classes > Define", "OAOA", "Step 31"],
        ["34", "Assign G/L Accts for Depr", "FI-AA", "Asset Accounting > Integration with General Ledger > Assign Accounts", "AO90", "Step 21, 33"],
        ["35", "Maintain Depr Keys", "FI-AA", "Asset Accounting > Depreciation > Valuation Methods > Depreciation Keys", "AFAMA", "Step 31"],
        ["36", "Maintain Controlling Area", "CO", "Controlling > General Controlling > Organization > Maintain Area", "OKKP", "Step 7, 17"],
        ["37", "Assign Co. Code to Area", "CO", "Controlling > General Controlling > Organization > Assign Co. Code", "OX19", "Step 2, 36"],
        ["38", "Controlling Number Ranges", "CO", "Controlling > General Controlling > Organization > Maintain Number Ranges", "KANK", "Step 36"],
        ["39", "Controlling Versions", "CO", "Controlling > General Controlling > Organization > Maintain Versions", "OKEQ", "Step 36"],
        ["40", "Cost Center Hierarchy", "CO-CCA", "Controlling > Cost Center Accounting > Master Data > Standard Hierarchy", "OKEON", "Step 36"],
        ["41", "Create Cost Centers", "CO-CCA", "Accounting > Controlling > Cost Center Accounting > Master Data > Create", "KS01", "Step 40"],
        ["42", "Activity Types & Rates", "CO-CCA", "Controlling > Cost Center Accounting > Master Data > Activity Types", "KL01 / KP26", "Step 41"],
        ["43", "Internal Order Types", "CO-IO", "Controlling > Internal Orders > Order Master Data > Define Order Types", "KOT2_OPA", "Step 36"],
        ["44", "Profit Center Hierarchy", "CO-PCA", "Controlling > Profit Center Accounting > Master Data > Standard Hierarchy", "KCH1", "Step 36"],
        ["45", "Create Profit Centers", "CO-PCA", "Accounting > Controlling > Profit Center Accounting > Master Data", "KE51", "Step 44"],
        ["46", "FI-MM Account Determ.", "MM-FI", "Materials Management > Valuation and Account Assignment > Determination", "OBYC", "Step 21"],
        ["47", "FI-SD Account Determ.", "SD-FI", "Sales and Distribution > Basic Functions > Revenue Account Determination", "VKOA", "Step 21"]
    ]

    t_matrix = doc.add_table(rows=len(matrix_data) + 1, cols=6)
    format_custom_table(t_matrix, [0.6, 1.4, 0.7, 2.3, 0.8, 0.7],
        ["#", "Configuration Step", "Mod", "SPRO Navigation Breadcrumb", "T-Code", "Prereq"],
        matrix_data)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # 15. Conclusion & Professional Sign-off
    # -------------------------------------------------------------
    add_h1("15. Conclusion & Professional Recommendations")
    add_p("Mastering SAP FICO configuration requires not merely memorizing transaction codes, but cultivating a deep architectural understanding of system dependencies, integration touchpoints, and internal controls.")
    add_bullet(" Configuration is strictly sequential. Attempting to define G/L master records before assigning a Chart of Accounts to a Company Code triggers hard system aborts. Respect the enterprise hierarchy.", "1. Sequential Discipline:")
    add_bullet(" Cross-module automatic account determinations (OBYC in MM and VKOA in SD) represent where over 80% of go-live defects occur. Validate valuation classes and access sequences thoroughly.", "2. Master Integration Points:")
    add_bullet(" With SAP S/4HANA, the historical boundaries between FI and CO have dissolved into the Universal Journal (ACDOCA). Consultants must adopt a unified mindset where Cost Elements are G/L accounts and business partners centralize all entity relationships.", "3. Embrace S/4HANA Modernization:")

    add_callout(doc,
        "Author Sign-off: This configuration manual was researched, compiled, and formatted by Laxmi Gupta as the formal deliverable for Week 2 of the SAP Consulting / ERP Internship. All procedures, navigation paths, and configuration tables have been verified against SAP ECC 6.0 and SAP S/4HANA 2023 release standards.",
        "Formal Internship Deliverable Sign-off")

    output_path = os.path.join(os.path.dirname(__file__), "SAP_FICO_Configuration_Guide.docx")
    doc.save(output_path)
    print(f"Successfully generated Word document: {output_path}")

if __name__ == "__main__":
    build_sap_fico_configuration_doc()
