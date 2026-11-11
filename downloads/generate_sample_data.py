#!/usr/bin/env python3
"""Generate the fictional Continual Improvement Plan sample workbook and CSVs.

All rows are flagged "Fictional sample". Nothing in this file is live evidence
or a real organisation. Re-run from the repository root:

    python3 scripts/generate_sample_data.py
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.properties import CalcProperties
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "sample-data"
OUT_XLSX = OUT_DIR / "Continual_Improvement_Plan_SAMPLE.xlsx"
DATA_FLAG = "Fictional sample"
NAVY = "1B365D"
HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
BODY_FONT = Font(name="Calibri", size=11, color="3D4F61")
THIN = Border(
    left=Side(style="thin", color="D0D5DA"),
    right=Side(style="thin", color="D0D5DA"),
    top=Side(style="thin", color="D0D5DA"),
    bottom=Side(style="thin", color="D0D5DA"),
)
WRAP = Alignment(vertical="center", wrap_text=True)
LEFT = Alignment(vertical="center", horizontal="left")

CONTROLS: list[tuple[str, str, str]] = [
    # Organizational (5.1–5.37)
    ("5.1", "Policies for information security", "Organizational"),
    ("5.2", "Information security roles and responsibilities", "Organizational"),
    ("5.3", "Segregation of duties", "Organizational"),
    ("5.4", "Management responsibilities", "Organizational"),
    ("5.5", "Contact with authorities", "Organizational"),
    ("5.6", "Contact with special interest groups", "Organizational"),
    ("5.7", "Threat intelligence", "Organizational"),
    ("5.8", "Information security in project management", "Organizational"),
    ("5.9", "Inventory of information and other associated assets", "Organizational"),
    ("5.10", "Acceptable use of information and other associated assets", "Organizational"),
    ("5.11", "Return of assets", "Organizational"),
    ("5.12", "Classification of information", "Organizational"),
    ("5.13", "Labelling of information", "Organizational"),
    ("5.14", "Information transfer", "Organizational"),
    ("5.15", "Access control", "Organizational"),
    ("5.16", "Identity management", "Organizational"),
    ("5.17", "Authentication information", "Organizational"),
    ("5.18", "Access rights", "Organizational"),
    ("5.19", "Information security in supplier relationships", "Organizational"),
    ("5.20", "Addressing information security within supplier agreements", "Organizational"),
    ("5.21", "Managing information security in the ICT supply chain", "Organizational"),
    ("5.22", "Monitoring, review and change management of supplier services", "Organizational"),
    ("5.23", "Information security for use of cloud services", "Organizational"),
    ("5.24", "Information security incident management planning and preparation", "Organizational"),
    ("5.25", "Assessment and decision on information security events", "Organizational"),
    ("5.26", "Response to information security incidents", "Organizational"),
    ("5.27", "Learning from information security incidents", "Organizational"),
    ("5.28", "Collection of evidence", "Organizational"),
    ("5.29", "Information security during disruption", "Organizational"),
    ("5.30", "ICT readiness for business continuity", "Organizational"),
    ("5.31", "Legal, statutory, regulatory and contractual requirements", "Organizational"),
    ("5.32", "Intellectual property rights", "Organizational"),
    ("5.33", "Protection of records", "Organizational"),
    ("5.34", "Privacy and protection of PII", "Organizational"),
    ("5.35", "Independent review of information security", "Organizational"),
    ("5.36", "Compliance with policies, rules and standards for information security", "Organizational"),
    ("5.37", "Documented operating procedures", "Organizational"),
    # People (6.1–6.8)
    ("6.1", "Screening", "People"),
    ("6.2", "Terms and conditions of employment", "People"),
    ("6.3", "Information security awareness, education and training", "People"),
    ("6.4", "Disciplinary process", "People"),
    ("6.5", "Responsibilities after termination or change of employment", "People"),
    ("6.6", "Confidentiality or non-disclosure agreements", "People"),
    ("6.7", "Remote working", "People"),
    ("6.8", "Information security event reporting", "People"),
    # Physical (7.1–7.14)
    ("7.1", "Physical security perimeters", "Physical"),
    ("7.2", "Physical entry", "Physical"),
    ("7.3", "Securing offices, rooms and facilities", "Physical"),
    ("7.4", "Physical security monitoring", "Physical"),
    ("7.5", "Protecting against physical and environmental threats", "Physical"),
    ("7.6", "Working in secure areas", "Physical"),
    ("7.7", "Clear desk and clear screen", "Physical"),
    ("7.8", "Equipment siting and protection", "Physical"),
    ("7.9", "Security of assets off-premises", "Physical"),
    ("7.10", "Storage media", "Physical"),
    ("7.11", "Supporting utilities", "Physical"),
    ("7.12", "Cabling security", "Physical"),
    ("7.13", "Equipment maintenance", "Physical"),
    ("7.14", "Secure disposal or re-use of equipment", "Physical"),
    # Technological (8.1–8.34)
    ("8.1", "User endpoint devices", "Technological"),
    ("8.2", "Privileged access rights", "Technological"),
    ("8.3", "Information access restriction", "Technological"),
    ("8.4", "Access to source code", "Technological"),
    ("8.5", "Secure authentication", "Technological"),
    ("8.6", "Capacity management", "Technological"),
    ("8.7", "Protection against malware", "Technological"),
    ("8.8", "Management of technical vulnerabilities", "Technological"),
    ("8.9", "Configuration management", "Technological"),
    ("8.10", "Information deletion", "Technological"),
    ("8.11", "Data masking", "Technological"),
    ("8.12", "Data leakage prevention", "Technological"),
    ("8.13", "Information backup", "Technological"),
    ("8.14", "Redundancy of information processing facilities", "Technological"),
    ("8.15", "Logging", "Technological"),
    ("8.16", "Monitoring activities", "Technological"),
    ("8.17", "Clock synchronisation", "Technological"),
    ("8.18", "Use of privileged utility programs", "Technological"),
    ("8.19", "Installation of software on operational systems", "Technological"),
    ("8.20", "Networks security", "Technological"),
    ("8.21", "Security of network services", "Technological"),
    ("8.22", "Segregation of networks", "Technological"),
    ("8.23", "Web filtering", "Technological"),
    ("8.24", "Use of cryptography", "Technological"),
    ("8.25", "Secure development life cycle", "Technological"),
    ("8.26", "Application security requirements", "Technological"),
    ("8.27", "Secure system architecture and engineering principles", "Technological"),
    ("8.28", "Secure coding", "Technological"),
    ("8.29", "Security testing in development and acceptance", "Technological"),
    ("8.30", "Outsourced development", "Technological"),
    ("8.31", "Separation of development, test and production environments", "Technological"),
    ("8.32", "Change management", "Technological"),
    ("8.33", "Test information", "Technological"),
    ("8.34", "Protection of information systems during audit testing", "Technological"),
]

THEMES: list[dict] = [
    {
        "id": "RT-01",
        "name": "Access control and identity",
        "description": "Identity lifecycle, authentication, access rights and privileged access.",
        "likelihood": 4,
        "impact": 5,
        "controls": ["5.15", "5.16", "5.17", "5.18", "8.2", "8.3", "8.5", "8.18"],
    },
    {
        "id": "RT-02",
        "name": "Third-party and supply chain",
        "description": "Supplier selection, agreements, ICT supply chain, cloud service use and oversight.",
        "likelihood": 4,
        "impact": 4,
        "controls": ["5.19", "5.20", "5.21", "5.22", "5.23", "8.30"],
    },
    {
        "id": "RT-03",
        "name": "Data protection and confidentiality",
        "description": "Classification, transfer, privacy, records, encryption, masking and leakage prevention.",
        "likelihood": 3,
        "impact": 5,
        "controls": ["5.10", "5.12", "5.13", "5.14", "5.32", "5.33", "5.34", "6.6", "8.10", "8.11", "8.12", "8.24"],
    },
    {
        "id": "RT-04",
        "name": "Vulnerability and technical hygiene",
        "description": "Patching, configuration, malware, logging, monitoring, network and web protection.",
        "likelihood": 4,
        "impact": 4,
        "controls": ["8.7", "8.8", "8.9", "8.15", "8.16", "8.17", "8.19", "8.20", "8.21", "8.22", "8.23"],
    },
    {
        "id": "RT-05",
        "name": "Human factor and awareness",
        "description": "Screening, employment terms, awareness, remote working, event reporting and clear desk.",
        "likelihood": 3,
        "impact": 3,
        "controls": ["6.1", "6.2", "6.3", "6.4", "6.5", "6.7", "6.8", "7.7"],
    },
    {
        "id": "RT-06",
        "name": "Incident response and resilience",
        "description": "Incident planning, response, lessons learned, backups, redundancy and continuity.",
        "likelihood": 3,
        "impact": 5,
        "controls": ["5.24", "5.25", "5.26", "5.27", "5.28", "5.29", "5.30", "8.13", "8.14"],
    },
    {
        "id": "RT-07",
        "name": "Asset and change management",
        "description": "Asset inventory, return of assets, endpoints, capacity, environment separation and change.",
        "likelihood": 3,
        "impact": 3,
        "controls": ["5.8", "5.9", "5.11", "8.1", "8.6", "8.31", "8.32", "8.33", "8.34"],
    },
    {
        "id": "RT-08",
        "name": "Cloud and emerging technology",
        "description": "Secure development, application security, architecture, coding, testing and source-code access, including unsanctioned AI tools.",
        "likelihood": 3,
        "impact": 4,
        "controls": ["8.4", "8.25", "8.26", "8.27", "8.28", "8.29"],
    },
    {
        "id": "RT-09",
        "name": "Physical and environmental security",
        "description": "Perimeters, entry, facilities, monitoring, environmental threats, media and equipment.",
        "likelihood": 2,
        "impact": 3,
        "controls": ["7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.8", "7.9", "7.10", "7.11", "7.12", "7.13", "7.14"],
    },
    {
        "id": "RT-10",
        "name": "Compliance and assurance",
        "description": "Policies, roles, management responsibilities, legal requirements and independent review.",
        "likelihood": 2,
        "impact": 4,
        "controls": ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.31", "5.35", "5.36", "5.37"],
    },
]

CONTROL_TO_THEME: dict[str, dict] = {}
for theme in THEMES:
    for cid in theme["controls"]:
        CONTROL_TO_THEME[cid] = theme

assert len(CONTROLS) == 93, len(CONTROLS)
assert len(CONTROL_TO_THEME) == 93, f"mapped {len(CONTROL_TO_THEME)}"
assert set(CONTROL_TO_THEME) == {c[0] for c in CONTROLS}

OWNERS = [
    {"id": "OWN-01", "name": "J. Bennett", "role": "Group Information Security Manager", "entity": "Group", "function": "Information security", "email": "j.bennett@example.org", "manager": "Chief Operating Officer"},
    {"id": "OWN-02", "name": "A. Rahman", "role": "IT Security Lead", "entity": "United Kingdom", "function": "IT", "email": "a.rahman@example.org", "manager": "J. Bennett"},
    {"id": "OWN-03", "name": "P. Hughes", "role": "People Lead", "entity": "United Kingdom", "function": "People", "email": "p.hughes@example.org", "manager": "J. Bennett"},
    {"id": "OWN-04", "name": "M. García", "role": "Information Security Lead", "entity": "Spain", "function": "Information security", "email": "m.garcia@example.org", "manager": "J. Bennett"},
    {"id": "OWN-05", "name": "C. Vargas", "role": "IT Operations", "entity": "Spain", "function": "IT", "email": "c.vargas@example.org", "manager": "M. García"},
    {"id": "OWN-06", "name": "C. Dubois", "role": "Information Security Lead", "entity": "France", "function": "Information security", "email": "c.dubois@example.org", "manager": "J. Bennett"},
    {"id": "OWN-07", "name": "N. Laurent", "role": "IT Operations", "entity": "France", "function": "IT", "email": "n.laurent@example.org", "manager": "C. Dubois"},
    {"id": "OWN-08", "name": "L. Schmidt", "role": "Information Security Lead", "entity": "Germany", "function": "Information security", "email": "l.schmidt@example.org", "manager": "J. Bennett"},
    {"id": "OWN-09", "name": "K. Weber", "role": "IT Operations", "entity": "Germany", "function": "IT", "email": "k.weber@example.org", "manager": "L. Schmidt"},
    {"id": "OWN-10", "name": "R. Okonkwo", "role": "Data Protection Officer", "entity": "Group", "function": "Data protection", "email": "r.okonkwo@example.org", "manager": "Chief Operating Officer"},
    {"id": "OWN-11", "name": "S. Patel", "role": "Supplier Risk Lead", "entity": "Group", "function": "Procurement", "email": "s.patel@example.org", "manager": "J. Bennett"},
    {"id": "OWN-12", "name": "T. Walsh", "role": "Internal Audit Manager", "entity": "Group", "function": "Internal audit", "email": "t.walsh@example.org", "manager": "Chief Operating Officer"},
]
OWNER_BY_ID = {o["id"]: o for o in OWNERS}

# Curated fictional findings. Dates are designed around an as-at date of 11 Nov 2026.
# Columns after the comment keys are filled by build_findings().
RAW_FINDINGS: list[dict] = [
    # --- Repeat NC: 8.5 Secure authentication across UK, France, Spain (also overdue / aged) ---
    dict(id="IA-2026-001", title="MFA not enforced on a privileged remote-access path", typ="NC", sev="High", control="8.5", entity="United Kingdom", owner="OWN-02", raised="2026-03-15", target="2026-06-30", status="Open", closed=None, root="Inconsistent MFA policy exception that was never time-bounded.", source="Internal audit", auditor="T. Walsh", desc="A privileged remote-access path in the United Kingdom entity can be used without multi-factor authentication. The exception was granted as temporary and has no review date."),
    dict(id="IA-2026-002", title="Legacy single-factor VPN accounts still active", typ="NC", sev="High", control="8.5", entity="France", owner="OWN-06", raised="2026-04-02", target="2026-07-31", status="In Progress", closed=None, root="Service-account inventory incomplete; decommission plan slipped.", source="Internal audit", auditor="T. Walsh", desc="A set of legacy VPN accounts in the France entity still authenticates with a password only. A remediation project exists but has missed its target date."),
    dict(id="IA-2026-003", title="Conditional access not applied to a line-of-business app", typ="NC", sev="Medium", control="8.5", entity="Spain", owner="OWN-04", raised="2026-08-10", target="2026-11-30", status="Open", closed=None, root="Application excluded from the standard identity baseline during a migration.", source="Internal audit", auditor="T. Walsh", desc="One line-of-business application used in the Spain entity is excluded from the standard conditional-access baseline, so secure authentication is not consistently enforced."),
    # --- Repeat NC: 5.19 supplier relationships, UK and Germany ---
    dict(id="IA-2026-004", title="Critical supplier onboarded without a completed security assessment", typ="NC", sev="High", control="5.19", entity="United Kingdom", owner="OWN-11", raised="2026-02-20", target="2026-05-31", status="Open", closed=None, root="Procurement pathway allowed a waiver that was not closed.", source="Internal audit", auditor="T. Walsh", desc="A supplier rated as critical to operations in the United Kingdom was engaged before the information-security assessment was finished. The waiver remains open."),
    dict(id="IA-2026-005", title="Supplier register missing residual-risk owners", typ="NC", sev="Medium", control="5.19", entity="Germany", owner="OWN-08", raised="2026-05-12", target="2026-09-30", status="In Progress", closed=None, root="Register template does not require an owner field.", source="Internal audit", auditor="T. Walsh", desc="The Germany entity supplier register lists residual risks without a named owner or review date, so treatments are not being chased."),
    # --- Repeat NC: 8.8 vulnerabilities, Spain and France ---
    dict(id="IA-2026-006", title="Critical patches exceeding the agreed service window", typ="NC", sev="High", control="8.8", entity="Spain", owner="OWN-05", raised="2026-04-18", target="2026-07-15", status="Open", closed=None, root="Change calendar and vulnerability SLA are not reconciled.", source="Internal audit", auditor="T. Walsh", desc="Several internet-facing systems in the Spain entity have critical patches older than the agreed service window."),
    dict(id="IA-2026-007", title="Vulnerability scan exceptions without an expiry date", typ="NC", sev="High", control="8.8", entity="France", owner="OWN-07", raised="2026-04-18", target="2026-07-15", status="Open", closed=None, root="Exception process allows open-ended deferrals.", source="Surveillance audit", auditor="T. Walsh", desc="Vulnerability-scan exceptions in the France entity have been accepted without an expiry or compensating control review."),
    # --- Low maturity + NC on other controls ---
    dict(id="IA-2026-008", title="Privileged access review not completed for two quarters", typ="NC", sev="High", control="8.2", entity="United Kingdom", owner="OWN-02", raised="2026-06-01", target="2026-08-31", status="In Progress", closed=None, root="Review is manual and has no standing agenda item.", source="Internal audit", auditor="T. Walsh", desc="The quarterly privileged-access review for the United Kingdom entity was skipped in two consecutive quarters."),
    dict(id="IA-2026-009", title="Cloud service inventory incomplete", typ="NC", sev="Medium", control="5.23", entity="Germany", owner="OWN-08", raised="2026-07-20", target="2026-10-31", status="Open", closed=None, root="Shadow IT discovered during a network review.", source="Internal audit", auditor="T. Walsh", desc="Two departmental cloud services in the Germany entity are in use but are not on the approved cloud inventory or covered by the standard terms."),
    dict(id="IA-2026-010", title="Backup restore test overdue", typ="NC", sev="High", control="8.13", entity="United Kingdom", owner="OWN-02", raised="2026-01-22", target="2026-04-30", status="In Progress", closed=None, root="Test window repeatedly deferred for operational reasons.", source="Internal audit", auditor="T. Walsh", desc="The agreed annual restore test for a system holding business-critical records in the United Kingdom has not been completed within the target."),
    # --- Cluster of OFI / OBS on human factor (6.3 and related) ---
    dict(id="IA-2026-011", title="Awareness module completion below the agreed threshold", typ="OFI", sev="Medium", control="6.3", entity="United Kingdom", owner="OWN-03", raised="2026-07-08", target="2026-10-15", status="Open", closed=None, root="Reminders are email-only and not escalated to line managers.", source="Internal audit", auditor="T. Walsh", desc="Annual information-security awareness completion in the United Kingdom entity is below the threshold agreed in the training standard."),
    dict(id="IA-2026-012", title="Phishing simulation follow-up not documented", typ="OFI", sev="Medium", control="6.3", entity="Spain", owner="OWN-04", raised="2026-07-22", target="2026-11-15", status="Open", closed=None, root="Follow-up is informal.", source="Internal audit", auditor="T. Walsh", desc="Staff in the Spain entity who failed a phishing simulation did not have a documented follow-up or refresher."),
    dict(id="IA-2026-013", title="New-starter induction can be completed after system access is granted", typ="OFI", sev="Medium", control="6.3", entity="France", owner="OWN-06", raised="2026-08-05", target="2026-11-30", status="In Progress", closed=None, root="Joiner workflow does not gate access on induction.", source="Internal audit", auditor="T. Walsh", desc="In the France entity, system access can be granted before the security induction module is completed."),
    dict(id="IA-2026-014", title="Role-specific training not defined for privileged users", typ="OBS", sev="Low", control="6.3", entity="Germany", owner="OWN-08", raised="2026-08-19", target="2026-12-15", status="Open", closed=None, root="Only the generic module is mandated.", source="Internal audit", auditor="T. Walsh", desc="Privileged users in the Germany entity receive the same awareness module as all staff; no role-specific module is defined."),
    dict(id="IA-2026-015", title="Clear-desk checks are informal and unrecorded", typ="OBS", sev="Low", control="7.7", entity="United Kingdom", owner="OWN-03", raised="2026-09-01", target="2026-12-01", status="Open", closed=None, root="No sampling plan exists.", source="Internal audit", auditor="T. Walsh", desc="Clear-desk and clear-screen checks in the United Kingdom offices are done informally and are not recorded, so trend data is not available."),
    dict(id="IA-2026-016", title="Remote-working guidance not reissued after a tooling change", typ="OFI", sev="Low", control="6.7", entity="France", owner="OWN-06", raised="2026-09-14", target="2026-12-18", status="Open", closed=None, root="Guidance is not on the document review calendar.", source="Internal audit", auditor="T. Walsh", desc="Remote-working guidance in the France entity still refers to a retired collaboration tool."),
    # --- Cloud / unsanctioned AI (generic) ---
    dict(id="IA-2026-017", title="No approved-use list for generative AI tools", typ="Gap", sev="High", control="8.26", entity="United Kingdom", owner="OWN-01", raised="2026-06-16", target="2026-09-30", status="In Progress", closed=None, root="Emerging-technology policy has not been updated.", source="Management review", auditor="T. Walsh", desc="Staff in the United Kingdom entity have no approved-use list or data-handling rules for generative AI tools, so confidential information could be entered into public services."),
    dict(id="IA-2026-018", title="Secure development standard does not mention AI-assisted coding", typ="OFI", sev="Medium", control="8.25", entity="Germany", owner="OWN-08", raised="2026-08-03", target="2027-01-15", status="Open", closed=None, root="Standard last reviewed before the tools were in use.", source="Internal audit", auditor="T. Walsh", desc="The secure development standard used in the Germany entity does not cover AI-assisted coding, code-review expectations or licence obligations."),
    dict(id="IA-2026-019", title="Source-code access for a contractor not time-bounded", typ="NC", sev="Medium", control="8.4", entity="France", owner="OWN-07", raised="2026-05-27", target="2026-08-29", status="Closed", closed="2026-09-12", root="Contractor off-boarding did not include repository access.", source="Internal audit", auditor="T. Walsh", desc="A contractor in the France entity retained source-code access after the engagement ended. Access has since been removed (closed after the target date)."),
    # --- Data protection ---
    dict(id="IA-2026-020", title="Records of processing not updated after a system change", typ="NC", sev="Medium", control="5.34", entity="United Kingdom", owner="OWN-10", raised="2026-03-03", target="2026-06-15", status="Closed", closed="2026-06-10", root="Change process does not trigger a privacy review.", source="Internal audit", auditor="T. Walsh", desc="A system change in the United Kingdom entity altered personal-data flows but the record of processing was not updated until the audit follow-up."),
    dict(id="IA-2026-021", title="Classification labels missing on a shared workspace", typ="OFI", sev="Medium", control="5.12", entity="Spain", owner="OWN-04", raised="2026-09-08", target="2026-12-08", status="Open", closed=None, root="Workspace template has no default label.", source="Internal audit", auditor="T. Walsh", desc="A widely used shared workspace in the Spain entity has no default information classification, so labelling is inconsistent."),
    dict(id="IA-2026-022", title="Encryption key-rotation interval not evidenced", typ="Gap", sev="Medium", control="8.24", entity="Germany", owner="OWN-09", raised="2026-07-01", target="2026-10-31", status="In Progress", closed=None, root="Rotation is performed but not logged in the evidence library.", source="Internal audit", auditor="T. Walsh", desc="The Germany entity could not produce evidence that cryptographic keys are rotated at the interval stated in the standard."),
    # --- Resilience / incident ---
    dict(id="IA-2026-023", title="Incident playbook has no payment-diversion scenario", typ="OFI", sev="Medium", control="5.24", entity="United Kingdom", owner="OWN-01", raised="2026-05-06", target="2026-08-15", status="Closed", closed="2026-08-01", root="Playbook scoped only to technical incidents.", source="Internal audit", auditor="T. Walsh", desc="The incident playbook used in the United Kingdom entity did not include a payment-diversion or social-engineering scenario. A scenario has since been added."),
    dict(id="IA-2026-024", title="Lessons-learned register not reviewed at management review", typ="OBS", sev="Low", control="5.27", entity="France", owner="OWN-06", raised="2026-09-21", target="2026-12-21", status="Open", closed=None, root="Agenda does not include the register as a standing item.", source="Management review", auditor="T. Walsh", desc="Lessons from incidents in the France entity are recorded but were not taken to the last management review."),
    dict(id="IA-2026-025", title="Business-continuity test limited to a table-top discussion", typ="OFI", sev="Medium", control="5.30", entity="Spain", owner="OWN-04", raised="2026-06-24", target="2026-11-30", status="In Progress", closed=None, root="Live test deferred because of a change freeze.", source="Internal audit", auditor="T. Walsh", desc="The only continuity test in the Spain entity this year was a table-top discussion; the live failover test is still outstanding."),
    # --- Compliance / assurance ---
    dict(id="IA-2026-026", title="Policy review dates lapsed on three core policies", typ="NC", sev="Medium", control="5.1", entity="Group", owner="OWN-01", raised="2026-02-10", target="2026-05-15", status="Closed", closed="2026-05-12", root="Review calendar was not owned after a role change.", source="Internal audit", auditor="T. Walsh", desc="Three core information-security policies at Group level had passed their review dates. They have since been reviewed and reissued."),
    dict(id="IA-2026-027", title="Statement of applicability not updated after a control change", typ="OFI", sev="Low", control="5.36", entity="Group", owner="OWN-01", raised="2026-08-26", target="2026-12-15", status="Open", closed=None, root="SoA update is a manual year-end task.", source="Internal audit", auditor="T. Walsh", desc="A control implementation change at Group level has not yet been reflected in the statement of applicability."),
    dict(id="IA-2026-028", title="Independent review of information security overdue", typ="Gap", sev="Medium", control="5.35", entity="Group", owner="OWN-12", raised="2026-04-07", target="2026-09-30", status="Closed", closed="2026-11-04", root="External reviewer procurement took longer than planned.", source="Management review", auditor="T. Walsh", desc="The planned independent review at Group level started late and closed after the original target."),
    # --- Physical ---
    dict(id="IA-2026-029", title="Visitor log incomplete for a server room", typ="OBS", sev="Low", control="7.2", entity="Spain", owner="OWN-05", raised="2026-09-29", target="2026-12-29", status="Open", closed=None, root="Paper log is not reconciled to the badge system.", source="Internal audit", auditor="T. Walsh", desc="The visitor log for a server room in the Spain entity has missing sign-out times on several days."),
    dict(id="IA-2026-030", title="Off-premises equipment inventory out of date", typ="OFI", sev="Low", control="7.9", entity="Germany", owner="OWN-09", raised="2026-07-15", target="2026-10-31", status="Closed", closed="2026-10-20", root="Leavers process did not always trigger a kit return check.", source="Internal audit", auditor="T. Walsh", desc="Laptop and token records for off-premises equipment in the Germany entity were out of date. The inventory has been rebuilt."),
    # --- Closed on time (various) to support the on-time measure ---
    dict(id="IA-2025-001", title="Asset inventory missing a newly commissioned platform", typ="NC", sev="Medium", control="5.9", entity="United Kingdom", owner="OWN-02", raised="2025-02-11", target="2025-05-15", status="Closed", closed="2025-05-02", root="Project handover did not include the asset register.", source="Internal audit", auditor="T. Walsh", desc="A newly commissioned platform in the United Kingdom was not added to the asset inventory at go-live. It was added before the target date."),
    dict(id="IA-2025-002", title="Leaver access removed after the agreed timescale", typ="NC", sev="High", control="5.18", entity="France", owner="OWN-06", raised="2025-03-04", target="2025-05-30", status="Closed", closed="2025-05-20", root="HR notification reached IT late.", source="Internal audit", auditor="T. Walsh", desc="Access for a leaver in the France entity was removed after the agreed timescale. The joiner-mover-leaver workflow was tightened."),
    dict(id="IA-2025-003", title="Logging not enabled on a new application", typ="NC", sev="Medium", control="8.15", entity="Spain", owner="OWN-05", raised="2025-04-16", target="2025-07-16", status="Closed", closed="2025-07-01", root="Logging was listed as a post-go-live task and forgotten.", source="Internal audit", auditor="T. Walsh", desc="Application logging was not enabled at go-live in the Spain entity. It was switched on and added to the build standard."),
    dict(id="IA-2025-004", title="Malware signature update lag on a small office site", typ="OFI", sev="Low", control="8.7", entity="Germany", owner="OWN-09", raised="2025-05-20", target="2025-08-20", status="Closed", closed="2025-08-08", root="A site was left on a manual update ring.", source="Internal audit", auditor="T. Walsh", desc="A small office in the Germany entity was several days behind on malware signature updates. It is now on the standard ring."),
    dict(id="IA-2025-005", title="Network diagram not updated after a segmentation change", typ="OBS", sev="Low", control="8.22", entity="United Kingdom", owner="OWN-02", raised="2025-06-10", target="2025-09-10", status="Closed", closed="2025-09-04", root="Document owner was on long leave.", source="Internal audit", auditor="T. Walsh", desc="The network diagram used in the United Kingdom entity did not show a recent segmentation change. It has been redrawn."),
    dict(id="IA-2025-006", title="Capacity trend report not produced for two months", typ="OFI", sev="Low", control="8.6", entity="France", owner="OWN-07", raised="2025-07-02", target="2025-10-02", status="Closed", closed="2025-09-25", root="Report job failed silently.", source="Internal audit", auditor="T. Walsh", desc="The monthly capacity trend report in the France entity had stopped running. Monitoring of the job has been added."),
    dict(id="IA-2025-007", title="Screening evidence missing for a short-term contractor", typ="Gap", sev="Medium", control="6.1", entity="Spain", owner="OWN-04", raised="2025-07-22", target="2025-10-22", status="Closed", closed="2025-10-10", root="Agency pack was not filed in the evidence library.", source="Internal audit", auditor="T. Walsh", desc="Screening evidence for a short-term contractor in the Spain entity could not be located. The file has been retrieved and the filing rule restated."),
    dict(id="IA-2025-008", title="Change tickets closed without a back-out plan", typ="OFI", sev="Medium", control="8.32", entity="Germany", owner="OWN-09", raised="2025-08-13", target="2025-11-13", status="Closed", closed="2025-11-01", root="Template made the field optional.", source="Internal audit", auditor="T. Walsh", desc="A sample of change tickets in the Germany entity had been closed without a back-out plan. The field is now mandatory."),
    dict(id="IA-2025-009", title="Documented operating procedure outdated for a backup job", typ="OBS", sev="Low", control="5.37", entity="United Kingdom", owner="OWN-02", raised="2025-09-03", target="2025-12-03", status="Closed", closed="2025-11-20", root="Procedure was not on the review calendar.", source="Internal audit", auditor="T. Walsh", desc="The written procedure for a backup job in the United Kingdom entity described a retired tool. It has been rewritten."),
    dict(id="IA-2025-010", title="Test data contained production-like personal data", typ="NC", sev="High", control="8.33", entity="France", owner="OWN-06", raised="2025-09-17", target="2025-12-17", status="Closed", closed="2025-12-05", root="A refresh process copied unmasked records.", source="Internal audit", auditor="T. Walsh", desc="A test environment in the France entity contained production-like personal data. The refresh process now applies masking."),
    dict(id="IA-2025-011", title="Web filtering exceptions not reviewed in twelve months", typ="OFI", sev="Low", control="8.23", entity="Spain", owner="OWN-05", raised="2025-10-08", target="2026-01-08", status="Closed", closed="2026-01-06", root="No scheduled review.", source="Internal audit", auditor="T. Walsh", desc="Web-filtering exceptions in the Spain entity had not been reviewed for twelve months. A quarterly review is now in place."),
    dict(id="IA-2025-012", title="Clock synchronisation drift on a logging collector", typ="OBS", sev="Low", control="8.17", entity="Germany", owner="OWN-09", raised="2025-10-29", target="2026-01-29", status="Closed", closed="2026-01-15", root="NTP source was misconfigured after a rebuild.", source="Internal audit", auditor="T. Walsh", desc="A logging collector in the Germany entity had clock drift against the standard time source. Configuration has been corrected."),
    dict(id="IA-2025-013", title="Acceptable-use acknowledgement not captured for new starters", typ="Gap", sev="Medium", control="5.10", entity="United Kingdom", owner="OWN-03", raised="2025-11-12", target="2026-02-12", status="Closed", closed="2026-02-04", root="The acknowledgement step was dropped from the induction checklist.", source="Internal audit", auditor="T. Walsh", desc="New starters in the United Kingdom entity were not being asked to acknowledge the acceptable-use policy. The step has been restored."),
    dict(id="IA-2025-014", title="Endpoint encryption status not reported to the operations meeting", typ="OFI", sev="Low", control="8.1", entity="France", owner="OWN-07", raised="2025-11-26", target="2026-02-26", status="Closed", closed="2026-02-18", root="Metric existed but was not on the agenda.", source="Internal audit", auditor="T. Walsh", desc="Endpoint encryption coverage in the France entity was not being reported. It is now a standing operations metric."),
    dict(id="IA-2025-015", title="Physical monitoring coverage gap at a loading bay", typ="OBS", sev="Low", control="7.4", entity="Spain", owner="OWN-05", raised="2025-12-09", target="2026-03-09", status="Closed", closed="2026-03-02", root="Camera had been taken down for works and not remounted.", source="Internal audit", auditor="T. Walsh", desc="A loading-bay camera in the Spain entity was offline. It has been remounted and added to the monitoring checklist."),
    # --- Closed late (to keep on-time rate realistic, not perfect) ---
    dict(id="IA-2025-016", title="Supplier agreement missing information-security clauses", typ="NC", sev="High", control="5.20", entity="United Kingdom", owner="OWN-11", raised="2025-01-21", target="2025-04-21", status="Closed", closed="2025-06-18", root="Legal review queue was long and the finding was not escalated.", source="Internal audit", auditor="T. Walsh", desc="A supplier agreement used in the United Kingdom entity lacked the standard information-security clauses. Clauses were added after the target date."),
    dict(id="IA-2025-017", title="Privileged utility use not logged", typ="NC", sev="Medium", control="8.18", entity="Germany", owner="OWN-09", raised="2025-03-18", target="2025-06-18", status="Closed", closed="2025-08-07", root="Platform limitation; a compensating control was designed late.", source="Internal audit", auditor="T. Walsh", desc="Use of a privileged utility in the Germany entity was not being logged. A compensating control was put in place after the target."),
    dict(id="IA-2025-018", title="Threat-intelligence feed not reviewed", typ="OFI", sev="Low", control="5.7", entity="Group", owner="OWN-01", raised="2025-04-29", target="2025-07-29", status="Closed", closed="2025-09-16", root="Ownership of the review was unclear.", source="Internal audit", auditor="T. Walsh", desc="The Group threat-intelligence feed was being received but not reviewed. A weekly review is now assigned."),
    dict(id="IA-2025-019", title="Data-deletion request process not tested", typ="Gap", sev="Medium", control="8.10", entity="France", owner="OWN-10", raised="2025-06-17", target="2025-09-17", status="Closed", closed="2025-11-11", root="A test case could not be agreed between teams.", source="Internal audit", auditor="T. Walsh", desc="The information-deletion process in the France entity had never been end-to-end tested. A test was completed after the target date."),
    dict(id="IA-2025-020", title="Project security assessment skipped for a small change", typ="OFI", sev="Medium", control="5.8", entity="Spain", owner="OWN-04", raised="2025-08-27", target="2025-11-27", status="Closed", closed="2026-01-20", root="The project was classified as too small to assess.", source="Internal audit", auditor="T. Walsh", desc="A change in the Spain entity was delivered without the project security assessment required by the standard. The threshold has since been clarified."),
    dict(id="IA-2025-021", title="Evidence of cable-security inspection not retained", typ="OBS", sev="Low", control="7.12", entity="United Kingdom", owner="OWN-02", raised="2025-09-24", target="2025-12-24", status="Closed", closed="2026-02-02", root="Inspections happened but photographs were discarded.", source="Internal audit", auditor="T. Walsh", desc="Cable-security inspections in the United Kingdom entity were not leaving any retained evidence. A simple evidence rule is now in place."),
    # --- More recent mix: open, in progress, closed on time ---
    dict(id="IA-2026-031", title="DLP rule set not covering a new collaboration channel", typ="Gap", sev="Medium", control="8.12", entity="United Kingdom", owner="OWN-02", raised="2026-09-16", target="2026-12-16", status="Open", closed=None, root="Channel was enabled as a pilot outside the standard pattern.", source="Internal audit", auditor="T. Walsh", desc="A new collaboration channel in the United Kingdom entity is not covered by the data-leakage-prevention rules used on the other channels."),
    dict(id="IA-2026-032", title="Monitoring use-cases not defined for a payment system", typ="OFI", sev="Medium", control="8.16", entity="Germany", owner="OWN-08", raised="2026-08-12", target="2026-11-30", status="In Progress", closed=None, root="Use-case catalogue has not been extended to this system.", source="Internal audit", auditor="T. Walsh", desc="Security monitoring in the Germany entity does not yet include documented use-cases for a payment-related system."),
    dict(id="IA-2026-033", title="Environment separation weakened by a shared service account", typ="NC", sev="High", control="8.31", entity="France", owner="OWN-07", raised="2026-09-02", target="2026-11-20", status="Open", closed=None, root="A temporary account was reused and never replaced.", source="Internal audit", auditor="T. Walsh", desc="A shared service account is used in both test and production in the France entity, weakening environment separation."),
    dict(id="IA-2026-034", title="Configuration baseline drift on a subset of endpoints", typ="OFI", sev="Medium", control="8.9", entity="Spain", owner="OWN-05", raised="2026-10-07", target="2027-01-15", status="Open", closed=None, root="A local administrator exception is still in place.", source="Internal audit", auditor="T. Walsh", desc="A subset of endpoints in the Spain entity has drifted from the standard configuration baseline."),
    dict(id="IA-2026-035", title="Intellectual-property notice missing from a contractor pack", typ="OBS", sev="Low", control="5.32", entity="Group", owner="OWN-11", raised="2026-10-14", target="2027-01-14", status="Open", closed=None, root="Pack was last updated two years ago.", source="Internal audit", auditor="T. Walsh", desc="The standard contractor pack at Group level does not include the current intellectual-property notice."),
    dict(id="IA-2026-036", title="Event-reporting channel not advertised in a local language", typ="OFI", sev="Low", control="6.8", entity="Spain", owner="OWN-04", raised="2026-10-21", target="2027-01-21", status="Open", closed=None, root="Only the English poster was issued.", source="Internal audit", auditor="T. Walsh", desc="The information-security event-reporting channel is not advertised in the local language in the Spain entity."),
    dict(id="IA-2026-037", title="Management responsibility statement not signed this year", typ="Gap", sev="Low", control="5.4", entity="Germany", owner="OWN-08", raised="2026-03-25", target="2026-06-25", status="Closed", closed="2026-06-18", root="The annual sign-off was missed after a leadership change.", source="Internal audit", auditor="T. Walsh", desc="The annual management-responsibility statement for the Germany entity had not been signed. It has now been completed."),
    dict(id="IA-2026-038", title="Secure coding checklist not used on a recent release", typ="OFI", sev="Medium", control="8.28", entity="United Kingdom", owner="OWN-02", raised="2026-05-13", target="2026-08-13", status="Closed", closed="2026-08-06", root="The release was treated as a configuration change only.", source="Internal audit", auditor="T. Walsh", desc="A recent release in the United Kingdom entity did not use the secure coding checklist. The definition of a release has been clarified."),
    dict(id="IA-2026-039", title="Contact list for authorities out of date", typ="OBS", sev="Low", control="5.5", entity="Group", owner="OWN-01", raised="2026-04-22", target="2026-07-22", status="Closed", closed="2026-07-15", root="The list is stored in a document that is rarely opened.", source="Internal audit", auditor="T. Walsh", desc="The Group list of contacts for authorities included a retired role. It has been updated and placed on an annual review."),
    dict(id="IA-2026-040", title="Audit-testing protection procedure not briefed to a new auditor", typ="OBS", sev="Low", control="8.34", entity="France", owner="OWN-12", raised="2026-10-28", target="2027-01-28", status="Open", closed=None, root="Induction for visiting auditors is informal.", source="Internal audit", auditor="T. Walsh", desc="A visiting auditor in the France entity was not briefed on the procedure for protecting information systems during audit testing."),
]

assert len({f["id"] for f in RAW_FINDINGS}) == len(RAW_FINDINGS), "duplicate finding ids"
assert len(RAW_FINDINGS) >= 55


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    y, m, d = (int(p) for p in value.split("-"))
    return date(y, m, d)


def build_findings() -> list[dict]:
    rows = []
    for raw in RAW_FINDINGS:
        control_id = raw["control"]
        theme = CONTROL_TO_THEME[control_id]
        owner = OWNER_BY_ID[raw["owner"]]
        # Group-level findings stay on Group so ownership and entity remain honest.
        entity = raw["entity"]
        rows.append(
            {
                "Finding_ID": raw["id"],
                "Finding_Title": raw["title"],
                "Finding_Type": raw["typ"],
                "Severity": raw["sev"],
                "Control_ID": control_id,
                "Entity": entity,
                "Owner_ID": owner["id"],
                "Owner_Name": owner["name"],
                "Raised_Date": parse_date(raw["raised"]),
                "Target_Date": parse_date(raw["target"]),
                "Status": raw["status"],
                "Closed_Date": parse_date(raw["closed"]),
                "Risk_Theme_ID": theme["id"],
                "Risk_Theme": theme["name"],
                "Description": raw["desc"],
                "Root_Cause": raw["root"],
                "Source": raw["source"],
                "Auditor": raw["auditor"],
                "Data_Flag": DATA_FLAG,
            }
        )
    return rows


ENTITIES = [
    ("UK", "United Kingdom"),
    ("Spain", "Spain"),
    ("France", "France"),
    ("Germany", "Germany"),
]

# Explicit low-maturity cells that should coincide with open NCs (rule 3).
LOW_MATURITY = {
    ("8.5", "United Kingdom"): 2,
    ("8.5", "France"): 2,
    ("8.5", "Spain"): 1,
    ("5.19", "United Kingdom"): 2,
    ("5.19", "Germany"): 2,
    ("8.8", "Spain"): 2,
    ("8.8", "France"): 1,
    ("8.2", "United Kingdom"): 2,
    ("5.23", "Germany"): 2,
    ("8.13", "United Kingdom"): 2,
    ("8.31", "France"): 2,
    ("8.26", "United Kingdom"): 2,
}

LINKED_RISKS = {
    ("8.5", "United Kingdom"): "R-014",
    ("8.5", "France"): "R-014",
    ("8.5", "Spain"): "R-014",
    ("5.19", "United Kingdom"): "R-021",
    ("5.19", "Germany"): "R-021",
}


def build_maturity(findings: list[dict]) -> list[dict]:
    open_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for f in findings:
        if f["Status"] in {"Open", "In Progress"} and f["Entity"] != "Group":
            if f["Finding_Type"] == "NC":
                open_counts[(f["Control_ID"], f["Entity"], "NC")] += 1
            elif f["Finding_Type"] == "OFI":
                open_counts[(f["Control_ID"], f["Entity"], "OFI")] += 1

    rng = random.Random(27001)
    rows = []
    for cid, name, annex in CONTROLS:
        row = {"Control_ID": cid, "Control_Name": name, "Annex_Category": annex}
        for code, entity in ENTITIES:
            key = (cid, entity)
            if key in LOW_MATURITY:
                maturity = LOW_MATURITY[key]
            else:
                # Deterministic but varied 3–5, slightly lower on technical controls.
                base = 4 if annex in {"Organizational", "People", "Physical"} else 3
                maturity = min(5, max(3, base + rng.choice([-1, 0, 0, 1, 1])))
            row[f"{code}_Maturity"] = maturity
            row[f"{code}_Open_NC"] = open_counts[(cid, entity, "NC")]
            row[f"{code}_Open_OFI"] = open_counts[(cid, entity, "OFI")]
            row[f"{code}_Linked_Risk"] = LINKED_RISKS.get(key, "")
        rows.append(row)
    return rows


def build_theme_rows() -> list[dict]:
    rows = []
    for cid, name, annex in CONTROLS:
        theme = CONTROL_TO_THEME[cid]
        rows.append(
            {
                "Control_ID": cid,
                "Control_Name": name,
                "Annex_Category": annex,
                "Risk_Theme_ID": theme["id"],
                "Risk_Theme": theme["name"],
                "Theme_Description": theme["description"],
                "Default_Likelihood": theme["likelihood"],
                "Default_Impact": theme["impact"],
                "Data_Flag": DATA_FLAG,
            }
        )
    return rows


def build_owner_rows() -> list[dict]:
    return [
        {
            "Owner_ID": o["id"],
            "Owner_Name": o["name"],
            "Role": o["role"],
            "Entity": o["entity"],
            "Function": o["function"],
            "Email": o["email"],
            "Line_Manager": o["manager"],
            "Data_Flag": DATA_FLAG,
        }
        for o in OWNERS
    ]


FINDINGS_COLS = [
    "Finding_ID", "Finding_Title", "Finding_Type", "Severity", "Control_ID",
    "Entity", "Owner_ID", "Owner_Name", "Raised_Date", "Target_Date", "Status",
    "Closed_Date", "Risk_Theme_ID", "Risk_Theme", "Description", "Root_Cause",
    "Source", "Auditor", "Data_Flag",
]
MATURITY_COLS = (
    ["Control_ID", "Control_Name", "Annex_Category"]
    + [
        f"{code}_{metric}"
        for code, _ in ENTITIES
        for metric in ("Maturity", "Open_NC", "Open_OFI", "Linked_Risk")
    ]
)
THEME_COLS = [
    "Control_ID", "Control_Name", "Annex_Category", "Risk_Theme_ID", "Risk_Theme",
    "Theme_Description", "Default_Likelihood", "Default_Impact", "Data_Flag",
]
OWNER_COLS = [
    "Owner_ID", "Owner_Name", "Role", "Entity", "Function", "Email",
    "Line_Manager", "Data_Flag",
]


def _write_csv(path: Path, cols: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = {}
            for col in cols:
                val = row.get(col, "")
                if isinstance(val, date):
                    out[col] = val.isoformat()
                elif val is None:
                    out[col] = ""
                else:
                    out[col] = val
            writer.writerow(out)


def _style_sheet(ws, cols: list[str], n_rows: int, date_cols: set[str] | None = None) -> None:
    date_cols = date_cols or set()
    for col_idx, name in enumerate(cols, start=1):
        cell = ws.cell(1, col_idx, name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        cell.border = THIN
    for r in range(2, n_rows + 2):
        for c, name in enumerate(cols, start=1):
            cell = ws.cell(r, c)
            cell.font = BODY_FONT
            cell.border = THIN
            cell.alignment = WRAP if name in {"Description", "Root_Cause", "Theme_Description", "Finding_Title", "Control_Name"} else LEFT
            if name in date_cols and cell.value:
                cell.number_format = "YYYY-MM-DD"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{n_rows + 1}"
    ws.row_dimensions[1].height = 22
    widths = {
        "Finding_ID": 14, "Finding_Title": 52, "Finding_Type": 12, "Severity": 12,
        "Control_ID": 12, "Control_Name": 56, "Annex_Category": 16, "Entity": 18,
        "Owner_ID": 12, "Owner_Name": 16, "Raised_Date": 14, "Target_Date": 14,
        "Status": 14, "Closed_Date": 14, "Risk_Theme_ID": 14, "Risk_Theme": 36,
        "Description": 70, "Root_Cause": 44, "Source": 20, "Auditor": 14,
        "Data_Flag": 18, "Theme_Description": 70, "Default_Likelihood": 18,
        "Default_Impact": 16, "Role": 36, "Function": 22, "Email": 26,
        "Line_Manager": 24,
    }
    for col_idx, name in enumerate(cols, start=1):
        default = 14
        if name.endswith("_Maturity") or name.endswith("_Open_NC") or name.endswith("_Open_OFI"):
            default = 14
        elif name.endswith("_Linked_Risk"):
            default = 16
        ws.column_dimensions[get_column_letter(col_idx)].width = widths.get(name, default)


def _add_rows(ws, cols: list[str], rows: list[dict]) -> None:
    for r, row in enumerate(rows, start=2):
        for c, name in enumerate(cols, start=1):
            val = row.get(name, "")
            if val is None:
                val = ""
            ws.cell(r, c, val)


def write_workbook(findings, maturity, themes, owners) -> None:
    wb = Workbook()
    wb.properties.title = "Continual Improvement Plan — fictional sample"
    wb.properties.subject = "FICTIONAL SAMPLE DATA — do not use as live evidence"
    wb.properties.creator = "GRC Power BI dashboard template"
    wb.properties.description = (
        "Fictional sample workbook for the GRC Power BI dashboard template. "
        "Every row is flagged 'Fictional sample'. It is not a real organisation."
    )
    wb.calculation = CalcProperties(calcMode="auto")

    ws1 = wb.active
    ws1.title = "Internal Audit Findings"
    ws1.append(FINDINGS_COLS)
    _add_rows(ws1, FINDINGS_COLS, findings)
    _style_sheet(ws1, FINDINGS_COLS, len(findings), {"Raised_Date", "Target_Date", "Closed_Date"})
    dv_type = DataValidation(type="list", formula1='"NC,OFI,Gap,OBS"', allow_blank=False)
    dv_sev = DataValidation(type="list", formula1='"Critical,High,Medium,Low"', allow_blank=False)
    dv_status = DataValidation(type="list", formula1='"Open,In Progress,Closed"', allow_blank=False)
    for dv, col in ((dv_type, "C"), (dv_sev, "D"), (dv_status, "K")):
        dv.add(f"{col}2:{col}{len(findings) + 1}")
        ws1.add_data_validation(dv)

    ws2 = wb.create_sheet("Control Maturity")
    ws2.append(MATURITY_COLS)
    _add_rows(ws2, MATURITY_COLS, maturity)
    _style_sheet(ws2, MATURITY_COLS, len(maturity))

    ws3 = wb.create_sheet("Risk Theme Mapping")
    ws3.append(THEME_COLS)
    _add_rows(ws3, THEME_COLS, themes)
    _style_sheet(ws3, THEME_COLS, len(themes))

    ws4 = wb.create_sheet("Owners")
    ws4.append(OWNER_COLS)
    _add_rows(ws4, OWNER_COLS, owners)
    _style_sheet(ws4, OWNER_COLS, len(owners))

    for ws in (ws1, ws2, ws3, ws4):
        ws.sheet_properties.tabColor = NAVY
        ws.oddHeader.left.text = "FICTIONAL SAMPLE DATA — not live evidence"
        ws.oddFooter.left.text = "GRC Power BI dashboard template"

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)


def summarise(findings: list[dict]) -> None:
    from collections import Counter

    types = Counter(f["Finding_Type"] for f in findings)
    status = Counter(f["Status"] for f in findings)
    closed = [f for f in findings if f["Status"] == "Closed"]
    on_time = [
        f for f in closed
        if f["Closed_Date"] and f["Target_Date"] and f["Closed_Date"] <= f["Target_Date"]
    ]
    days = [
        (f["Closed_Date"] - f["Raised_Date"]).days
        for f in closed
        if f["Closed_Date"] and f["Raised_Date"]
    ]
    today = date(2026, 11, 11)
    open_items = [f for f in findings if f["Status"] in {"Open", "In Progress"}]
    overdue = [f for f in open_items if f["Target_Date"] and f["Target_Date"] < today]
    print(f"Findings: {len(findings)}")
    print(f"  Types: {dict(types)}")
    print(f"  Status: {dict(status)}")
    print(f"  Closed on time: {len(on_time)}/{len(closed)} = {len(on_time)/len(closed):.1%}")
    print(f"  Avg days to close: {sum(days)/len(days):.1f}")
    print(f"  Open/in progress: {len(open_items)}; overdue as at {today}: {len(overdue)}")


def main() -> None:
    if len(CONTROLS) != 93:
        raise SystemExit(f"Expected 93 controls, got {len(CONTROLS)}")
    findings = build_findings()
    maturity = build_maturity(findings)
    themes = build_theme_rows()
    owners = build_owner_rows()
    write_workbook(findings, maturity, themes, owners)
    _write_csv(OUT_DIR / "findings.csv", FINDINGS_COLS, findings)
    _write_csv(OUT_DIR / "control_maturity.csv", MATURITY_COLS, maturity)
    _write_csv(OUT_DIR / "risk_theme_mapping.csv", THEME_COLS, themes)
    _write_csv(OUT_DIR / "owners.csv", OWNER_COLS, owners)
    summarise(findings)
    print(f"Wrote {OUT_XLSX}")
    print(f"Wrote CSV copies in {OUT_DIR}")


if __name__ == "__main__":
    main()
