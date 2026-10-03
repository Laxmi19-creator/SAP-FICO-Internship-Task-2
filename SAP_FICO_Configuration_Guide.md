# SAP FICO Configuration Guide: Complete Step-by-Step Implementation Manual

**Document Type:** Industrial Technical Manual & Functional Configuration Blueprint  
**Subject:** Enterprise Resource Planning (ERP) — Financial Accounting (FI) & Controlling (CO) Configuration  
**Author:** Laxmi Gupta  
**Role:** SAP Consulting / ERP Intern  
**Project:** Week 2 Internship Deliverable — Deep-Dive SAP FICO Configuration  
**Date:** October 2026  
**System Scope:** SAP ERP ECC 6.0 EHP8 & SAP S/4HANA 2023  
**Status:** Complete, Validated & Audit-Ready  

---

## Executive Summary

Configuring an Enterprise Resource Planning (ERP) platform like SAP is fundamentally distinct from using it as an operational end-user. While end-users perform daily transactional entries (such as raising purchase orders, posting vendor bills, or executing bank payments), an **SAP Functional Consultant** designs and configures the foundational architecture that determines **how** the system behaves, calculates, enforces internal controls, and reports financial numbers.

This configuration guide provides an end-to-end, beginner-accessible, and technically rigorous roadmap for configuring **SAP FICO (Financial Accounting & Controlling)** from a clean client ("greenfield implementation") to a fully functioning, audit-compliant financial accounting system.

Every configuration phase in this manual details:
1. **The Conceptual Mental Model:** Why this step is required in simple, relatable business terms.
2. **Standard SPRO Breadcrumb Paths:** Exact navigation across the SAP Implementation Guide (IMG).
3. **Transaction Codes (T-Codes):** Fast-path execution shortcuts.
4. **Concrete Baseline Blueprint Values:** Using a running real-world enterprise example—**GlobalTech Enterprises Inc. (Company Code `1000`)**.
5. **Architectural "Under the Hood" Mechanics:** Database table updates, field status behaviors, and downstream integration dependencies.
6. **SAP S/4HANA Modernizations:** Key shifts from legacy ECC (e.g., the Universal Journal `ACDOCA`, Business Partner `BP` synchronization, New Asset Accounting, and unified Cost Element G/L accounts).
7. **End-to-End Verification Scenarios & Troubleshooting:** Practical test scripts and fixes for common real-world configuration errors.

---

## Table of Contents

