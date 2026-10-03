# ⚙️ SAP FICO: Complete Step-by-Step Configuration & Implementation Guide

[![SAP ERP](https://img.shields.io/badge/SAP-ECC%206.0%20%7C%20S%2F4HANA%202023-003366?style=for-the-badge&logo=sap&logoColor=white)](https://www.sap.com)
[![Topic](https://img.shields.io/badge/Focus-FICO%20Configuration%20%26%20Customizing-0070BA?style=for-the-badge)](https://help.sap.com)
[![Deliverable](https://img.shields.io/badge/Deliverable-DOCX%20%2B%20Implementation%20Manual-success?style=for-the-badge)](./SAP_FICO_Configuration_Guide.docx)
[![Author](https://img.shields.io/badge/Author-Laxmi%20Gupta-orange?style=for-the-badge)](https://github.com/Laxmi19-creator)

---

## 📌 Project Overview & Internship Context

* **Intern:** **Laxmi Gupta** (SAP Consulting / ERP Intern)
* **Assignment:** **Week 2 Task: SAP FICO Configuration**
* **Primary Objective:** Delve into the configuration aspect of SAP FICO; research, design, and document the complete steps involved in building an enterprise SAP FICO system from scratch.
* **Core Deliverable:** 
  * 📄 **[Download Word Document (DOCX)](./SAP_FICO_Configuration_Guide.docx)** (Evaluation-ready, executive-styled DOC file deliverable)
  * 📑 **[Full Configuration Manual (Markdown)](./SAP_FICO_Configuration_Guide.md)** (Complete 15-section technical reference with SPRO paths, T-codes, and data models)
  * 🐍 **[Automation Script (`build_doc.py`)](./build_doc.py)** (Python script leveraging `python-docx` for document generation)

---

## 💡 The Consultant's Mindset: What is Configuration?

For any beginner or junior consultant, understanding the distinction between the three operational tiers of SAP is crucial:

```
+-------------------------------------------------------------------------+
|                           TIER 1: CONFIGURATION                         |
|  * Performed by: SAP Functional Consultants                             |
|  * Environment: Development (DEV Client 110)                            |
|  * Tools: SPRO / Implementation Guide (IMG) / T-Codes                   |
|  * Output: Transport Requests (TRs) moved systematically                |
|  * Examples: Company Code, Fiscal Year, Document Types, Tolerance Rules |
+------------------------------------+------------------------------------+
                                     | Defines the rules and boundaries for
                                     v
+-------------------------------------------------------------------------+
|                           TIER 2: MASTER DATA                           |
|  * Performed by: Key Users / Master Data Stewards in Production         |
|  * Examples: Chart of Accounts (FS00), Business Partners (BP), Costs    |
|  * Characteristic: Long-term business records referenced repeatedly     |
+------------------------------------+------------------------------------+
                                     | Serves as the operational actors in
                                     v
+-------------------------------------------------------------------------+
|                        TIER 3: TRANSACTIONAL DATA                       |
|  * Performed by: Operational End-Users (AP Clerk, Billing Specialist)   |
|  * Environment: Production (PRD Client 300)                             |
|  * Examples: Invoices (FB60/FB70), Payments (F110), Journal (FB50)      |
|  * Characteristic: Daily high-volume business activity                  |
+-------------------------------------------------------------------------+
```

---

## 🗺️ High-Level 10-Phase Configuration Roadmap

```
Phase 1: Enterprise Structure ➔ Define Company (OX15), Company Code (OX02), Credit Area (OB45)
   │
Phase 2: Global Settings      ➔ Fiscal Year K4 (OB29), Posting Periods (OB52), Field Status (OBC4)
   │
Phase 3: General Ledger (GL)  ➔ Chart of Accounts GTCA (OB13), Account Groups (OBD4), Retained Earnings (OB53)
   │
Phase 4: Accounts Payable     ➔ Vendor Groups (OBD3), BP Roles (FLVN00/01), Terms (OBB8), Payment Engine (FBZP)
   │
Phase 5: Accounts Receivable  ➔ Customer Groups (OBD2), BP Roles (FLCU00/01), Dunning (FBMP), Credit Limits
   │
Phase 6: Asset Accounting     ➔ Chart of Depr (EC08), Asset Classes (OAOA), Account Determination (AO90)
   │
Phase 7: Controlling Basic    ➔ Controlling Area (OKKP), CO Number Ranges (KANK), Version 0 (OKEQ)
   │
Phase 8: Cost Center Acct     ➔ Standard Hierarchy (OKEON), Cost Centers (KS01), Activity Planning (KP26)
   │
Phase 9: Internal Orders & PC ➔ Order Types (KOT2_OPA), Settlement (OKO7), Profit Centers (KE51)
   │
Phase 10: Cross-Module Integr ➔ FI-MM Account Determination (OBYC), FI-SD Revenue Accounts (VKOA)
```

---

## 🏢 The Baseline Blueprint: GlobalTech Enterprises Inc.

To provide clear, coherent examples throughout the guide, every configuration step was built on a consistent enterprise blueprint:

| Entity Level | Real-World Entity Name | Configured Technical Key | Notes |
| :--- | :--- | :--- | :--- |
| **Group Company** | GlobalTech Enterprises Holdings LLC | `GT00` | Group consolidation parent (`OX15`) |
| **Company Code** | GlobalTech Solutions USA Inc. | `1000` | Statutory legal entity (`OX02`, `USD`) |
| **Chart of Accounts** | GlobalTech Operational Chart of Accounts | `GTCA` | 6-digit account numbering (`OB13`) |
| **Fiscal Year** | Standard Calendar Year + 4 Special Periods | `K4` | Jan–Dec regular, 13–16 audit (`OB29`) |
| **Posting Period Var** | GlobalTech Posting Period Variant | `GT10` | Centralized closing control (`OBBO`) |
| **Field Status Var** | GlobalTech Field Status Variant | `GTFS` | G001, G004, G005, G067 groups (`OBC4`) |
| **Controlling Area** | GlobalTech Central Controlling Area | `1000` | 1:N Cross-Company Code (`OKKP`) |
| **Credit Control Area**| GlobalTech Credit Management Area | `GTCR` | Centralized exposure tracking (`OB45`) |

---

## 🧪 End-to-End Verification & Testing Lifecycle

A configuration is never complete until it successfully processes a full business cycle:

```
1. Capital Journal (FB50)        ==> Debit Cash (110000) / Credit Capital (200000)
2. Vendor Invoice (FB60)         ==> Debit Supplies (410000) / Credit Vendor Payable (210000)
3. Automated Payment Run (F110)  ==> Debit Vendor Payable / Credit Outgoing Bank Clearing
4. Customer Invoicing (FB70)     ==> Debit Customer Receivable (120000) / Credit Revenue (300000)
5. Incoming Cash Receipt (F-28)  ==> Debit Bank Clearing / Credit Customer Receivable
6. Monthly Asset Depr (AFAB)     ==> Debit Depreciation Expense (450000) / Credit Acc. Depr (150100)
7. Overhead Cost Assessment (KSU5)==> Allocate IT costs (1000-IT) to Production (1000-MFG)
8. Balance Sheet Audit (F.01)    ==> Validate: Total Assets == Total Liabilities + Equity
```

---

## ⚡ Master SPRO Configuration Cheat Sheet (Top 25 T-Codes)

| Step # | Configuration Step | Module | SPRO Navigation Path | T-Code |
| :---: | :--- | :---: | :--- | :---: |
| **01** | Define Company (Group) | FI | `Enterprise Structure > Definition > Financial Accounting > Define Company` | `OX15` |
| **02** | Define Company Code | FI | `Enterprise Structure > Definition > Financial Accounting > Edit Co. Code Data` | `OX02` |
| **03** | Assign Co. Code to Company | FI | `Enterprise Structure > Assignment > Financial Accounting > Assign Co. Code` | `OX16` |
| **04** | Maintain Fiscal Year Variant | FI | `Financial Accounting Global Settings > Ledgers > Fiscal Year > Maintain FYV` | `OB29` |
| **05** | Assign Co. Code to FYV | FI | `Financial Accounting Global Settings > Ledgers > Fiscal Year > Assign FYV` | `OB37` |
| **06** | Open & Close Posting Periods | FI | `Financial Accounting Global Settings > Ledgers > Posting Periods > Open/Close` | `OB52` |
| **07** | Define Field Status Variant | FI | `Financial Accounting Global Settings > Ledgers > Fields > Define FSV` | `OBC4` |
| **08** | Define Document Types & Ranges | FI | `Financial Accounting Global Settings > Document > Document Types / Number Ranges` | `OBA7 / FBN1` |
| **09** | Define Tolerance Groups | FI | `Financial Accounting Global Settings > Document > Line Item > Tolerances` | `OBA4` |
| **10** | Define Chart of Accounts | FI | `General Ledger Accounting > Master Data > G/L Accounts > Edit COA` | `OB13` |
| **11** | Define Retained Earnings Acct | FI | `General Ledger Accounting > Master Data > G/L Accounts > Retained Earnings` | `OB53` |
| **12** | Create G/L Master Records | FI | `Accounting > Financial Accounting > General Ledger > Master Records` | `FS00` |
| **13** | Vendor Account Groups & Ranges | FI-AP | `Accounts Payable > Vendor Accounts > Master Data > Groups / Ranges` | `OBD3 / XKN1` |
| **14** | Terms of Payment | FI-AP | `Accounts Payable > Business Transactions > Maintain Terms of Payment` | `OBB8` |
| **15** | Automatic Payment Program | FI-AP | `Accounts Payable > Business Transactions > Outgoing Payments > Auto Pmt` | `FBZP` |
| **16** | Customer Account Groups & Ranges| FI-AR | `Accounts Receivable > Customer Accounts > Master Data > Groups / Ranges` | `OBD2 / XDN1` |
| **17** | Dunning Procedures | FI-AR | `Accounts Receivable > Business Transactions > Dunning > Define Procedures` | `FBMP` |
| **18** | Copy Chart of Depreciation | FI-AA | `Asset Accounting > Organizational Structures > Copy Chart of Depr` | `EC08` |
| **19** | Define Asset Classes & Accts | FI-AA | `Asset Accounting > Organizational Structures > Asset Classes / Accounts` | `OAOA / AO90` |
| **20** | Maintain Controlling Area | CO | `Controlling > General Controlling > Organization > Maintain Area` | `OKKP` |
| **21** | Cost Center Hierarchy & Centers| CO-CCA| `Controlling > Cost Center Accounting > Master Data > Hierarchy / Create` | `OKEON / KS01`|
| **22** | Activity Types & Rates | CO-CCA| `Controlling > Cost Center Accounting > Master Data > Activity Types` | `KL01 / KP26` |
| **23** | Profit Center Standard Hierarchy| CO-PCA| `Controlling > Profit Center Accounting > Master Data > Standard Hierarchy` | `KCH1 / KE51` |
| **24** | FI-MM Account Determination | MM-FI | `Materials Management > Valuation and Account Assignment > Determination` | `OBYC` |
| **25** | FI-SD Revenue Determination | SD-FI | `Sales and Distribution > Basic Functions > Revenue Account Determination` | `VKOA` |

---

## 🛠️ Common Configuration Troubleshooting

| Error Code | Symptom & Cause | SPRO Navigation Fix | Fix T-Code |
| :--- | :--- | :--- | :--- |
| **F5 394** | Field status conflict between Field Status Group (`OBC4`) and Posting Key (`OB41`). | `Financial Accounting Global Settings > Ledgers > Fields > Define Field Status Variants` | `OBC4 / OB41` |
| **F5 286** | Posting period not open for month/year or account type (`+`, `S`, `K`, `D`). | `Financial Accounting Global Settings > Ledgers > Fiscal Year > Posting Periods > Open/Close` | `OB52` |
| **F5 150** | Document number range interval missing for active fiscal year. | `Financial Accounting Global Settings > Document > Number Ranges > Define Number Ranges` | `FBN1` |
| **M8 147** | Missing automatic account determination for transaction keys `BSX` or `WRX`. | `Materials Management > Valuation and Account Assignment > Account Determination` | `OBYC` |
| **KI 235** | Primary cost account posted without mandatory CO object assignment. | `Controlling > Cost Center Accounting > Actual Postings > Account Assignment` | `OKB9 / FS00` |
| **CVI_MAPPING** | Number range mismatch between Business Partner and Customer/Vendor. | `Cross-Application Components > Master Data Sync > Customer/Vendor Integration` | `MDS_LINKS` |

---

## 🎓 Internship Viva & Interview Q&A (Top 5 Questions)

### Q1: What is the difference between a Company and a Company Code in SAP?
> **Answer:** A **Company Code (`OX02`)** is the primary legal entity for which statutory financial statements (Balance Sheet, P&L) are drawn up for external tax and legal compliance. A **Company (`OX15`)** is a corporate consolidation unit under which multiple subsidiary Company Codes roll up for consolidated group reporting.

### Q2: Why is the Universal Journal (`ACDOCA`) in S/4HANA considered a revolution compared to ECC 6.0?
> **Answer:** In ECC 6.0, financial data was fragmented across multiple tables (`BKPF`/`BSEG` for FI, `COEP` for CO, `ANEP` for Assets, `FAGLFLEXA` for New G/L), requiring complex month-end reconciliation. S/4HANA merges all FI and CO dimensions into a single line-item table (`ACDOCA`), ensuring an instant single source of truth without reconciliation.

### Q3: What happens in transaction `FBZP`?
> **Answer:** `FBZP` is the central configuration cockpit for the Automatic Payment Program (`F110`). It configures 6 key settings: All Company Codes, Paying Company Codes, Payment Methods in Country, Payment Methods in Company Code, Bank Determination, and House Banks.

### Q4: Why can't you post directly to a Reconciliation Account via `FB50`?
> **Answer:** Reconciliation accounts (Customer AR `120000`, Vendor AP `210000`) maintain strict sub-ledger integrity. All postings must flow through customer (`FB70`) or vendor (`FB60`) transactions so the subsidiary ledger and general ledger remain permanently in balance.

### Q5: What is the role of transaction `OBYC`?
> **Answer:** `OBYC` is the automatic account determination engine connecting SAP MM and SAP FI. When goods are received (`MIGO`), `OBYC` uses the Material's Valuation Class and Transaction Keys (such as `BSX` for Inventory and `WRX` for GR/IR Clearing) to post financial accounting documents automatically.

---

## 🚀 How to Run the Document Generator

To re-generate the primary DOCX deliverable:
```powershell
# Using the pre-configured Python virtual environment:
& "..\SAP-FICO-Internship-Task-1\.venv\Scripts\python.exe" build_doc.py
```

### Repository Structure
```text
SAP-FICO-Internship-Task-2/
├── SAP_FICO_Configuration_Guide.docx  # Primary Word Document deliverable (58 KB)
├── SAP_FICO_Configuration_Guide.md    # Complete Markdown reference manual
├── README.md                           # GitHub documentation, roadmap & viva guide
├── build_doc.py                        # Automated python-docx document builder
└── .gitignore                          # Clean repository exclusions
```

---
*Created by **Laxmi Gupta** | SAP Consulting / ERP Internship Deliverable — Week 2*