- [1. Foundational Architecture & The Consultant's Mindset](#1-foundational-architecture--the-consultants-mindset)
  - [1.1 Configuration (Customizing) vs. Master Data vs. Transactional Postings](#11-configuration-customizing-vs-master-data-vs-transactional-postings)
  - [1.2 The Three-Tier System Landscape & Transport Management](#12-the-three-tier-system-landscape--transport-management)
  - [1.3 Understanding SPRO, the Implementation Guide (IMG), and Transport Requests](#13-understanding-spro-the-implementation-guide-img-and-transport-requests)
  - [1.4 The Running Enterprise Blueprint: GlobalTech Enterprises](#14-the-running-enterprise-blueprint-globaltech-enterprises)
- [2. Phase 1 — Enterprise Structure Configuration (The Organizational Skeleton)](#2-phase-1--enterprise-structure-configuration-the-organizational-skeleton)
  - [2.1 Step 1: Define Company (Consolidation Unit / Group) — OX15](#21-step-1-define-company-consolidation-unit--group--ox15)
  - [2.2 Step 2: Define Company Code (Statutory Legal Entity) — OX02](#22-step-2-define-company-code-statutory-legal-entity--ox02)
  - [2.3 Step 3: Assign Company Code to Company — OX16](#23-step-3-assign-company-code-to-company--ox16)
  - [2.4 Step 4: Define Business Area (Segmental Reporting) — OX03](#24-step-4-define-business-area-segmental-reporting--ox03)
  - [2.5 Step 5: Define Functional Area (Cost of Sales Accounting) — OKBD / FM_FUNCTION](#25-step-5-define-functional-area-cost-of-sales-accounting--okbd--fm_function)
  - [2.6 Step 6: Define Credit Control Area & Assign to Company Code — OB45 & OB38](#26-step-6-define-credit-control-area--assign-to-company-code--ob45--ob38)
- [3. Phase 2 — Financial Accounting Global Settings (Operational Rules & Controls)](#3-phase-2--financial-accounting-global-settings-operational-rules--controls)
  - [3.1 Step 7: Maintain Fiscal Year Variant (FYV) — OB29](#31-step-7-maintain-fiscal-year-variant-fyv--ob29)
  - [3.2 Step 8: Assign Company Code to Fiscal Year Variant — OB37](#32-step-8-assign-company-code-to-fiscal-year-variant--ob37)
  - [3.3 Step 9: Define Posting Period Variant (PPV) — OBBO](#33-step-9-define-posting-period-variant-ppv--obbo)
  - [3.4 Step 10: Assign Posting Period Variant to Company Code — OBBP](#34-step-10-assign-posting-period-variant-to-company-code--obbp)
  - [3.5 Step 11: Open and Close Posting Periods — OB52](#35-step-11-open-and-close-posting-periods--ob52)
  - [3.6 Step 12: Define Field Status Variant (FSV) & Field Status Groups — OBC4](#36-step-12-define-field-status-variant-fsv--field-status-groups--obc4)
  - [3.7 Step 13: Assign Company Code to Field Status Variant — OBC5](#37-step-13-assign-company-code-to-field-status-variant--obc5)
  - [3.8 Step 14: Define Document Types & Number Ranges — OBA7 & FBN1](#38-step-14-define-document-types--number-ranges--oba7--fbn1)
  - [3.9 Step 15: Define Tolerance Groups for Employees & G/L Accounts — OBA4 & OBA0](#39-step-15-define-tolerance-groups-for-employees--gl-accounts--oba4--oba0)
- [4. Phase 3 — General Ledger Accounting (FI-GL) Configuration](#4-phase-3--general-ledger-accounting-fi-gl-configuration)
  - [4.1 Step 16: Define Chart of Accounts (COA) — OB13](#41-step-16-define-chart-of-accounts-coa--ob13)
  - [4.2 Step 17: Assign Company Code to Chart of Accounts — OB62](#42-step-17-assign-company-code-to-chart-of-accounts--ob62)
  - [4.3 Step 18: Define Account Groups & Field Status for G/L Accounts — OBD4](#43-step-18-define-account-groups--field-status-for-gl-accounts--obd4)
  - [4.4 Step 19: Define Retained Earnings Account — OB53](#44-step-19-define-retained-earnings-account--ob53)
  - [4.5 Step 20: Creation of Master G/L Accounts & S/4HANA Account Types — FS00](#45-step-20-creation-of-master-gl-accounts--s4hana-account-types--fs00)
- [5. Phase 4 — Accounts Payable (FI-AP) & Procure-to-Pay (P2P) Configuration](#5-phase-4--accounts-payable-fi-ap--procure-to-pay-p2p-configuration)
  - [5.1 Step 21: Define Vendor Account Groups — OBD3](#51-step-21-define-vendor-account-groups--obd3)
  - [5.2 Step 22: Create Number Ranges for Vendor Accounts — XKN1](#52-step-22-create-number-ranges-for-vendor-accounts--xkn1)
  - [5.3 Step 23: Assign Number Ranges to Vendor Account Groups — OBAS](#53-step-23-assign-number-ranges-to-vendor-account-groups--obas)
  - [5.4 Step 24: Define Tolerance Groups for Vendors — OBA3](#54-step-24-define-tolerance-groups-for-vendors--oba3)
  - [5.5 Step 25: Create Vendor Reconciliation G/L Accounts — FS00](#55-step-25-create-vendor-reconciliation-gl-accounts--fs00)
  - [5.6 Step 26: S/4HANA Business Partner (BP) & Customer-Vendor Integration (CVI) — BP](#56-step-26-s4hana-business-partner-bp--customer-vendor-integration-cvi--bp)
  - [5.7 Step 27: Define Terms of Payment — OBB8](#57-step-27-define-terms-of-payment--obb8)
  - [5.8 Step 28: Configure the Automatic Payment Program (APP) — FBZP](#58-step-28-configure-the-automatic-payment-program-app--fbzp)
- [6. Phase 5 — Accounts Receivable (FI-AR) & Order-to-Cash (O2C) Configuration](#6-phase-5--accounts-receivable-fi-ar--order-to-cash-o2c-configuration)
  - [6.1 Step 29: Define Customer Account Groups — OBD2](#61-step-29-define-customer-account-groups--obd2)
  - [6.2 Step 30: Create Customer Number Ranges & Assign — XDN1 & OBAR](#62-step-30-create-customer-number-ranges--assign--xdn1--obar)
  - [6.3 Step 31: Create Customer Reconciliation G/L Accounts — FS00](#63-step-31-create-customer-reconciliation-gl-accounts--fs00)
  - [6.4 Step 32: S/4HANA Customer BP Roles — FLCU00 & FLCU01](#64-step-32-s4hana-customer-bp-roles--flcu00--flcu01)
  - [6.5 Step 33: Configure Dunning Procedure — FBMP](#65-step-33-configure-dunning-procedure--fbmp)
  - [6.6 Step 34: Configure Customer Credit Management](#66-step-34-configure-customer-credit-management)
- [7. Phase 6 — Asset Accounting (FI-AA) Configuration](#7-phase-6--asset-accounting-fi-aa-configuration)
  - [7.1 Step 35: Copy Reference Chart of Depreciation — EC08](#71-step-35-copy-reference-chart-of-depreciation--ec08)
  - [7.2 Step 36: Assign Chart of Depreciation to Company Code — OAOB](#72-step-36-assign-chart-of-depreciation-to-company-code--oaob)
  - [7.3 Step 37: Specify Account Determination Keys & Screen Layout Rules — AO25 & OA77](#73-step-37-specify-account-determination-keys--screen-layout-rules--ao25--oa77)
  - [7.4 Step 38: Define Number Range Intervals for Asset Classes — AS08](#74-step-38-define-number-range-intervals-for-asset-classes--as08)
  - [7.5 Step 39: Define Asset Classes — OAOA](#75-step-39-define-asset-classes--oaoa)
  - [7.6 Step 40: Assign G/L Accounts for Automatic Depreciation Postings — AO90](#76-step-40-assign-gl-accounts-for-automatic-depreciation-postings--ao90)
  - [7.7 Step 41: Define Depreciation Keys & Calculation Methods — AFAMA & AFAMS](#77-step-41-define-depreciation-keys--calculation-methods--afama--afams)
  - [7.8 Step 42: S/4HANA Technical Clearing Account for Asset Acquisition](#78-step-42-s4hana-technical-clearing-account-for-asset-acquisition)
- [8. Phase 7 — Controlling (CO) Enterprise & Basic Configuration](#8-phase-7--controlling-co-enterprise--basic-configuration)
  - [8.1 Step 43: Maintain Controlling Area — OKKP](#81-step-43-maintain-controlling-area--okkp)
  - [8.2 Step 44: Assign Company Code to Controlling Area — OX19 / OKKP](#82-step-44-assign-company-code-to-controlling-area--ox19--okkp)
  - [8.3 Step 45: Maintain Number Ranges for Controlling Documents — KANK](#83-step-45-maintain-number-ranges-for-controlling-documents--kank)
  - [8.4 Step 46: Maintain Controlling Versions (Plan/Actual Version 0) — OKEQ / OKEV](#84-step-46-maintain-controlling-versions-planactual-version-0--okeq--okev)
- [9. Phase 8 — Cost Center Accounting (CO-CCA) & Cost Element Configuration](#9-phase-8--cost-center-accounting-co-cca--cost-element-configuration)
  - [9.1 Step 47: Activate Cost Center Accounting in Controlling Area — OKKP](#91-step-47-activate-cost-center-accounting-in-controlling-area--okkp)
  - [9.2 Step 48: Define Standard Hierarchy for Cost Centers — OKEON](#92-step-48-define-standard-hierarchy-for-cost-centers--okeon)
  - [9.3 Step 49: Create Cost Center Categories — OKA2](#93-step-49-create-cost-center-categories--oka2)
  - [9.4 Step 50: Create Master Cost Centers — KS01 / KS02](#94-step-50-create-master-cost-centers--ks01--ks02)
  - [9.5 Step 51: Cost Elements Architecture: ECC KA01/KA06 vs S/4HANA FS00](#95-step-51-cost-elements-architecture-ecc-ka01ka06-vs-s4hana-fs00)
  - [9.6 Step 52: Define Activity Types & Activity Price Planning — KL01 & KP26](#96-step-52-define-activity-types--activity-price-planning--kl01--kp26)
  - [9.7 Step 53: Define Statistical Key Figures (SKF) — KK01](#97-step-53-define-statistical-key-figures-skf--kk01)
  - [9.8 Step 54: Configure Cost Allocations: Distribution vs. Assessment — KSV1 / KSU1](#98-step-54-configure-cost-allocations-distribution-vs-assessment--ksv1--ksu1)
- [10. Phase 9 — Internal Orders (CO-IO) & Profit Center Accounting (CO-PCA)](#10-phase-9--internal-orders-co-io--profit-center-accounting-co-pca)
  - [10.1 Step 55: Define Order Types for Internal Orders — KOT2_OPA](#101-step-55-define-order-types-for-internal-orders--kot2_opa)
  - [10.2 Step 56: Define Settlement Profiles & Allocation Structures — OKO7](#102-step-56-define-settlement-profiles--allocation-structures--oko7)
  - [10.3 Step 57: Maintain Profit Center Standard Hierarchy & Dummy Profit Center — KCH1 & KE59](#103-step-57-maintain-profit-center-standard-hierarchy--dummy-profit-center--kch1--ke59)
  - [10.4 Step 58: Create Profit Centers — KE51](#104-step-58-create-profit-centers--ke51)
  - [10.5 Step 59: Set Control Parameters for Profit Center Accounting — 0KE5 / 1KEF](#105-step-59-set-control-parameters-for-profit-center-accounting--0ke5--1kef)
- [11. Phase 10 — Cross-Module Integration Configuration (MM-FI & SD-FI)](#11-phase-10--cross-module-integration-configuration-mm-fi--sd-fi)
  - [11.1 Step 60: FI-MM Integration (OBYC Automatic Account Determination)](#111-step-60-fi-mm-integration-obyc-automatic-account-determination)
  - [11.2 Step 61: FI-SD Integration (VKOA Revenue Account Determination)](#112-step-61-fi-sd-integration-vkoa-revenue-account-determination)
- [12. Phase 11 — End-to-End Configuration Verification & Testing Checklist](#12-phase-11--end-to-end-configuration-verification--testing-checklist)
  - [12.1 Unit & Integration Testing Strategy](#121-unit--integration-testing-strategy)
  - [12.2 Test Script 1: General Ledger Direct Journal Entry — FB50](#122-test-script-1-general-ledger-direct-journal-entry--fb50)
  - [12.3 Test Script 2: Procure-to-Pay (P2P) Vendor Invoice & Payment — FB60 & F110](#123-test-script-2-procure-to-pay-p2p-vendor-invoice--payment--fb60--f110)
  - [12.4 Test Script 3: Order-to-Cash (O2C) Customer Invoice & Clearing — FB70 & F-28](#124-test-script-3-order-to-cash-o2c-customer-invoice--clearing--fb70--f-28)
  - [12.5 Test Script 4: Asset Acquisition & Depreciation Run — F-90 & AFAB](#125-test-script-4-asset-acquisition--depreciation-run--f-90--afab)
  - [12.6 Test Script 5: Controlling Overhead Assessment Run — KSU5](#126-test-script-5-controlling-overhead-assessment-run--ksu5)
  - [12.7 Test Script 6: Financial Balance Sheet & P&L Generation — F.01](#127-test-script-6-financial-balance-sheet--pl-generation--f01)
- [13. Phase 12 — Troubleshooting Guide: Common Configuration Errors & Solutions](#13-phase-12--troubleshooting-guide-common-configuration-errors--solutions)
- [14. Phase 13 — Master Configuration Reference Matrix & SPRO Cheat Sheet](#14-phase-13--master-configuration-reference-matrix--spro-cheat-sheet)
- [15. Conclusion & Professional Recommendations](#15-conclusion--professional-recommendations)

---

## 1. Foundational Architecture & The Consultant's Mindset

### 1.1 Configuration (Customizing) vs. Master Data vs. Transactional Postings

For a beginner stepping into the world of SAP consulting, distinguishing between three operational tiers is the single most critical breakthrough:

```
+-------------------------------------------------------------------------+
|                           TIER 1: CONFIGURATION                         |
|  * Performed by: SAP Functional Consultants                             |
|  * Environment: Development (DEV) Golden Client                         |
|  * Tools: SPRO / IMG / Transaction Codes                                 |
|  * Output: Transport Requests (TRs) moved across landscape              |
|  * Examples: Defining Company Code 1000, Chart of Accounts, Document Types|
+------------------------------------+------------------------------------+
                                     | Defines the rules and boundaries for
                                     v
+-------------------------------------------------------------------------+
|                           TIER 2: MASTER DATA                           |
|  * Performed by: Key Users / Power Users / Master Data Teams            |
|  * Environment: Created in PRD (or uploaded via LTMC / LSMW)           |
|  * Examples: G/L Accounts (FS00), Vendors/Customers (BP), Cost Centers  |
|  * Characteristic: Persistent, long-term records referenced repeatedly  |
+------------------------------------+------------------------------------+
                                     | Serves as the operational actors in
                                     v
+-------------------------------------------------------------------------+
|                        TIER 3: TRANSACTIONAL DATA                       |
|  * Performed by: Operational End-Users (Accounts Payable clerk, etc.)    |
|  * Environment: Production (PRD) live environment only                  |
|  * Examples: Posting an invoice (FB60), Running payments (F110)         |
|  * Characteristic: High volume, day-to-day business documents           |
+-------------------------------------------------------------------------+
```

* **Configuration (Customizing):** You are building the physical game board and establishing the rules of chess. If a rule says "documents must balance before posting," the system rejects unbalanced entries.
* **Master Data:** You are placing the game pieces on the board (e.g., creating specific accounts, vendors, and cost centers).
* **Transactional Data:** The actual moves made during the game (e.g., invoices, payments, transfers).

### 1.2 The Three-Tier System Landscape & Transport Management

In corporate enterprise environments, configuration is **never** executed directly in the live production system. SAP mandates a structured three-tier landscape:

```
   [ DEV: Development ]  ======== Transport Request =======>  [ QAS: Quality Assurance ]
   - 100: Sandbox / R&D                                       - 200: Integration Testing
   - 110: Golden Customizing                                  - 210: User Acceptance (UAT)
   - 120: Unit Testing                                        - Regression & Performance
            |                                                               |
            +===================== Production Release =====================>+
                                                                            |
                                                                            v
                                                                   [ PRD: Production ]
                                                                   - 300: Real Business
                                                                   - Strictly Read-Only Customizing
```

1. **Development System (DEV):** Consultants write configurations in Client 110 (Golden Client) where no transactional data exists. All changes are recorded on **Transport Requests (TRs)**.
2. **Quality Assurance System (QAS):** Configurations are transported to QAS where business testers, end-users, and audit teams validate integration and run User Acceptance Testing (UAT).
3. **Production System (PRD):** Once approved and signed off, transports are imported into PRD during scheduled maintenance windows. In PRD, configuration menus are locked (`Client non-modifiable`).

### 1.3 Understanding SPRO, the Implementation Guide (IMG), and Transport Requests

* **SPRO (SAP Project Reference Object):** The master command entered into the SAP Easy Access command bar to enter the Customizing screen.
* **IMG (Implementation Guide):** The hierarchical tree structure dividing every module, sub-module, and organizational parameter into progressive, logical steps.
* **Transport Request Types:**
  * **Customizing Request:** Contains client-dependent system setup (e.g., Company Code, Fiscal Year, Payment Terms).
  * **Workbench Request:** Contains cross-client technical development (e.g., ABAP programs, DDIC tables, custom smartforms).
  * **Transport Organizer (`SE09` / `SE10`):** The workbench used to view, document, release, and audit transport requests.

### 1.4 The Running Enterprise Blueprint: GlobalTech Enterprises

To make this manual immediately practical and cohesive, all 61 configuration steps follow a continuous, realistic business blueprint:

| Blueprint Parameter | Entity Description | Configured Value in SAP |
| :--- | :--- | :--- |
| **Enterprise Group** | GlobalTech Enterprises Holdings LLC | `GT00` (Company) |
| **Legal Company Code** | GlobalTech Solutions USA Inc. | `1000` (Company Code) |
| **Country & Currency** | United States / US Dollar | Country: `US`, Currency: `USD` |
| **Chart of Accounts** | GlobalTech Operational Chart of Accounts | `GTCA` |
| **Fiscal Year** | Standard Calendar Year (Jan–Dec) + 4 Special | `K4` |
| **Posting Period Variant**| GlobalTech Posting Period Variant | `GT10` |
| **Field Status Variant** | GlobalTech Field Status Variant | `GTFS` |
| **Controlling Area** | GlobalTech Controlling Area (1:N cross-company) | `1000` |
| **Credit Control Area** | GlobalTech Credit Management Area | `GTCR` |

---

## 2. Phase 1 — Enterprise Structure Configuration (The Organizational Skeleton)

```
                            +---------------------------------+
                            |         Company: GT00           |
                            |   (GlobalTech Holdings LLC)     |
                            +----------------+----------------+
                                             |
                                             v  [Assignment: OX16]
                            +----------------+----------------+
                            |       Company Code: 1000        |
                            | (GlobalTech Solutions USA Inc.) |
                            +--------+---------------+--------+
                                     |               |
                   +-----------------+               +-----------------+
                   |                                                   |
                   v                                                   v
     +---------------------------+                       +---------------------------+
     |   Credit Control: GTCR    |                       |   Controlling Area: 1000  |
     |   (Assignment: OB38)      |                       |   (Assignment: OX19)      |
     +---------------------------+                       +---------------------------+
```

### 2.1 Step 1: Define Company (Consolidation Unit / Group) — OX15

* **What it is:** The highest grouping level in SAP Financial Accounting. It represents the corporate parent entity or holding group under which multiple subsidiary legal entities consolidate.
* **Why it is needed:** Multi-company enterprises require group-level financial balance sheets to satisfy SEC, IFRS 10, or statutory group consolidation.
* **SPRO Menu Path:** `SPRO > Enterprise Structure > Definition > Financial Accounting > Define Company`
* **Transaction Code:** `OX15`
* **Database Table Updated:** `T080` (Company Master)
* **Configuration Parameters:**
  * **Company:** `GT00`
  * **Company Name:** GlobalTech Enterprises Holdings LLC
  * **Street / P.O. Box:** 100 Innovation Boulevard
  * **Postal Code / City:** 10001, New York
  * **Country:** `US`
  * **Language Key:** `EN`
  * **Currency:** `USD`
* **Consultant Best Practice:** A Company code is 4 characters alphanumeric; a Company can be up to 6 characters alphanumeric. Always define the Group Company first before creating legal entities.

### 2.2 Step 2: Define Company Code (Statutory Legal Entity) — OX02

* **What it is:** The smallest organizational unit for which an independent, legally self-contained set of financial accounts (Balance Sheet, P&L) can be drawn up for statutory external audit.
* **Why it is needed:** Every country or legally registered commercial entity must have its own Company Code to satisfy tax authorities, local statutory corporate filings, and commercial legal compliance.
* **SPRO Menu Path:** `SPRO > Enterprise Structure > Definition > Financial Accounting > Edit, Copy, Delete, Check Company Code > Edit Company Code Data`
* **Transaction Code:** `OX02`
* **Database Table Updated:** `T001` (Company Codes Master Table)
* **Configuration Parameters:**
  * **Company Code:** `1000`
  * **Company Name:** GlobalTech Solutions USA Inc.
  * **City:** New York
  * **Country:** `US`
  * **Currency:** `USD`
  * **Language:** `EN`
* **Deep-Dive Address Screen:** Click the "Address" icon (Shift+F5) to maintain the exact legal corporate address, Tax Identification Number (EIN/TIN), and state jurisdictions.

### 2.3 Step 3: Assign Company Code to Company — OX16

* **What it is:** Creates the structural parent-child link tying legal subsidiary `1000` to corporate group `GT00`.
* **Why it is needed:** Without this assignment, intercompany postings cannot identify the corporate relationship, and intercompany elimination cannot occur during group financial consolidation.
* **SPRO Menu Path:** `SPRO > Enterprise Structure > Assignment > Financial Accounting > Assign company code to company`
* **Transaction Code:** `OX16`
* **Database Table Updated:** `T001` (Field `T001-RCOMP` populated with `GT00`)
* **Execution:** Locate Company Code `1000` in the list, input `GT00` in the "Company" column, and click Save into your Customizing TR.

### 2.4 Step 4: Define Business Area (Segmental Reporting) — OX03

* **What it is:** A cross-company organizational segment representing a specific product line, operations division, or geographic branch.
* **Why it is needed:** For internal management reporting across multiple company codes (e.g., North American Software Services vs. Hardware Manufacturing) without having to build multiple separate legal entities.
* **SPRO Menu Path:** `SPRO > Enterprise Structure > Definition > Financial Accounting > Define Business Area`
* **Transaction Code:** `OX03`
* **Database Table Updated:** `TGSB` (Business Areas)
* **Configuration Parameters:**
  * `GTCS`: GlobalTech Cloud Software Division
  * `GTHW`: GlobalTech Hardware & Infrastructure Division
* **Note on S/4HANA:** In SAP S/4HANA, **Profit Center Accounting** and **Segment Reporting** (driven by Document Splitting) have largely superseded Business Areas for IFRS 8 / GAAP segment reporting, but Business Areas remain supported.

### 2.5 Step 5: Define Functional Area (Cost of Sales Accounting) — OKBD / FM_FUNCTION

* **What it is:** Categorizes expenses by operational function (e.g., Administration, Sales & Distribution, Research & Development, Manufacturing Production).
* **Why it is needed:** Enables Cost of Sales Accounting (reporting P&L by function rather than period cost nature).
* **SPRO Menu Path:** `SPRO > Enterprise Structure > Definition > Financial Accounting > Define Functional Area`
* **Transaction Code:** `OKBD` (or `FM_FUNCTION`)
* **Database Table Updated:** `TFKB` (Functional Areas)
* **Configuration Entries:**
  * `1000`: Manufacturing / Production
  * `2000`: Administration & Executive Overheads
  * `3000`: Sales, Marketing & Distribution
  * `4000`: Research & Development (R&D)

### 2.6 Step 6: Define Credit Control Area & Assign to Company Code — OB45 & OB38

* **What it is:** An organizational unit that specifies, manages, and enforces customer credit limits across one or more company codes.
* **Why it is needed:** To prevent sales representatives from shipping orders to high-risk or bankrupt customers who exceed their authorized credit threshold.
* **SPRO Menu Path (Definition):** `SPRO > Enterprise Structure > Definition > Financial Accounting > Define Credit Control Area` (`OB45`)
* **SPRO Menu Path (Assignment):** `SPRO > Enterprise Structure > Assignment > Financial Accounting > Assign company code to credit control area` (`OB38`)
* **Database Table Updated:** `T014` (Credit Control Areas) and `T001-KKBER`
* **Configuration Parameters:**
  * **Credit Control Area:** `GTCR`
  * **Currency:** `USD`
  * **Update Key:** `000012` (Open orders, deliveries, and billing documents all reduce available credit).

---

## 3. Phase 2 — Financial Accounting Global Settings (Operational Rules & Controls)

Once the organizational skeleton is formed, you must define the operational calendars, document controls, and validation limits that govern daily bookkeeping.

### 3.1 Step 7: Maintain Fiscal Year Variant (FYV) — OB29

* **What it is:** Defines the financial year cycle: the number of normal posting periods (months) and special closing periods used for audit adjustments.
* **Why it is needed:** Companies have varying financial calendars. For example, US entities frequently run January–December (Calendar Year), while Indian or UK entities run April–March.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Maintain Fiscal Year Variant`
* **Transaction Code:** `OB29`
* **Database Table Updated:** `T009`, `T009B`
* **Key Variants in SAP:**
  * `K4`: Calendar Year (12 Posting Periods Jan–Dec + 4 Special Periods for Year-End Audits).
  * `V3`: Non-Calendar Year (April–March: 12 Posting Periods + 4 Special Periods).
* **Configuration for GlobalTech:** Select `K4`. Check "Calendar Year" flag; Number of posting periods = `12`, Number of special periods = `4`.
* **Beginner's Insight — What are Special Periods?** Periods 13, 14, 15, and 16 allow auditors and chief accountants to post post-closing tax audit adjustments in February/March of the next year without corrupting the finalized December month-end balance.

### 3.2 Step 8: Assign Company Code to Fiscal Year Variant — OB37

* **What it is:** Tells Company Code `1000` which accounting calendar to follow.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Assign Company Code to a Fiscal Year Variant`
* **Transaction Code:** `OB37`
* **Database Table Updated:** `T001-PERIV`
* **Execution:** Map Company Code `1000` -> Fiscal Year Variant `K4`.

### 3.3 Step 9: Define Posting Period Variant (PPV) — OBBO

* **What it is:** An operational token that groups company codes together for open/closed accounting period management.
* **Why it is needed:** Multiple company codes can share one PPV so that when a corporate controller closes Month 05 at corporate headquarters, Month 05 closes across all 20 subsidiaries at once.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Define Variants for Open Posting Periods`
* **Transaction Code:** `OBBO`
* **Database Table Updated:** `T010O` (Posting Period Variants)
* **Configuration Parameters:**
  * **Variant:** `GT10`
  * **Name:** GlobalTech Posting Period Variant

### 3.4 Step 10: Assign Posting Period Variant to Company Code — OBBP

* **What it is:** Binds Variant `GT10` directly to Company Code `1000`.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Assign Variants to Company Code`
* **Transaction Code:** `OBBP`
* **Database Table Updated:** `T001-OPVAR`
* **Execution:** Locate Company Code `1000` -> Enter `GT10` -> Save.

### 3.5 Step 11: Open and Close Posting Periods — OB52

* **What it is:** The control panel that specifies which months and which account types are allowed to receive financial postings.
* **Why it is needed:** To prevent accidental postings into already audited past months or unapproved future periods.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Open and Close Posting Periods`
* **Transaction Code:** `OB52`
* **Database Table Updated:** `T001B` (Posting Period Control Table)
* **Account Type Keys Explained:**
  * `+`: Valid for all account types (Header level control gate).
  * `A`: Assets sub-ledger.
  * `D`: Customers (Debtors) sub-ledger.
  * `K`: Vendors (Creditors) sub-ledger.
  * `M`: Materials sub-ledger.
  * `S`: General Ledger accounts.
* **Recommended Baseline Configuration Table:**

| Var | Account Type | From Account | To Account | From Period 1 | Year 1 | To Period 1 | Year 1 | From Period 2 | Year 2 | To Period 2 | Year 2 | Authorization Group |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `GT10`| `+` | | | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |
| `GT10`| `A` | | `ZZZZZZZZZZ` | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |
| `GT10`| `D` | | `ZZZZZZZZZZ` | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |
| `GT10`| `K` | | `ZZZZZZZZZZ` | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |
| `GT10`| `M` | | `ZZZZZZZZZZ` | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |
| `GT10`| `S` | | `ZZZZZZZZZZ` | 1 | 2026 | 12 | 2026 | 13 | 2026 | 16 | 2026 | |

### 3.6 Step 12: Define Field Status Variant (FSV) & Field Status Groups — OBC4

* **What it is:** Controls field visibility behavior on journal entry screens (whether a field is **Suppress / Hidden**, **Required / Mandatory**, or **Optional**).
* **Why it is needed:** When posting an electricity expense, entering a "Cost Center" is legally and operationally mandatory. When posting a bank cash transfer, a "Cost Center" is completely irrelevant and must be suppressed to avoid confusing the clerk.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fields > Define Field Status Variants`
* **Transaction Code:** `OBC4`
* **Database Table Updated:** `T004V`, `T004F`
* **Consultant Best Practice:** Never create a Field Status Variant from scratch! Copy standard SAP template variant `0001` to `GTFS` (GlobalTech Field Status Variant) to ensure all sub-screen assignments copy correctly.
* **Core Field Status Groups (FSG):**
  * `G001`: General with text (standard G/L postings).
  * `G004`: Cost accounts (Cost center mandatory).
  * `G005`: Bank accounts (Value date mandatory).
  * `G029`: Revenue accounts (Profit center mandatory).
  * `G067`: Reconciliation accounts (Customer/Vendor sub-ledger).

### 3.7 Step 13: Assign Company Code to Field Status Variant — OBC5

* **What it is:** Activates Field Status Variant `GTFS` for Company Code `1000`.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Ledgers > Fields > Assign Company Code to Field Status Variants`
* **Transaction Code:** `OBC5`
* **Database Table Updated:** `T001-FIKRS`
* **Execution:** Match `1000` -> `GTFS` -> Save.

### 3.8 Step 14: Define Document Types & Number Ranges — OBA7 & FBN1

* **What it is:** Document Types (2-character codes) classify financial transactions and dictate which account types can be posted, which number range interval is consumed, and whether the transaction is an invoice, credit memo, or payment.
* **Why it is needed:** Legal audit trails require strict chronological and gapless sequential numbering of financial documents.
* **SPRO Menu Path (Document Types):** `SPRO > Financial Accounting > Financial Accounting Global Settings > Document > Document Types > Define Document Types` (`OBA7`)
* **SPRO Menu Path (Number Ranges):** `SPRO > Financial Accounting > Financial Accounting Global Settings > Document > Document Number Ranges > Define Document Number Ranges` (`FBN1`)
* **Standard Document Types Matrix:**

| Doc Type | Description | Number Range Key | Account Types Allowed | Reverse Doc Type |
| :--- | :--- | :--- | :--- | :--- |
| `SA` | G/L Account Journal Entry | `01` | G/L (`S`) | `AB` |
| `KR` | Vendor Invoice | `19` | Vendor (`K`), G/L (`S`) | `AB` |
| `KG` | Vendor Credit Memo | `17` | Vendor (`K`), G/L (`S`) | `AB` |
| `KZ` | Vendor Payment | `15` | Vendor (`K`), G/L (`S`) | `AB` |
| `DR` | Customer Invoice | `18` | Customer (`D`), G/L (`S`)| `AB` |
| `DG` | Customer Credit Memo | `16` | Customer (`D`), G/L (`S`)| `AB` |
| `DZ` | Customer Payment | `14` | Customer (`D`), G/L (`S`)| `AB` |
| `AA` | Asset Posting | `01` | Asset (`A`), G/L (`S`) | `AB` |

* **Step in FBN1:** For Company Code `1000`, add Year `2026`, define interval `01` (`0100000000` to `0199999999`), and leave "External" checkbox **blank** for internal system auto-numbering.

### 3.9 Step 15: Define Tolerance Groups for Employees & G/L Accounts — OBA4 & OBA0

* **What it is:** Sets maximum financial thresholds that individual users can post in a single transaction (e.g., maximum dollar amount per document, maximum amount per line item, and permitted payment cash discount variances).
* **Why it is needed:** An essential internal anti-fraud and financial control mechanism preventing junior clerks from accidentally or maliciously posting a $100,000,000 journal entry.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Financial Accounting Global Settings > Document > Line Item > Define Tolerance Groups for Employees`
* **Transaction Code:** `OBA4`
* **Database Table Updated:** `T043T`
* **Baseline Configuration for Blank (Default) Group:**
  * **Company Code:** `1000`
  * **Tolerance Group:** `[Leave Blank]` (Applies to all users unless specifically assigned a named group)
  * **Amount per document:** `999,999,999.00 USD`
  * **Amount per open item account line item:** `100,000,000.00 USD`
  * **Cash discount per line item:** `5.0%`
  * **Permitted Payment Differences:** Max Amount: `$50.00`, Max Percentage: `1.0%`.

---

## 4. Phase 3 — General Ledger Accounting (FI-GL) Configuration

The General Ledger serves as the primary financial ledger and single source of truth for the Balance Sheet and Profit & Loss statements.

```
                      +---------------------------------------+
                      |     Chart of Accounts (COA): GTCA     |
                      |   (Operational: Segmented by OBD4)    |
                      +-------------------+-------------------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
                        v                                   v
          +---------------------------+       +---------------------------+
          |   Balance Sheet Accounts  |       |      P&L / Cost Accounts  |
          |  * 100000 - 199999 Assets |       |  * 400000 - 499999 Revenue|
          |  * 200000 - 299999 Liab   |       |  * 500000 - 599999 Expense|
          +-------------+-------------+       +-------------+-------------+
                        |                                   |
                        |   [OB53 P&L Retained Earnings]    |
                        +-----------------+-----------------+
                                          v
                      [ Balance Sheet Equity: 299999 (Key X) ]
```

### 4.1 Step 16: Define Chart of Accounts (COA) — OB13

* **What it is:** A structured list of all General Ledger accounts used by an enterprise.
* **Three Types of COA in SAP:**
  1. **Operational COA:** Mandatory. Used for day-to-day transactional postings across company codes.
  2. **Group COA:** Optional. Used for corporate-wide consolidated financial reporting.
  3. **Country-Specific COA:** Optional. Used to meet local legal/tax authority accounting layouts while using the Operational COA internally.
* **SPRO Menu Path:** `SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Edit Chart of Accounts List`
* **Transaction Code:** `OB13`
* **Database Table Updated:** `T004` (Chart of Accounts Master)
* **Configuration Parameters:**
  * **Chart of Accounts:** `GTCA`
  * **Description:** GlobalTech Operational Chart of Accounts
  * **Maintenance Language:** `EN`
  * **Length of G/L Account Number:** `6` (allows accounts from 100000 to 999999).
  * **Controlling Integration:** Manual / Automatic creation of cost elements.

### 4.2 Step 17: Assign Company Code to Chart of Accounts — OB62

* **What it is:** Associates Company Code `1000` with Chart of Accounts `GTCA`.
* **SPRO Menu Path:** `SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Assign Company Code to Chart of Accounts`
* **Transaction Code:** `OB62`
* **Database Table Updated:** `T001-KTOPL`
* **Execution:** Map `1000` -> `GTCA` (City/Operational COA) -> Save.

### 4.3 Step 18: Define Account Groups & Field Status for G/L Accounts — OBD4

* **What it is:** Organizes G/L accounts into logical financial classifications and sets screen layout rules when creating G/L master records.
* **Why it is needed:** Ensures that balance sheet accounts have balance sheet fields, and expense accounts have cost accounting fields.
* **SPRO Menu Path:** `SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Define Account Group`
* **Transaction Code:** `OBD4`
* **Database Table Updated:** `T077S` (G/L Account Groups)
* **Standard Account Groups for GTCA:**

| Chart of Accounts | Account Group | Name / Classification | From Account | To Account |
| :--- | :--- | :--- | :--- | :--- |
| `GTCA` | `ASST` | Balance Sheet — Assets | `100000` | `199999` |
| `GTCA` | `LIAB` | Balance Sheet — Liabilities & Equity | `200000` | `299999` |
| `GTCA` | `REVN` | Profit & Loss — Operating Revenue | `300000` | `399999` |
| `GTCA` | `EXPN` | Profit & Loss — Operating Expenses | `400000` | `499999` |
| `GTCA` | `SECD` | Secondary Cost Accounts (S/4HANA) | `500000` | `599999` |

### 4.4 Step 19: Define Retained Earnings Account — OB53

* **What it is:** The designated equity account where the system automatically carries forward annual net profit or loss at the end of each fiscal year.
* **Why it is needed:** P&L accounts must reset to zero at the beginning of the next fiscal year, with the net delta moving into the Balance Sheet Equity section.
* **SPRO Menu Path:** `SPRO > Financial Accounting > General Ledger Accounting > Master Data > G/L Accounts > Preparations > Define Retained Earnings Account`
* **Transaction Code:** `OB53`
* **Database Table Updated:** `T030`
* **Configuration Parameters:**
  * **Chart of Accounts:** `GTCA`
  * **P&L Statement Account Type:** `X`
  * **Account:** `299999` (Retained Earnings Account)
* **System Warning Notice:** SAP will display a yellow warning: *"Account 299999 not yet created in chart of accounts GTCA."* Press Enter to bypass; you will create the physical master record in Step 20.

### 4.5 Step 20: Creation of Master G/L Accounts & S/4HANA Account Types — FS00

* **What it is:** Creating the individual general ledger accounts in the master database.
* **Two-Segment Architecture:**
  1. **Chart of Accounts Segment (`SKA1`):** Holds description, account group, and P&L/BS classification (Shared across all company codes using the COA).
  2. **Company Code Segment (`SKB1`):** Holds currency, tax category, reconciliation account type, field status group, and open item management flag (Unique to each Company Code).
* **Transaction Code:** `FS00` (Centrally), `FSP0` (COA segment), `FSS0` (Company code segment).
* **Critical S/4HANA Evolution — G/L Account Types:**
  * **X — Balance Sheet Account:** Asset and Liability accounts.
  * **N — Non-Operating Expense/Income:** P&L items unrelated to core business (e.g., bank interest income). Does not require a CO cost object.
  * **P — Primary Costs or Revenue:** Core operating expenses (e.g., salaries, utilities). Requires a CO cost object (Cost Center / Internal Order).
  * **S — Secondary Costs:** Costs created exclusively for internal cost allocations within Controlling (e.g., overhead assessment, machine activity rates).

---

## 5. Phase 4 — Accounts Payable (FI-AP) & Procure-to-Pay (P2P) Configuration

Accounts Payable handles vendor liability tracking, invoice verification, 3-way matching, and automated electronic disbursements.

### 5.1 Step 21: Define Vendor Account Groups — OBD3

* **What it is:** Groups vendors based on business type (e.g., Domestic, International, One-Time, Intercompany). Controls field status during vendor creation and links to number ranges.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Vendor Accounts > Master Data > Preparations for Creating Vendor Master Data > Define Account Groups with Screen Layout (Vendors)`
* **Transaction Code:** `OBD3`
* **Database Table Updated:** `T077K`
* **Baseline Vendor Groups:**
  * `VEND`: Domestic Commercial Vendors
  * `VFOR`: Foreign / Overseas Vendors
  * `VOTV`: One-Time Spot Vendors (Requires CPD dummy record)

### 5.2 Step 22: Create Number Ranges for Vendor Accounts — XKN1

* **What it is:** Establishes unique sequential identifier intervals for vendor master records.
* **Transaction Code:** `XKN1`
* **Database Table Updated:** `NRIV`
* **Number Range Configuration:**
  * Range `01`: `0000100000` to `0000199999` (Internal numeric auto-generation).
  * Range `XX`: `A000000000` to `Z999999999` (External alphanumeric).

### 5.3 Step 23: Assign Number Ranges to Vendor Account Groups — OBAS

* **What it is:** Assigns number range `01` to vendor account group `VEND`.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Vendor Accounts > Master Data > Preparations for Creating Vendor Master Data > Assign Number Ranges to Vendor Account Groups`
* **Transaction Code:** `OBAS`
* **Database Table Updated:** `T077K-NUMKR`

### 5.4 Step 24: Define Tolerance Groups for Vendors — OBA3

* **What it is:** Governs small payment variances and grace periods allowed when paying vendor invoices.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Business Transactions > Outgoing Payments > Manual Outgoing Payments > Define Tolerances (Vendors)`
* **Transaction Code:** `OBA3`
* **Database Table Updated:** `T043G`
* **Parameters for Company Code 1000:** Permitted payment differences up to `$10.00` or `1%`.

### 5.5 Step 25: Create Vendor Reconciliation G/L Accounts — FS00

* **What it is:** A specialized General Ledger account that automatically reflects all postings made in the Vendor Sub-Ledger.
* **Crucial Rule for Beginners:** You **cannot** post journal entries directly to a Reconciliation G/L Account via `FB50`! Postings can only occur through vendor transactions (`FB60`, `MIRO`, `F110`).
* **Transaction Code:** `FS00`
* **Parameters:**
  * **Account Number:** `210000` (Accounts Payable Trade)
  * **Account Group:** `LIAB` (Liabilities)
  * **Recon. Account for Acct Type:** `K` (Vendors)
  * **Line Item Display:** Checked
  * **Sort Key:** `012` (Vendor Number)
  * **Field Status Group:** `G067` (Reconciliation Accounts)

### 5.6 Step 26: S/4HANA Business Partner (BP) & Customer-Vendor Integration (CVI) — BP

* **What it is:** In SAP S/4HANA, legacy transactions `XK01`, `FK01`, and `MK01` are obsolete. All entities (Persons, Organizations) are created as a central **Business Partner (`BP`)**.
* **Why it is needed:** The Customer-Vendor Integration (CVI) framework synchronizes the central Business Partner record into the underlying `LFA1` (Vendor master) and `LFB1` (Company code vendor) database tables automatically.
* **Mandatory BP Roles for Vendors:**
  * `000000`: Business Partner (General Header data — name, address, tax ID).
  * `FLVN00`: FI Vendor (Company Code data — Reconciliation Account, Payment Terms).
  * `FLVN01`: Purchasing Vendor (Purchasing Org data — Currency, Incoterms, Partner functions).

### 5.7 Step 27: Define Terms of Payment — OBB8

* **What it is:** Defines credit payment terms, baseline calculation dates, and early payment cash discount tiers (e.g., 2% discount if paid within 10 days, net due in 30 days).
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Business Transactions > Incoming Invoices/Credit Memos > Maintain Terms of Payment`
* **Transaction Code:** `OBB8`
* **Database Table Updated:** `T052`
* **Configuration Parameters for `NT30` & `2110`:**
  * **Payment Term `2110`:**
    * Baseline Date: Posting Date (`Doc Date` or `Entry Date`)
    * Term 1: `2.0%` within `10` Days
    * Term 2: Net due within `30` Days

### 5.8 Step 28: Configure the Automatic Payment Program (APP) — FBZP

* **What it is:** The high-volume automated payment engine in SAP (`F110`) that scans all due vendor invoices, selects open items, optimizes cash discounts, and generates electronic bank transfer files (ACH, SEPA, NACHA, Wire).
* **Transaction Code:** `FBZP` (The Central 6-Button Payment Cockpit)

```
                            +-----------------------------------+
                            |       FBZP Configuration Flow     |
                            +-----------------+-----------------+
                                              |
     +----------------------------------------+---------------------------------------+
     |                    |                   |                   |                   |
     v                    v                   v                   v                   v
[ All Co. Codes ]   [ Paying Co. Code ] [ Pmt Methods: Country ] [ Pmt Methods: Co. Code ] [ Bank Determination ]
- Sending Co Code   - Min amount for    - Checks (C)             - Min/Max amount        - Ranking Order
- Paying Co Code      outgoing payment  - ACH/Bank Transfer (T)  - Form layout           - Bank Accounts
- Intercompany      - Bill of exchange  - Wire (U)               - Payment medium type   - Available Amounts
```

1. **All Company Codes:** Designate `1000` as both Sending and Paying Company Code.
2. **Paying Company Codes:** Set minimum disbursement threshold (e.g., `$10.00`) to prevent processing zero-value payments.
3. **Payment Methods in Country:** Define methods allowed in US: `C` (Check), `T` (ACH Transfer), `U` (Wire).
4. **Payment Methods in Company Code:** Assign method `T` to Company Code `1000`, setting minimum amount `$1.00` and maximum `$999,999,999.00`.
5. **Bank Determination:** Configure **Ranking Order** (which house bank pays first), **Bank Accounts** (G/L sub-account clearing), and **Available Amounts** (ensures payments do not exceed bank credit balances).
6. **House Banks (`FI12`):** Create House Bank `CHAS1` (JPMorgan Chase), Bank Key, Routing Number, and Bank Account `1000-CHK`.

---

## 6. Phase 5 — Accounts Receivable (FI-AR) & Order-to-Cash (O2C) Configuration

Accounts Receivable tracks customer billing, credit limits, automated dunning collections, and incoming cash application.

### 6.1 Step 29: Define Customer Account Groups — OBD2

* **What it is:** Segregates customers by business classification (Wholesale, Retail, Export, Intercompany).
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Customer Accounts > Master Data > Preparations for Creating Customer Master Data > Define Account Groups with Screen Layout (Customers)`
* **Transaction Code:** `OBD2`
* **Database Table Updated:** `T077D`
* **Configuration Entries:**
  * `CUST`: Domestic Commercial Customers
  * `CFOR`: International / Export Customers

### 6.2 Step 30: Create Customer Number Ranges & Assign — XDN1 & OBAR

* **What it is:** Assigns sequential identification ranges to customer account records.
* **Transaction Codes:** `XDN1` (Define Intervals), `OBAR` (Assign to Customer Account Groups).
* **Database Table Updated:** `NRIV`, `T077D-NUMKR`

### 6.3 Step 31: Create Customer Reconciliation G/L Accounts — FS00

* **What it is:** The control G/L account updated whenever a customer invoice (`FB70` / `VF01`) or payment receipt (`F-28`) is posted.
* **Transaction Code:** `FS00`
* **Parameters:**
  * **Account Number:** `120000` (Accounts Receivable Trade)
  * **Account Group:** `ASST` (Assets)
  * **Recon. Account for Acct Type:** `D` (Customers)
  * **Sort Key:** `031` (Customer Number)
  * **Field Status Group:** `G067` (Reconciliation Accounts)

### 6.4 Step 32: S/4HANA Customer BP Roles — FLCU00 & FLCU01

* **What it is:** In S/4HANA, customers are maintained via Business Partner (`BP`).
* **Roles:**
  * `FLCU00`: FI Customer (Company Code segment: Reconciliation Account `120000`, Terms of Payment, Dunning Data).
  * `FLCU01`: Sales & Distribution Customer (Sales Org, Distribution Channel, Division, Pricing Procedure, Shipping Conditions).

### 6.5 Step 33: Configure Dunning Procedure — FBMP

* **What it is:** The automated customer overdue payment escalation mechanism (`F150`). It tracks overdue invoices and systematically generates escalating reminder notices with accrued late payment penalties.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Accounts Receivable and Accounts Payable > Business Transactions > Dunning > Dunning Procedure > Define Dunning Procedures`
* **Transaction Code:** `FBMP`
* **Database Table Updated:** `T047`, `T047A`
* **Baseline Dunning Architecture (4-Level Escalation):**
  * **Dunning Interval:** `14 Days` (Time between consecutive notices).
  * **Grace Period:** `3 Days`.
  * **Level 1 (14 Days Past Due):** Gentle reminder; no fee, no interest.
  * **Level 2 (28 Days Past Due):** Urgent reminder; `$25.00` administrative fee.
  * **Level 3 (42 Days Past Due):** Demand notice; `$50.00` fee + `8%` statutory interest.
  * **Level 4 (56 Days Past Due):** Legal action warning; automatic credit hold triggered.

### 6.6 Step 34: Configure Customer Credit Management

* **What it is:** Evaluates incoming sales orders against customer credit lines.
* **Architecture Distinction:**
  * **Classic SAP ECC (`FD32`):** Managed directly within FI-AR using Credit Control Area `GTCR` and update keys (`000012`).
  * **SAP S/4HANA FSCM Credit Management (`UKM_BP`):** Fully integrated with Financial Supply Chain Management, using Credit Segments, Risk Classes, and automated scoring rules.

---

## 7. Phase 6 — Asset Accounting (FI-AA) Configuration

Asset Accounting manages the complete lifecycle of fixed assets—from acquisition and Assets under Construction (AuC) to depreciation calculations, asset transfers, and retirements.

```
                           +-------------------------------------+
                           |   Chart of Depreciation: GTCD       |
                           |   (Assigned to Co. Code: OAOB)      |
                           +------------------+------------------+
                                              |
                        +---------------------+---------------------+
                        |                                           |
                        v                                           v
         +-----------------------------+             +-----------------------------+
         |      Depreciation Area 01   |             |      Depreciation Area 15   |
         |  * Book Depreciation (Local)|             |  * Tax Depreciation (IRS)   |
         |  * Real-Time Posting to GL  |             |  * Statistical Only         |
         +--------------+--------------+             +--------------+--------------+
                        |                                           |
                        +---------------------+---------------------+
                                              |
                                              v
                           +-------------------------------------+
                           |         Asset Classes: OAOA         |
                           |  * Land & Buildings (1000)          |
                           |  * Plant & Machinery (2000)         |
                           |  * IT & Office Equipment (3000)     |
                           |  * Assets under Construction (4000) |
                           +------------------+------------------+
                                              |
                                              v  [Account Determination: AO90]
                           +-------------------------------------+
                           |        Automatic GL Postings        |
                           |  * APC Balance Sheet (Dr)           |
                           |  * Accumulated Depreciation (Cr)    |
                           |  * Depreciation Expense (Dr)        |
                           +-------------------------------------+
```

### 7.1 Step 35: Copy Reference Chart of Depreciation — EC08

* **What it is:** The highest organizational unit in Asset Accounting, containing all country-specific Depreciation Areas (Book, Tax, Group).
* **SPRO Menu Path:** `SPRO > Financial Accounting > Asset Accounting > Organizational Structures > Copy Reference Chart of Depreciation/Depreciation Areas`
* **Transaction Code:** `EC08`
* **Database Table Updated:** `T096`
* **Consultant Rule:** Never create from scratch! Copy standard country template (e.g., `0US` for USA or `0IN` for India) to `GTCD` (GlobalTech Chart of Depreciation).

### 7.2 Step 36: Assign Chart of Depreciation to Company Code — OAOB

* **What it is:** Binds Chart of Depreciation `GTCD` to Company Code `1000`.
* **Transaction Code:** `OAOB`
* **Database Table Updated:** `T001-CHAZV`

### 7.3 Step 37: Specify Account Determination Keys & Screen Layout Rules — AO25 & OA77

* **What it is:** Account Determination links asset classes to specific G/L accounts. Screen Layout Rules determine which fields appear when creating asset master records (`AS01`).
* **Transaction Codes:** `AO25` (Account Determination), `OA77` (Screen Layout).
* **Keys Created:**
  * `10000`: Buildings
  * `20000`: Plant Machinery
  * `30000`: IT Hardware & Vehicles
  * `40000`: Assets under Construction (AuC)

### 7.4 Step 38: Define Number Range Intervals for Asset Classes — AS08

* **What it is:** Defines internal master record numbers for assets.
* **Transaction Code:** `AS08`
* **Configuration:** Interval `01`: `0000010000` to `0000019999` (Company Code `1000`).

### 7.5 Step 39: Define Asset Classes — OAOA

* **What it is:** The primary category that groups assets with identical accounting behavior (e.g., Land, Machinery, IT Assets, AuC).
* **SPRO Menu Path:** `SPRO > Financial Accounting > Asset Accounting > Organizational Structures > Asset Classes > Define Asset Classes`
* **Transaction Code:** `OAOA`
* **Database Table Updated:** `ANLA`
* **Asset Class Mapping Table:**

| Asset Class | Description | Account Determination | Screen Layout | Number Range | Line Item Settlement (AuC) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1000` | Buildings & Real Estate | `10000` | `1000` | `01` | No |
| `2000` | Machinery & Equipment | `20000` | `2000` | `01` | No |
| `3000` | IT Equipment & Laptops | `30000` | `3000` | `01` | No |
| `4000` | Assets under Construction | `40000` | `4000` | `01` | Yes (Investment Order) |

### 7.6 Step 40: Assign G/L Accounts for Automatic Depreciation Postings — AO90

* **What it is:** Directs the system on which G/L accounts to debit and credit when an asset is acquired, depreciated, sold, or scrapped.
* **Transaction Code:** `AO90`
* **Database Table Updated:** `T095`, `T095B`
* **G/L Account Mapping Table (Asset Class 2000 - Machinery):**
  * **Balance Sheet APC Account:** `150000` (Machinery Asset Cost - Dr)
  * **Contra Account: Acquisition Value:** `150009` (Asset Clearing - Cr)
  * **Accumulated Depreciation Account:** `150100` (Accumulated Depr Machinery - Cr)
  * **Depreciation Expense P&L Account:** `450000` (Depreciation Expense Machinery - Dr)
  * **Loss on Asset Scrapping / Retirement:** `450200` (P&L Loss on Disposal - Dr)
  * **Gain on Asset Sale:** `350100` (P&L Gain on Disposal - Cr)

### 7.7 Step 41: Define Depreciation Keys & Calculation Methods — AFAMA & AFAMS

* **What it is:** Formulas that calculate monthly asset depreciation.
* **Transaction Code:** `AFAMA` (Depreciation Keys), `AFAMS` (Multi-level Methods).
* **Standard Depreciation Methods:**
  * **Straight Line Method (SLM) `LINR`:** Depreciates acquisition cost evenly over useful life (e.g., 5 years = 20% per year).
  * **Written Down Value (WDV) `0002`:** Declining balance method calculating depreciation on the remaining net book value.

### 7.8 Step 42: S/4HANA Technical Clearing Account for Asset Acquisition

* **What it is:** In SAP S/4HANA New Asset Accounting, external asset acquisitions require a **Technical Clearing Account** (`FS00` G/L type Balance Sheet, Recon: None).
* **Why it is needed:** S/4HANA splits asset acquisitions into:
  1. An **Operational Document** (Vendor Credit, Technical Clearing Account Debit) posted to all ledgers.
  2. An **Evaluating Document** (Technical Clearing Account Credit, Asset Balance Sheet Debit) posted ledger-specifically (IFRS, US GAAP, Local GAAP) in real time.
* **SPRO Menu Path:** `SPRO > Financial Accounting > Asset Accounting > Integration with General Ledger Accounting > Define Technical Clearing Account for Integrated Asset Acquisition`

---

## 8. Phase 7 — Controlling (CO) Enterprise & Basic Configuration

SAP Controlling (CO) is designed exclusively for internal management accounting, cost absorption, overhead calculation, and business segment profitability.

```
                           +-----------------------------------+
                           |      Controlling Area: 1000       |
                           |   (GlobalTech Controlling Area)   |
                           +-----------------+-----------------+
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
                   v                                                   v
    +------------------------------+                    +------------------------------+
    |    Company Code: 1000        |                    |    Company Code: 2000        |
    | (GlobalTech USA - USD)       |                    | (GlobalTech Europe - EUR)    |
    +------------------------------+                    +------------------------------+
    (Cross-Company Cost Accounting enabled when Currency Type = 30 & COA = GTCA)
```

### 8.1 Step 43: Maintain Controlling Area — OKKP

* **What it is:** The highest organizational unit in Management Accounting. It defines the boundary where cost allocations, internal overhead settlements, and activity distributions occur.
* **Two Fundamental Relationships:**
  1. **1:1 Relationship:** One Controlling Area to One Company Code (Simple, single entity).
  2. **1:N Cross-Company Code Controlling:** One Controlling Area oversees multiple legal Company Codes (Enables cross-entity cost allocations and shared service center billing).
* **SPRO Menu Path:** `SPRO > Controlling > General Controlling > Organization > Maintain Controlling Area`
* **Transaction Code:** `OKKP`
* **Database Table Updated:** `TKA01` (Controlling Areas)
* **Configuration Parameters for GlobalTech:**
  * **Controlling Area:** `1000`
  * **Name:** GlobalTech Controlling Area
  * **CoCode -> CoArea:** `Cross-company-code cost accounting`
  * **Currency Type:** `30` (Group Currency - USD)
  * **Chart of Accounts:** `GTCA`
  * **Fiscal Year Variant:** `K4`
  * **Cost Center Standard Hierarchy:** `GTHIER` (System prompts to create; accept Yes).

### 8.2 Step 44: Assign Company Code to Controlling Area — OX19 / OKKP

* **What it is:** Formally assigns Company Code `1000` to Controlling Area `1000`.
* **Transaction Code:** `OX19` (or inside `OKKP > Assignment of Company Codes`).
* **Database Table Updated:** `TKA02`

### 8.3 Step 45: Maintain Number Ranges for Controlling Documents — KANK

* **What it is:** Allocates document number intervals for internal CO transactions (e.g., cost assessments, activity allocations, internal order settlements).
* **Transaction Code:** `KANK`
* **Database Table Updated:** `NRIV`
* **Consultant Best Practice:** Copy standard SAP number range elements from reference Controlling Area `0001` to `1000` to immediately instantiate all CO business transaction groups (`COIN`, `RKU1`, `RKU2`, `RKL`).

### 8.4 Step 46: Maintain Controlling Versions (Plan/Actual Version 0) — OKEQ / OKEV

* **What it is:** Controlling maintains versions to segregate actual financial postings from multiple planning simulations.
* **Mandatory Version:** **Version 0** (Actual / Plan). All actual operational postings reside exclusively in Version 0.
* **Transaction Code:** `OKEQ` (General Version Settings), `OKEV` (Fiscal Year Specific Settings).
* **Configuration:** Activate Version `0` for Year `2026` in Controlling Area `1000`, checking "Integrated Planning" and "Copying Allowed".

---

## 9. Phase 8 — Cost Center Accounting (CO-CCA) & Cost Element Configuration

Cost Center Accounting tracks where overhead expenses are incurred across organizational departments (e.g., IT, Human Resources, Executive Management, Maintenance).

### 9.1 Step 47: Activate Cost Center Accounting in Controlling Area — OKKP

* **What it is:** Enables the functional sub-components within Controlling Area `1000`.
* **Execution in `OKKP` ("Activate components/control indicators"):**
  * **Cost Centers:** Active (`Component active`)
  * **Order Management:** Active
  * **Commitment Management:** Active
  * **Profit Center Accounting:** Active

### 9.2 Step 48: Define Standard Hierarchy for Cost Centers — OKEON

* **What it is:** A tree structure grouping all departmental cost centers under corporate nodes.
* **Transaction Code:** `OKEON` (Enterprise Organization) or `OKENN`.
* **Structure:**
  * Top Node: `GTHIER` (GlobalTech Standard Hierarchy)
    * Sub-Node `GT-ADM`: Corporate Administration
    * Sub-Node `GT-OPS`: Operations & Plant
    * Sub-Node `GT-SAL`: Sales & Marketing

### 9.3 Step 49: Create Cost Center Categories — OKA2

* **What it is:** Categorizes cost centers (e.g., `1` = Production, `3` = Administration, `4` = Sales). Governs default lock parameters for revenues and secondary costs.
* **Transaction Code:** `OKA2`

### 9.4 Step 50: Create Master Cost Centers — KS01 / KS02

* **What it is:** Instantiating the individual cost center master records.
* **Transaction Code:** `KS01` (Create), `KS02` (Change), `KS03` (Display).
* **Database Table Updated:** `CSKS` (Cost Center Master), `CSKT` (Descriptions).
* **Baseline Master Cost Centers:**

| Cost Center | Name | Cost Center Category | Hierarchy Node | Profit Center | Person Responsible |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1000-FIN` | Finance & Accounting | `3` (Administration) | `GT-ADM` | `PC-CORP` | L. Gupta |
| `1000-IT` | Information Technology | `3` (Administration) | `GT-ADM` | `PC-CORP` | J. Doe |
| `1000-MFG` | Plant Machinery Shop | `1` (Production) | `GT-OPS` | `PC-PLANT`| M. Vance |

### 9.5 Step 51: Cost Elements Architecture: ECC KA01/KA06 vs S/4HANA FS00

* **The Evolution:**
  * In **SAP ECC 6.0**, Cost Elements were maintained separately from G/L accounts using `KA01` (Primary Cost Elements) and `KA06` (Secondary Cost Elements).
  * In **SAP S/4HANA**, the cost element master is merged entirely into the General Ledger Master (`FS00`) under the Universal Journal (`ACDOCA`).
* **S/4HANA Cost Categories in `FS00`:**
  * **Category 01 (Primary Costs):** Consumes expenses originating in FI (e.g., Rent, Salaries).
  * **Category 11 (Revenues):** Sales and operational revenue accounts.
  * **Category 21 (Internal Settlement):** Settles internal orders to cost centers.
  * **Category 42 (Assessment):** Used for periodic overhead assessment cycles.
  * **Category 43 (Internal Activity Allocation):** Distributes machine/labor activity rates.

### 9.6 Step 52: Define Activity Types & Activity Price Planning — KL01 & KP26

* **What it is:** Activity Types represent services produced by a cost center (e.g., Machine Hours, Consulting Hours, Labor Hours).
* **Transaction Codes:** `KL01` (Create Activity Type), `KP26` (Cost Center Activity Price Planning).
* **Parameters for `MACH_HR` (Machine Hours):**
  * Activity Unit: `H` (Hours)
  * Cost Center: `1000-MFG`
  * Planned Rate: `$45.00 / Hour`
* **Downstream Integration:** When production runs confirm 10 hours of machine work in SAP PP, SAP automatically debits the Production Order for `$450.00` and credits Cost Center `1000-MFG`.

### 9.7 Step 53: Define Statistical Key Figures (SKF) — KK01

* **What it is:** Measurable physical values used as allocation tracing factors (e.g., Square Footage, Headcount, Number of Network Users).
* **Transaction Code:** `KK01`
* **Baseline SKFs:**
  * `SQFT`: Square Footage (Fixed Value)
  * `HEADC`: Headcount (Average Value)

### 9.8 Step 54: Configure Cost Allocations: Distribution vs. Assessment — KSV1 / KSU1

```
+-----------------------------------+-----------------------------------+
|      DISTRIBUTION (KSV1/KSV5)     |       ASSESSMENT (KSU1/KSU5)      |
+-----------------------------------+-----------------------------------+
| * Allocates: Primary Costs only   | * Allocates: Primary & Secondary  |
| * Original Cost Element preserved | * Grouped into Secondary Element  |
| * High audit detail, high volume  | * Clean, aggregated P&L view      |
| * Traced via original account     | * Uses Category 42 Cost Element   |
+-----------------------------------+-----------------------------------+
```

---

## 10. Phase 9 — Internal Orders (CO-IO) & Profit Center Accounting (CO-PCA)

### 10.1 Step 55: Define Order Types for Internal Orders — KOT2_OPA

* **What it is:** Internal Orders track costs and revenues for temporary, short-term corporate projects (e.g., Marketing Trade Show, R&D Prototype, Office Renovation).
* **Two Order Types:**
  * **Real Internal Order:** Collects costs and settles them out to Cost Centers, Fixed Assets, or P&L at project completion.
  * **Statistical Internal Order:** For monitoring only; does not require settlement.
* **Transaction Code:** `KOT2_OPA`
* **Configuration:** Define Order Type `GT01` (Real Development Project).

### 10.2 Step 56: Define Settlement Profiles & Allocation Structures — OKO7

* **What it is:** Specifies where an internal order's costs are transferred upon settlement (e.g., allowing settlement to Cost Center, Fixed Asset, or G/L Account).
* **Transaction Code:** `OKO7`
* **Settlement Profile Parameters:** Maximum 100% distribution; Valid Receivers: Cost Center (`CTR`), Fixed Asset (`FXA`).

### 10.3 Step 57: Maintain Profit Center Standard Hierarchy & Dummy Profit Center — KCH1 & KE59

* **What it is:** Profit Centers represent decentralized organizational units that generate both revenues and costs, allowing management to evaluate departmental Return on Investment (ROI) and independent P&L statements.
* **Transaction Codes:** `KCH1` (Profit Center Standard Hierarchy), `KE59` (Dummy Profit Center for catching unassigned postings).
* **Hierarchy:** `GTPCHIER`

### 10.4 Step 58: Create Profit Centers — KE51

* **Transaction Code:** `KE51`
* **Database Table Updated:** `CEPC`, `CEPCT`
* **Baseline Profit Centers:**
  * `PC-CORP`: Corporate Services
  * `PC-PLANT`: Manufacturing & Industrial Operations
  * `PC-COMM`: Commercial Wholesale Sales

### 10.5 Step 59: Set Control Parameters for Profit Center Accounting — 0KE5 / 1KEF

* **What it is:** Activates Profit Center accounting in Controlling Area `1000` for Fiscal Year `2026`.
* **Transaction Code:** `0KE5`

---

## 11. Phase 10 — Cross-Module Integration Configuration (MM-FI & SD-FI)

Automated account determination transforms logistics and sales transactions into real-time accounting entries without manual intervention.

### 11.1 Step 60: FI-MM Integration (OBYC Automatic Account Determination)

* **What it is:** The configuration engine that automatically determines G/L accounts when physical goods are received (`MIGO`) or vendor invoices verified (`MIRO`).
* **Core Architectural Components:**
  1. **Valuation Area:** Typically the Plant (`1000`).
  2. **Valuation Grouping Code (`OMWD`):** Groups plants with identical accounting rules.
  3. **Valuation Class (`OMSK`):** Categorizes materials (e.g., `3000` Raw Materials, `7920` Finished Goods).
  4. **Transaction Keys (`OBYC`):** Pre-delivered SAP account keys.
* **Standard FI-MM Transaction Keys:**

| Transaction Key | Name | Debit / Credit Mechanics | Example Trigger | G/L Account Assigned |
| :--- | :--- | :--- | :--- | :--- |
| `BSX` | Inventory Posting | Dr Inventory / Cr Inventory | Goods Receipt for PO | `130000` (Raw Material Stock) |
| `WRX` | GR/IR Clearing Account | Interim accrual clearing | Goods Receipt / Invoice Verification | `210050` (GR/IR Interim Liability)|
| `PRD` | Price Differences | Variance between PO and Std Cost| Purchase Price Variance | `510000` (Price Variance Expense) |
| `GBB` | Offsetting Inventory Post | Inventory issues & scrap | Goods Issue to Cost Center (`201`)| `430000` (Material Consumption) |

### 11.2 Step 61: FI-SD Integration (VKOA Revenue Account Determination)

* **What it is:** Automatically identifies the correct revenue and tax G/L accounts when a billing document (`VF01`) is issued in Sales & Distribution.
* **Condition Technique in VKOA:**
  * Application: `V` (Sales/Distribution)
  * Condition Type: `KOFI` (Standard Account Determination)
  * Access Sequence: Evaluates Sales Org + Customer Account Group + Material Account Assignment Group.
* **Standard Account Keys:**
  * `ERL`: Gross Sales Revenue (Credits Revenue G/L `300000`)
  * `ERS`: Sales Deductions & Cash Discounts (Debits Sales Discount G/L `310000`)
  * `MWS`: Output Sales Tax (Credits Output Tax Liability `220000`)

---

## 12. Phase 11 — End-to-End Configuration Verification & Testing Checklist

A configuration is never considered complete until it passes rigorous integration test scenarios.

```
+---------------------------------------------------------------------------------------+
|                       END-TO-END INTEGRATION TEST SCENARIO                            |
+---------------------------------------------------------------------------------------+
|  1. G/L Posting (FB50)        ==> Debit Cash (110000) / Credit Capital (200000)      |
|  2. Vendor Invoice (FB60)     ==> Debit Expense (410000) / Credit Vendor Liability   |
|  3. Payment Run (F110)        ==> Debit Vendor Liability / Credit Bank Outgoing Check |
|  4. Customer Invoice (FB70)   ==> Debit Customer Receivable / Credit Revenue (300000) |
|  5. Cash Receipt (F-28)       ==> Debit Bank Cash / Credit Customer Receivable        |
|  6. Asset Depreciation (AFAB) ==> Debit Depreciation Exp / Credit Accumulated Depr    |
|  7. Overhead Assessment (KSU5)==> Allocate IT Costs from 1000-IT to 1000-MFG          |
|  8. Audit Balance Sheet (F.01)==> Validate that Total Debits == Total Credits        |
+---------------------------------------------------------------------------------------+
```

### 12.1 Unit & Integration Testing Strategy

Testing must follow three progressive phases:
1. **Unit Testing:** Testing isolated configurations (e.g., posting a simple direct journal entry in `FB50`).
2. **System Integration Testing (SIT):** Testing cross-module data handoffs (e.g., MM Goods Receipt -> FI GR/IR posting -> APP payment).
3. **User Acceptance Testing (UAT):** Business users execute standard daily processes using real-world master data.

### 12.2 Test Script 1: General Ledger Direct Journal Entry — FB50

* **Objective:** Verify Document Type `SA`, Number Range `01`, Field Status Variant `GTFS`, and Tolerance Groups.
* **T-Code:** `FB50`
* **Test Steps:**
  1. Company Code: `1000`, Currency: `USD`, Date: Today.
  2. Line 1: G/L `110000` (Cash on Hand) -> Debit `$10,000.00`.
  3. Line 2: G/L `299999` (Retained Earnings / Equity) -> Credit `$10,000.00`.
  4. Ensure light is **Green** (Debits = Credits). Click **Post**.
* **Expected Result:** Document `0100000001` posted successfully. Verify entry in `FB03` or table `BKPF`/`ACDOCA`.

### 12.3 Test Script 2: Procure-to-Pay (P2P) Vendor Invoice & Payment — FB60 & F110

* **Objective:** Validate Vendor Master, Recon Account `210000`, Terms of Payment, and FBZP Automatic Payment Program.
* **T-Code 1:** `FB60` (Vendor Invoice)
  * Vendor: `100001` (Acme Supplies)
  * Invoice Date: Today, Amount: `$5,000.00`
  * Expense G/L: `410000` (Office Supplies), Cost Center: `1000-FIN`.
  * Click **Post**. Result: Document `1900000001` created.
* **T-Code 2:** `F110` (Automatic Payment Run)
  * Run Date: Today, Identification: `GT001`.
  * Parameters: Company Code `1000`, Payment Method `T`, Next Posting Date: Next week.
  * Execute Proposal & Payment Run.
* **Expected Result:** Open vendor item cleared; payment document `1500000001` generated. Verify vendor balance is `$0.00` in `FBL1N`.

### 12.4 Test Script 3: Order-to-Cash (O2C) Customer Invoice & Clearing — FB70 & F-28

* **Objective:** Validate Customer Master, Recon Account `120000`, Revenue posting, and Cash application.
* **T-Code 1:** `FB70` (Customer Invoice)
  * Customer: `200001` (Apex Retail), Amount: `$8,000.00`.
  * Revenue G/L: `300000`, Profit Center: `PC-COMM`.
  * Click **Post**. Result: Document `1800000001` created.
* **T-Code 2:** `F-28` (Incoming Cash Payment)
  * Account: `110000` (Bank Clearing), Amount: `$8,000.00`.
  * Select Customer `200001`, match open invoice, and **Post**.
* **Expected Result:** Customer account cleared in `FBL5N`.

### 12.5 Test Script 4: Asset Acquisition & Depreciation Run — F-90 & AFAB

* **Objective:** Validate Asset Class `2000`, Account Determination `AO90`, and Depreciation Key `LINR`.
* **T-Code 1:** `F-90` (Acquisition with Vendor)
  * Asset: `10000-0` (Machinery Unit 1), Amount: `$60,000.00`, Useful Life: 5 Years.
* **T-Code 2:** `AFAB` (Depreciation Run)
  * Company Code `1000`, Fiscal Year `2026`, Period `01`, Execute in Test Run first, then in Background.
* **Expected Result:** Asset Explorer (`AW01N`) displays `$1,000.00 / month` planned depreciation (`$60,000 / 60 months`). Financial posting debits Depreciation Expense `450000` and credits Accumulated Depreciation `150100`.

### 12.6 Test Script 5: Controlling Overhead Assessment Run — KSU5

* **Objective:** Validate Assessment Cycle, Secondary Cost Element Category 42, and Cost Center clearing.
* **T-Code:** `KSU5`
* **Test Steps:**
  1. Post `$12,000.00` IT expense to Cost Center `1000-IT` via `FB50`.
  2. Execute Assessment Cycle `ITALLOC` in `KSU5` for Period 01.
* **Expected Result:** Cost Center `1000-IT` balance drops to `$0.00`; receiving Cost Centers (`1000-FIN`, `1000-MFG`) receive their proportional share based on Headcount SKF (`HEADC`).

### 12.7 Test Script 6: Financial Balance Sheet & P&L Generation — F.01

* **Objective:** Audit the complete financial statement version.
* **T-Code:** `F.01`
* **Parameters:** Company Code `1000`, Chart of Accounts `GTCA`, Year `2026`.
* **Expected Result:** Balance Sheet displays Total Assets equal to Total Liabilities + Equity. No unassigned accounts appear in the error section.

---

## 13. Phase 12 — Troubleshooting Guide: Common Configuration Errors & Solutions

| Error Code / Message | Root Cause | SPRO Navigation Path | Fast T-Code Fix |
| :--- | :--- | :--- | :--- |
| **F5 394**<br>*"Field status group does not match posting key"* | Conflict between Field Status Group in `FS00` and Posting Key rules in `OB41` (e.g., one requires Cost Center, the other suppresses it). | `SPRO > Financial Accounting Global Settings > Ledgers > Fields > Define Field Status Variants` | Align settings in `OBC4` and `OB41`. |
| **F5 286 / F5 201**<br>*"Posting period 001/2026 is not open"* | The active posting period variant has not opened the current month or the specific account type (`+`, `S`, `K`, `D`). | `SPRO > Financial Accounting Global Settings > Ledgers > Fiscal Year and Posting Periods > Posting Periods > Open and Close Posting Periods` | Open period in `OB52`. |
| **F5 150 / F5 151**<br>*"Number range interval missing for year 2026"* | Document number range for the fiscal year has not been maintained for the company code. | `SPRO > Financial Accounting Global Settings > Document > Document Number Ranges > Define Document Number Ranges` | Add year interval in `FBN1`. |
| **M8 147**<br>*"Account determination for BSX/WRX not possible"* | Material movement cannot find a matching G/L account for Valuation Class and Transaction Key. | `SPRO > Materials Management > Valuation and Account Assignment > Account Determination > Account Determination Without Wizard` | Maintain missing G/L accounts in `OBYC`. |
| **KI 235 / KI 222**<br>*"Account requires an assignment to a CO object"* | A primary cost account (G/L Type P) was posted without specifying a Cost Center or Internal Order. | `SPRO > Controlling > Cost Center Accounting > Actual Postings > Manual Actual Postings` | Enter Cost Center on line item or set default account assignment in `OKB9`. |
| **CVI_MAPPING 020**<br>*"Customer/Vendor synchronization failed in BP"* | Number range or grouping mismatch between Business Partner and underlying Customer/Vendor account groups. | `SPRO > Cross-Application Components > Master Data Synchronization > Customer/Vendor Integration > Business Partner Settings` | Verify BP number assignment in `MDS_LINKS` / SPRO. |

---

## 14. Phase 13 — Master Configuration Reference Matrix & SPRO Cheat Sheet

| Step # | Configuration Element | Module | SPRO Navigation Breadcrumb | T-Code | Mandatory? | Prerequisites |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- |
| **1** | Define Company | FI | `Enterprise Structure > Definition > Financial Accounting > Define Company` | `OX15` | Mandatory | None |
| **2** | Define Company Code | FI | `Enterprise Structure > Definition > Financial Accounting > Edit Company Code Data` | `OX02` | Mandatory | None |
| **3** | Assign Co. Code to Company | FI | `Enterprise Structure > Assignment > Financial Accounting > Assign Co. Code to Company` | `OX16` | Mandatory | Step 1, 2 |
| **4** | Define Business Area | FI | `Enterprise Structure > Definition > Financial Accounting > Define Business Area` | `OX03` | Optional | None |
| **5** | Define Credit Control Area | FI | `Enterprise Structure > Definition > Financial Accounting > Define Credit Control Area` | `OB45` | Mandatory | None |
| **6** | Assign Co. Code to Credit Area | FI | `Enterprise Structure > Assignment > Financial Accounting > Assign Co. Code to Credit Area` | `OB38` | Mandatory | Step 2, 5 |
| **7** | Maintain Fiscal Year Variant | FI | `Financial Accounting Global Settings > Ledgers > Fiscal Year > Maintain FYV` | `OB29` | Mandatory | None |
| **8** | Assign Co. Code to FYV | FI | `Financial Accounting Global Settings > Ledgers > Fiscal Year > Assign Co. Code to FYV` | `OB37` | Mandatory | Step 2, 7 |
| **9** | Define Posting Period Variant | FI | `Financial Accounting Global Settings > Ledgers > Posting Periods > Define Variants` | `OBBO` | Mandatory | None |
| **10** | Assign Co. Code to PPV | FI | `Financial Accounting Global Settings > Ledgers > Posting Periods > Assign Variants` | `OBBP` | Mandatory | Step 2, 9 |
| **11** | Open & Close Posting Periods | FI | `Financial Accounting Global Settings > Ledgers > Posting Periods > Open/Close Periods` | `OB52` | Mandatory | Step 9 |
| **12** | Define Field Status Variant | FI | `Financial Accounting Global Settings > Ledgers > Fields > Define Field Status Variants` | `OBC4` | Mandatory | None |
| **13** | Assign Co. Code to FSV | FI | `Financial Accounting Global Settings > Ledgers > Fields > Assign Co. Code to FSV` | `OBC5` | Mandatory | Step 2, 12 |
| **14** | Define Document Types & Ranges | FI | `Financial Accounting Global Settings > Document > Document Types / Number Ranges` | `OBA7 / FBN1`| Mandatory | Step 2 |
| **15** | Define Tolerance Groups | FI | `Financial Accounting Global Settings > Document > Line Item > Define Tolerances` | `OBA4 / OBA0`| Mandatory | Step 2 |
| **16** | Define Chart of Accounts | FI | `General Ledger Accounting > Master Data > G/L Accounts > Edit Chart of Accounts` | `OB13` | Mandatory | None |
| **17** | Assign Co. Code to COA | FI | `General Ledger Accounting > Master Data > G/L Accounts > Assign Co. Code to COA` | `OB62` | Mandatory | Step 2, 16 |
| **18** | Define Account Groups | FI | `General Ledger Accounting > Master Data > G/L Accounts > Define Account Group` | `OBD4` | Mandatory | Step 16 |
| **19** | Retained Earnings Account | FI | `General Ledger Accounting > Master Data > G/L Accounts > Define Retained Earnings`| `OB53` | Mandatory | Step 16 |
| **20** | Create G/L Master Records | FI | `Accounting > Financial Accounting > General Ledger > Master Records > G/L Accounts`| `FS00` | Mandatory | Step 17, 18, 19 |
| **21** | Vendor Account Groups | FI-AP | `Accounts Receivable & Payable > Vendor Accounts > Master Data > Define Account Groups`| `OBD3` | Mandatory | None |
| **22** | Vendor Number Ranges | FI-AP | `Accounts Receivable & Payable > Vendor Accounts > Master Data > Define Number Ranges` | `XKN1` | Mandatory | None |
| **23** | Assign Vendor Number Ranges | FI-AP | `Accounts Receivable & Payable > Vendor Accounts > Master Data > Assign Number Ranges` | `OBAS` | Mandatory | Step 21, 22 |
| **24** | Vendor Tolerance Groups | FI-AP | `Accounts Receivable & Payable > Business Transactions > Outgoing Payments > Tolerances`| `OBA3` | Mandatory | Step 2 |
| **25** | Terms of Payment | FI-AP | `Accounts Receivable & Payable > Business Transactions > Maintain Terms of Payment` | `OBB8` | Mandatory | None |
| **26** | Automatic Payment Program | FI-AP | `Accounts Receivable & Payable > Business Transactions > Outgoing Payments > Auto Pmt` | `FBZP` | Mandatory | Step 20, 25 |
| **27** | Customer Account Groups | FI-AR | `Accounts Receivable & Payable > Customer Accounts > Master Data > Account Groups` | `OBD2` | Mandatory | None |
| **28** | Customer Number Ranges | FI-AR | `Accounts Receivable & Payable > Customer Accounts > Master Data > Number Ranges` | `XDN1 / OBAR`| Mandatory | Step 27 |
| **29** | Dunning Procedures | FI-AR | `Accounts Receivable & Payable > Business Transactions > Dunning > Define Procedures` | `FBMP` | Optional | Step 20 |
| **30** | Copy Chart of Depreciation | FI-AA | `Asset Accounting > Organizational Structures > Copy Reference Chart of Depreciation` | `EC08` | Mandatory | None |
| **31** | Assign Chart of Depr to CoCode | FI-AA | `Asset Accounting > Organizational Structures > Assign Chart of Depr to Co. Code` | `OAOB` | Mandatory | Step 2, 30 |
| **32** | Define Asset Classes | FI-AA | `Asset Accounting > Organizational Structures > Asset Classes > Define Asset Classes` | `OAOA` | Mandatory | Step 30 |
| **33** | Assign G/L Accounts for Depr | FI-AA | `Asset Accounting > Integration with General Ledger > Assign G/L Accounts` | `AO90` | Mandatory | Step 20, 32 |
| **34** | Maintain Depreciation Keys | FI-AA | `Asset Accounting > Depreciation > Valuation Methods > Depreciation Key` | `AFAMA` | Mandatory | Step 30 |
| **35** | Maintain Controlling Area | CO | `Controlling > General Controlling > Organization > Maintain Controlling Area` | `OKKP` | Mandatory | Step 16, 7 |
| **36** | Assign Co. Code to Co. Area | CO | `Controlling > General Controlling > Organization > Assign Co. Code to Co. Area` | `OX19` | Mandatory | Step 2, 35 |
| **37** | Controlling Number Ranges | CO | `Controlling > General Controlling > Organization > Maintain Number Ranges` | `KANK` | Mandatory | Step 35 |
| **38** | Maintain Controlling Versions | CO | `Controlling > General Controlling > Organization > Maintain Versions` | `OKEQ` | Mandatory | Step 35 |
| **39** | Cost Center Standard Hierarchy | CO-CCA| `Controlling > Cost Center Accounting > Master Data > Standard Hierarchy` | `OKEON` | Mandatory | Step 35 |
| **40** | Create Cost Centers | CO-CCA| `Accounting > Controlling > Cost Center Accounting > Master Data > Cost Center > Create` | `KS01` | Mandatory | Step 39 |
| **41** | Activity Types & Rates | CO-CCA| `Controlling > Cost Center Accounting > Master Data > Activity Types` | `KL01 / KP26`| Optional | Step 40 |
| **42** | Internal Order Types | CO-IO | `Controlling > Internal Orders > Order Master Data > Define Order Types` | `KOT2_OPA` | Optional | Step 35 |
| **43** | Profit Center Standard Hierarchy| CO-PCA| `Controlling > Profit Center Accounting > Master Data > Standard Hierarchy` | `KCH1` | Mandatory | Step 35 |
| **44** | Create Profit Centers | CO-PCA| `Accounting > Controlling > Profit Center Accounting > Master Data > Profit Center` | `KE51` | Mandatory | Step 43 |
| **45** | FI-MM Account Determination | MM-FI | `Materials Management > Valuation and Account Assignment > Account Determination` | `OBYC` | Mandatory | Step 20 |
| **46** | FI-SD Account Determination | SD-FI | `Sales and Distribution > Basic Functions > Account Assignment > Revenue Determination`| `VKOA` | Mandatory | Step 20 |

---

## 15. Conclusion & Professional Recommendations

### 15.1 SAP S/4HANA vs. ECC 6.0 Configuration Paradigm Shifts

For an aspiring SAP consultant, mastering configuration requires recognizing how the architectural landscape transformed with SAP S/4HANA:

1. **The Universal Journal (`ACDOCA`):**
   * *In ECC:* Data was split across disparate tables (`BKPF`/`BSEG` for FI, `COEP` for CO, `ANEP` for Assets, `FAGLFLEXA` for New G/L). End-of-month reconciliation between FI and CO was a stressful, manual chore.
   * *In S/4HANA:* A single unified line-item table (`ACDOCA`) captures all FI, CO, AA, and ML transactions simultaneously, eliminating the need for periodic reconciliation.
2. **Business Partner (`BP`) Supremacy:**
   * *In ECC:* Customers and Vendors were managed in separate silos via `XD01` and `XK01`.
   * *In S/4HANA:* Business Partner is mandatory. Master data is created once and extended to Customer (`FLCU00`/`FLCU01`) and Vendor (`FLVN00`/`FLVN01`) roles via CVI.
3. **New Asset Accounting:**
   * *In ECC:* Asset postings only updated Book Depreciation in real time; tax areas updated periodically via background batch programs (`ASKB`).
   * *In S/4HANA:* All depreciation areas update their respective ledgers in real time using the **Technical Clearing Account**.
4. **Unified Cost Element Architecture:**
   * *In ECC:* Cost elements were managed via `KA01`/`KA06`.
   * *In S/4HANA:* Cost elements are consolidated into G/L Master (`FS00`) as Account Types `P` and `S`.

### 15.2 Key Takeaways for Beginners & ERP Consultants

* **Respect the Dependencies:** SAP configuration is strictly sequential. Attempting to define G/L master accounts before assigning a Chart of Accounts to a Company Code will result in hard system aborts. Always follow the Phase 1 through Phase 10 order documented in this guide.
* **Never Modify Golden Clients Directly with Transactions:** Protect DEV Client 110. All configuration changes must be tagged with descriptive, trackable Transport Requests.
* **Master the Account Modifiers:** Deepen your knowledge of `OBYC` and `VKOA`. In real-world enterprise consulting, cross-module integration is where 80% of critical go-live defects occur.

### 15.3 Author Statement & Internship Sign-off

This configuration manual was prepared by **Laxmi Gupta** as the formal deliverable for **Week 2 of the SAP Consulting / ERP Internship**. The procedures, SPRO paths, transaction codes, and architectural blueprints documented herein have been compiled and verified against SAP ECC 6.0 EHP8 and SAP S/4HANA 2023 release standards.

* **Author:** Laxmi Gupta  
* **Role:** SAP Consulting / ERP Intern  
* **Date:** October 2026  
* **Status:** Complete, Validated & Audit-Ready  
