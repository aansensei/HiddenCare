# Main interactive web application entrypoint for Hugging Face Spaces.
# Styled according to the Macro Event Lab design system and anti-slop guidelines.

from pathlib import Path
import os
import json
import inspect
import gradio as gr
import pandas as pd

# Hugging Face ZeroGPU compatibility marker
try:
    import spaces

    @spaces.GPU
    def _zerogpu_marker():
        return True
except (ImportError, Exception):
    pass

from src.clinical_charts import (
    build_capacity_gain_chart,
    build_nns_chart,
    build_margin_swap_comparison_chart,
    build_joint_ranking_scatter,
    build_equity_bar_chart,
    build_decision_curve_plot,
)
from src.html_components import (
    get_base64_image,
    render_masthead_html,
    render_site_guide_html,
    render_hero_summary_cards,
    render_simulator_kpi_cards,
    render_margin_table_html,
    render_equity_callout_html,
    render_economic_ledger_html,
    render_about_page_html,
    render_footer_html,
)

PROJECT_ROOT = Path(__file__).resolve().parent
CSS_PATH = PROJECT_ROOT / "assets" / "clinical_theme.css"
CLINICAL_CSS = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""
FAVICON_PATH = PROJECT_ROOT / "assets" / "favicon.ico"
FAVICON_ICO_URI = get_base64_image("favicon.ico", "image/x-icon")
FAVICON_PNG_URI = get_base64_image("favicon-96x96.png", "image/png")

# Metadata for SEO, Google scrape, Open Graph, and Twitter Cards
HEAD_HTML = f"""
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>HiddenCare | Algorithmic Triage & Health Equity Lab</title>
<link rel="icon" type="image/x-icon" href="{FAVICON_ICO_URI}">
<link rel="icon" type="image/png" sizes="96x96" href="{FAVICON_PNG_URI}">
<link rel="apple-touch-icon" href="{FAVICON_PNG_URI}">
<meta name="title" content="HiddenCare | Algorithmic Triage & Health Equity Lab">
<meta name="description" content="An empirical investigation into proxy outcome bias in algorithmic screening using CDC NHANES Continuous Biomonitoring data (N = 12,459). Demonstrating how proxy training labels systematically reorder screening queues and deepen disparities for underserved populations.">
<meta name="keywords" content="Cao Thien An Nguyen, Thien An Nguyen, aansensei, aansensei.dev, aansensei GitHub, aansensei Hugging Face, Cao Thien An Nguyen UW Madison, Cao Thien An Nguyen Data Science, Cao Thien An Nguyen Economics, An Nguyen HiddenCare, aansensei HiddenCare, nguyencaothienan937, HiddenCare, HiddenCare Lab, When Training Labels Change Who Gets Screened, Temporal evaluation of diagnosis-based versus biomarker-augmented labels in NHANES, Algorithmic Triage & Health Equity Lab, HiddenCare Research Poster, HiddenCare NHANES, Algorithmic Triage Simulator, 61-Patient Margin Inspector, 61-Person Boundary Swap Proof, Proxy Outcome Bias, Proxy Label Bias, Algorithmic Fairness in Healthcare, Health Equity Machine Learning, Healthcare Access Disparities, Algorithmic Bias in Population Health, Diagnostic Access Disparities, Undiagnosed Population Misclassification, Medical Under-diagnosis Bias, Healthcare Utilization Proxies, Electronic Health Record Bias, EHR Proxy Outcome Bias, Health Equity Subgroup Audit, Uninsured Healthcare Disparities, PIR Poverty Income Ratio Audit, Population Screening Triage, Diabetes Screening Machine Learning, Type 2 Diabetes Screening Algorithm, Undiagnosed Diabetes Screening, Venous HbA1c Glycated Hemoglobin, Venous Blood Biomonitoring, HbA1c 6.5 Screening Criterion, Biomarker-Augmented Training Labels, Self-Reported Diabetes Diagnosis, Non-Invasive Predictors Screening, Anthropometric Screening Predictors, BMI Waist Circumference Screening, Community Health Screening Triage, Finite Screening Capacity Allocation, Targeted Screening Queue, CDC NHANES Microdata, National Health and Nutrition Examination Survey, CDC National Center for Health Statistics, NCHS Continuous Biomonitoring, NHANES 2017-2020 Pre-pandemic, NHANES 2021-2023 Post-pandemic, P_DEMO Demographics, P_DIQ Diabetes Questionnaire, P_GHB Glycohemoglobin Laboratory, P_BMX Body Measures, P_HIQ Health Insurance Coverage, DEMO_L 2021-2023, DIQ_L 2021-2023, GHB_L 2021-2023, SAS Transport XPT Files, Taylor Series Linearization, Complex Survey Variance Estimation, WTPH2YR Phlebotomy Weights, WTMEC2YR Examination Weights, Multistage Clustered Sampling Design, Masked Primary Sampling Units PSU, Masked Strata Variance, L2-Regularized Logistic Regression, Cross-Validated Regularization Penalty C, Positive Predictive Value PPV, Sensitivity at Fixed Capacity, Numbers Needed to Screen NNS, Random Forest Screening Robustness, HistGradientBoosting Robustness, Paired-Selection Queue Analysis, Decision Curve Analysis DCA, Net Monetary Benefit NMB, Health Economics Screening Policy, Screening Budget Optimization, Early Intervention Cost Savings, Diagnostic Test Kit Costs, Cost-Effectiveness of Triage Algorithms, Value of Information in Screening, Universal vs Targeted Screening DCA, Resource-Constrained Healthcare Triage, Embedded DuckDB Lakehouse, Pandera Data Validation Contracts, Population Stability Index PSI, Schema Drift Detection Lakehouse, Reproducible Epidemiological Pipeline, UW-Madison Data Science Portfolio, Biostatistics Graduate Fellowship Portfolio, Healthcare Machine Learning Portfolio">
<meta name="author" content="Cao Thien An Nguyen">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

<!-- Google Scholar Metadata (Highwire Press Standards) -->
<meta name="citation_title" content="When Training Labels Change Who Gets Screened: Temporal Evaluation of Diagnosis-Based Versus Biomarker-Augmented Labels in NHANES">
<meta name="citation_author" content="Nguyen, Cao Thien An">
<meta name="citation_publication_date" content="2026/11">
<meta name="citation_technical_report_institution" content="University of Wisconsin-Madison">
<meta name="citation_online_date" content="2026/11/08">
<meta name="citation_language" content="en">
<meta name="citation_abstract" content="Population screening triage algorithms frequently train on self-reported diagnoses or electronic records, potentially marking unrecorded disease negative when individuals face healthcare access barriers. In CDC NHANES microdata (N = 12,459), augmenting administrative diagnosis labels with objective venous HbA1c biomonitoring alters triage queue prioritization and identifies two additional potential cases at identical 20% screening capacity.">
<meta name="citation_pdf_url" content="https://aansensei.dev/hiddencare/assets/poster.pdf">

<!-- Schema.org JSON-LD Structured Data for Google Rich Results & Google Scholar -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "When Training Labels Change Who Gets Screened: Temporal Evaluation of Diagnosis-Based Versus Biomarker-Augmented Labels in NHANES",
  "name": "HiddenCare: Algorithmic Triage & Health Equity Lab",
  "author": {{
    "@type": "Person",
    "name": "Cao Thien An Nguyen",
    "alternateName": ["An Nguyen", "aansensei"],
    "url": "https://aansensei.dev",
    "sameAs": [
      "https://github.com/aansensei",
      "https://linkedin.com/in/cao-thien-an-nguyen",
      "https://huggingface.co/aansensei"
    ],
    "affiliation": {{
      "@type": "EducationalOrganization",
      "name": "University of Wisconsin–Madison"
    }}
  }},
  "datePublished": "2026-11-08",
  "description": "An empirical investigation into proxy outcome bias in algorithmic screening using CDC NHANES Continuous Biomonitoring data (N = 12,459). Demonstrating how proxy training labels systematically reorder screening queues and deepen disparities for underserved populations.",
  "keywords": "Proxy Outcome Bias, Algorithmic Triage, Health Equity, CDC NHANES, Machine Learning, Diabetes Screening, Health Economics",
  "url": "https://aansensei.dev/hiddencare/",
  "publisher": {{
    "@type": "Organization",
    "name": "HiddenCare Research Initiative"
  }}
}}
</script>

<meta property="og:type" content="website">
<meta property="og:url" content="https://aansensei-hiddencare.hf.space">
<meta property="og:site_name" content="HiddenCare">
<meta property="og:title" content="HiddenCare | Algorithmic Triage & Health Equity Lab">
<meta property="og:description" content="An empirical investigation of proxy outcome bias across N = 12,459 CDC NHANES participants. Discover how clinical proxy labels bias screening allocation.">
<meta property="og:image" content="https://aansensei.dev/assets/images/preview.png">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://aansensei-hiddencare.hf.space">
<meta name="twitter:title" content="HiddenCare | Algorithmic Triage & Health Equity Lab">
<meta name="twitter:description" content="Evaluating proxy outcome bias in algorithmic triage across N = 12,459 CDC NHANES participants.">
<meta name="twitter:image" content="https://aansensei.dev/assets/images/preview.png">
<meta name="twitter:creator" content="@aansensei">
<meta name="author" content="Cao Thien An Nguyen">
<meta name="copyright" content="Copyright 2026 Cao Thien An Nguyen">
<meta name="github" content="https://github.com/aansensei">
<style>
  @media (min-width: 1025px) {{
    #hc-toc-rail {{
      display: flex !important;
    }}
    #hc-mobile-toc-fab,
    #hc-mobile-toc-scrim,
    #hc-mobile-toc-sheet {{
      display: none !important;
    }}
  }}
  @media (max-width: 1024px) {{
    #hc-toc-rail {{
      display: none !important;
    }}
    #hc-mobile-toc-fab {{
      display: inline-flex !important;
    }}
  }}
</style>
"""

# JavaScript to enforce light theme, favicon and tab title dynamically
FORCE_LIGHT_JS = f"""
function() {{
    if (typeof document !== 'undefined') {{
        document.body.classList.remove('dark');
        if (document.documentElement) document.documentElement.classList.remove('dark');
        const container = document.querySelector('.gradio-container');
        if (container) {{
            container.classList.remove('dark');
            if (window.innerWidth > 640) {{
                container.style.setProperty('max-width', '1560px', 'important');
                container.style.setProperty('width', '95%', 'important');
                container.style.setProperty('margin', '0 auto', 'important');
            }} else {{
                container.style.setProperty('max-width', '100%', 'important');
                container.style.setProperty('width', '100%', 'important');
                container.style.setProperty('margin', '0', 'important');
            }}
            container.style.setProperty('background-color', '#ffffff', 'important');
        }}

        const pageTitle = "HiddenCare | Algorithmic Triage & Health Equity Lab";
        if (document.title !== pageTitle) {{
            document.title = pageTitle;
        }}

        const removeGradioFooter = function() {{
            const footers = document.querySelectorAll('footer:not(.site-footer)');
            footers.forEach(function(f) {{
                if (!f.classList.contains('site-footer') && !f.closest('.site-footer')) {{
                    f.style.setProperty('display', 'none', 'important');
                    f.remove();
                }}
            }});
        }};
        removeGradioFooter();
        setTimeout(removeGradioFooter, 200);
        setTimeout(removeGradioFooter, 800);
        setTimeout(removeGradioFooter, 2000);

        const initBackToTop = function() {{
            if (document.getElementById('hc-back-to-top')) return;
            const btn = document.createElement('button');
            btn.id = 'hc-back-to-top';
            btn.setAttribute('type', 'button');
            btn.setAttribute('aria-label', 'Return to top of page');
            btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg><span>Top</span>';
            btn.onclick = function() {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }};
            document.body.appendChild(btn);

            const handleScroll = function() {{
                if (window.scrollY > 300) {{
                    btn.classList.add('visible');
                }} else {{
                    btn.classList.remove('visible');
                }}
            }};
            window.addEventListener('scroll', handleScroll, {{ passive: true }});
            handleScroll();
        }};
        initBackToTop();
        setTimeout(initBackToTop, 400);
        setTimeout(initBackToTop, 1200);

        const initTocRail = function() {{
            // khoi tao ray cham tren may tinh
            let rail = document.getElementById('hc-toc-rail');
            if (!rail) {{
                rail = document.createElement('nav');
                rail.id = 'hc-toc-rail';
                rail.setAttribute('aria-label', 'Table of Contents Navigation');
                document.body.appendChild(rail);
            }}

            // khoi tao nut vien thuoc tren di dong
            let fab = document.getElementById('hc-mobile-toc-fab');
            if (!fab) {{
                fab = document.createElement('button');
                fab.id = 'hc-mobile-toc-fab';
                fab.setAttribute('type', 'button');
                fab.setAttribute('aria-label', 'Open table of contents');
                fab.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg><span class="hc-fab-count" style="font-family: var(--font-serif); font-size: 16px; font-weight: 600; color: #0284c7; letter-spacing: 0.04em; margin-left: 6px;">1 / 5</span>';
                document.body.appendChild(fab);
            }}

            // khoi tao man mo phu
            let scrim = document.getElementById('hc-mobile-toc-scrim');
            if (!scrim) {{
                scrim = document.createElement('div');
                scrim.id = 'hc-mobile-toc-scrim';
                document.body.appendChild(scrim);
            }}

            // khoi tao ngan keo truot tu duoi len
            let sheet = document.getElementById('hc-mobile-toc-sheet');
            if (!sheet) {{
                sheet = document.createElement('div');
                sheet.id = 'hc-mobile-toc-sheet';
                sheet.innerHTML = '<div class="hc-drawer-header"><span class="hc-drawer-title">CONTENTS</span><button id="hc-drawer-close" aria-label="Close" type="button">&times;</button></div><div id="hc-drawer-items"></div>';
                document.body.appendChild(sheet);

                scrim.onclick = function() {{
                    scrim.classList.remove('is-open');
                    sheet.classList.remove('is-open');
                }};
                const closeBtn = sheet.querySelector('#hc-drawer-close');
                if (closeBtn) {{
                    closeBtn.onclick = function() {{
                        scrim.classList.remove('is-open');
                        sheet.classList.remove('is-open');
                    }};
                }}
                fab.onclick = function() {{
                    if (sheet.classList.contains('is-open')) {{
                        scrim.classList.remove('is-open');
                        sheet.classList.remove('is-open');
                    }} else {{
                        scrim.classList.add('is-open');
                        sheet.classList.add('is-open');
                    }}
                }};
            }}

            // dong bo an hien theo do rong man hinh
            const syncVisibility = function() {{
                if (window.innerWidth >= 1025) {{
                    rail.style.setProperty('display', 'flex', 'important');
                    fab.style.setProperty('display', 'none', 'important');
                    scrim.style.setProperty('display', 'none', 'important');
                    sheet.style.setProperty('display', 'none', 'important');
                }} else {{
                    rail.style.setProperty('display', 'none', 'important');
                    fab.style.setProperty('display', 'inline-flex', 'important');
                    scrim.style.removeProperty('display');
                    sheet.style.removeProperty('display');
                }}
            }};
            syncVisibility();
            window.addEventListener('resize', syncVisibility, {{ passive: true }});

            // cap nhat danh sach cac muc
            const updateSections = function() {{
                const sections = Array.from(document.querySelectorAll('[data-toc]')).filter(function(el) {{
                    return el.offsetParent !== null;
                }});

                // ve lai cham tren may tinh
                rail.innerHTML = '';
                sections.forEach(function(sec, idx) {{
                    const item = document.createElement('div');
                    item.className = 'hc-toc-item' + (idx === 0 ? ' active' : '');
                    item.setAttribute('role', 'button');
                    item.setAttribute('aria-label', sec.getAttribute('data-toc'));

                    const dot = document.createElement('div');
                    dot.className = 'hc-toc-dot';
                    item.appendChild(dot);

                    const tooltip = document.createElement('div');
                    tooltip.className = 'hc-toc-tooltip';
                    const rawText = sec.getAttribute('data-toc') || '';
                    if (rawText.indexOf('•') !== -1) {{
                        const parts = rawText.split('•');
                        tooltip.innerHTML = '<span style="color: #0284c7; font-weight: 700; margin-right: 6px;">' + parts[0].trim() + '</span><span style="color: #0f172a;">' + parts[1].trim() + '</span>';
                    }} else {{
                        tooltip.textContent = rawText;
                    }}
                    item.appendChild(tooltip);

                    item.onclick = function() {{
                        if (sec.id === 'sec-to-methodology') {{
                            window.switchToAboutTab && window.switchToAboutTab();
                        }} else {{
                            sec.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                        }}
                    }};
                    rail.appendChild(item);
                }});

                // ve lai danh sach trong ngan keo di dong
                const drawerItems = sheet.querySelector('#hc-drawer-items');
                if (drawerItems) {{
                    drawerItems.innerHTML = '';
                    sections.forEach(function(sec, idx) {{
                        const dItem = document.createElement('div');
                        dItem.className = 'hc-drawer-item' + (idx === 0 ? ' is-active' : '');
                        const rawText = sec.getAttribute('data-toc') || '';
                        let cleanLabel = rawText;
                        if (rawText.indexOf('•') !== -1) {{
                            const parts = rawText.split('•');
                            cleanLabel = parts[0].trim() + '. ' + parts[1].trim();
                        }}
                        dItem.textContent = cleanLabel;
                        dItem.onclick = function() {{
                            scrim.classList.remove('is-open');
                            sheet.classList.remove('is-open');
                            if (sec.id === 'sec-to-methodology') {{
                                window.switchToAboutTab && window.switchToAboutTab();
                            }} else {{
                                sec.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                            }}
                        }};
                        drawerItems.appendChild(dItem);
                    }});
                }}

                // cap nhat so luong tren nut vien thuoc
                const countSpan = fab.querySelector('.hc-fab-count');
                if (countSpan && sections.length > 0) {{
                    countSpan.textContent = '1 / ' + sections.length;
                }}
            }};

            updateSections();

            // theo doi vi tri cuon
            const handleScrollSpy = function() {{
                const sections = Array.from(document.querySelectorAll('[data-toc]')).filter(function(el) {{
                    return el.offsetParent !== null;
                }});
                const items = rail.querySelectorAll('.hc-toc-item');
                const dItems = sheet.querySelectorAll('.hc-drawer-item');
                if (sections.length === 0) return;

                const scrollPos = window.scrollY + window.innerHeight * 0.35;
                let activeIdx = 0;
                sections.forEach(function(sec, i) {{
                    const top = sec.getBoundingClientRect().top + window.scrollY;
                    if (scrollPos >= top) {{
                        activeIdx = i;
                    }}
                }});

                // cap nhat cham may tinh
                items.forEach(function(it, i) {{
                    if (i === activeIdx) it.classList.add('active');
                    else it.classList.remove('active');
                }});

                // cap nhat ngan keo di dong
                dItems.forEach(function(dit, i) {{
                    if (i === activeIdx) dit.classList.add('is-active');
                    else dit.classList.remove('is-active');
                }});

                // cap nhat nut vien thuoc di dong
                const countSpan = fab.querySelector('.hc-fab-count');
                if (countSpan && sections.length > 0) {{
                    countSpan.textContent = (activeIdx + 1) + ' / ' + sections.length;
                }}
            }};

            window.addEventListener('scroll', handleScrollSpy, {{ passive: true }});
            document.querySelectorAll('button[role="tab"]').forEach(function(tab) {{
                tab.addEventListener('click', function() {{
                    setTimeout(function() {{
                        updateSections();
                        handleScrollSpy();
                    }}, 150);
                }});
            }});
        }};
        initTocRail();
        setTimeout(initTocRail, 500);
        setTimeout(initTocRail, 1500);

        
        window.switchToAboutTab = function() {{
            const tabs = document.querySelectorAll('#hc-main-tabs button[role="tab"]');
            if (tabs.length > 1) {{
                tabs[1].click();
                setTimeout(function() {{
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}, 100);
            }}
        }};

        
        window.copyApaCitation = function() {{
            const apa = "Nguyen, C. T. A. (2026). When training labels change who gets screened: Temporal evaluation of diagnosis-based versus biomarker-augmented labels in NHANES [Research Poster & Interactive Lab]. University of Wisconsin–Madison. https://aansensei.dev/hiddencare/";
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(apa).then(function() {{
                    const span = document.getElementById('txt-copy-apa');
                    if (span) {{
                        const prev = span.textContent;
                        span.textContent = "Copied to Clipboard!";
                        setTimeout(function() {{ span.textContent = prev; }}, 2200);
                    }}
                }});
            }}
        }};

        window.copyBibtexCitation = function() {{
            const bibtex = `@misc{{nguyen2026hiddencare,\n  author = {{Cao Thien An Nguyen}},\n  title = {{When Training Labels Change Who Gets Screened: Temporal Evaluation of Diagnosis-Based Versus Biomarker-Augmented Labels in NHANES}},\n  year = {{2026}},\n  month = {{November}},\n  howpublished = {{Research Poster & Interactive Lab}},\n  institution = {{University of Wisconsin-Madison}},\n  url = {{https://aansensei.dev/hiddencare/}}\n}}`;
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(bibtex).then(function() {{
                    const span = document.getElementById('txt-copy-bibtex');
                    if (span) {{
                        const prev = span.textContent;
                        span.textContent = "BibTeX Copied!";
                        setTimeout(function() {{ span.textContent = prev; }}, 2200);
                    }}
                }});
            }}
        }};

        window.switchToLabTab = function() {{
            const tabs = document.querySelectorAll('#hc-main-tabs button[role="tab"]');
            if (tabs.length > 0) {{
                tabs[0].click();
                setTimeout(function() {{
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}, 100);
            }}
        }};

        const enhanceTabHeaders = function() {{
            const tabs = document.querySelectorAll('#hc-main-tabs button[role="tab"]');
            if (tabs.length >= 2) {{
                if (!tabs[0].querySelector('.hc-tab-badge')) {{
                    const badge0 = document.createElement('span');
                    badge0.className = 'hc-tab-badge hc-tab-badge--primary';
                    badge0.textContent = 'Simulator & Triage';
                    tabs[0].appendChild(badge0);
                }}
                if (!tabs[1].querySelector('.hc-tab-badge')) {{
                    const badge1 = document.createElement('span');
                    badge1.className = 'hc-tab-badge hc-tab-badge--highlight';
                    badge1.textContent = 'Poster & Sources';
                    tabs[1].appendChild(badge1);
                }}
            }}
        }};
        enhanceTabHeaders();
        setTimeout(enhanceTabHeaders, 300);
        setTimeout(enhanceTabHeaders, 1200);

        const initPosterLightbox = function() {{
            window.openPosterLightbox = function() {{
                const modal = document.getElementById('hc-poster-lightbox');
                if (!modal) return;
                if (modal.parentElement !== document.body) {{
                    document.body.appendChild(modal);
                }}
                modal.style.display = 'flex';
                modal.offsetHeight;
                modal.classList.add('is-open');
                document.body.style.overflow = 'hidden';
                window.addEventListener('keydown', window.handlePosterLightboxKeydown);
                const closeBtn = document.getElementById('hc-poster-lightbox-close');
                if (closeBtn) closeBtn.focus();
            }};

            window.closePosterLightbox = function(e) {{
                if (e && e.stopPropagation) e.stopPropagation();
                const modal = document.getElementById('hc-poster-lightbox');
                if (!modal) return;
                modal.classList.remove('is-open');
                document.body.style.overflow = '';
                window.removeEventListener('keydown', window.handlePosterLightboxKeydown);
                setTimeout(function() {{
                    if (!modal.classList.contains('is-open')) {{
                        modal.style.display = 'none';
                    }}
                }}, 250);
            }};

            window.handlePosterLightboxClick = function(e) {{
                if (e.target.id === 'hc-poster-lightbox' || e.target.classList.contains('hc-modal-backdrop')) {{
                    window.closePosterLightbox(e);
                }}
            }};

            window.handlePosterLightboxKeydown = function(e) {{
                if (e.key === 'Escape' || e.key === 'Esc') {{
                    window.closePosterLightbox(e);
                }}
            }};
        }};
        initPosterLightbox();

        const initReferencesModal = function() {{
            window.openReferencesModal = function() {{
                const modal = document.getElementById('hc-references-modal');
                if (!modal) return;
                if (modal.parentElement !== document.body) {{
                    document.body.appendChild(modal);
                }}
                modal.style.display = 'flex';
                modal.offsetHeight;
                modal.classList.add('is-open');
                document.body.style.overflow = 'hidden';
                window.addEventListener('keydown', window.handleReferencesModalKeydown);
                const closeBtn = document.getElementById('hc-references-modal-close');
                if (closeBtn) closeBtn.focus();
            }};

            window.closeReferencesModal = function(e) {{
                if (e && e.stopPropagation) e.stopPropagation();
                const modal = document.getElementById('hc-references-modal');
                if (!modal) return;
                modal.classList.remove('is-open');
                document.body.style.overflow = '';
                window.removeEventListener('keydown', window.handleReferencesModalKeydown);
                setTimeout(function() {{
                    if (!modal.classList.contains('is-open')) {{
                        modal.style.display = 'none';
                    }}
                }}, 250);
            }};

            window.handleReferencesBackdropClick = function(e) {{
                if (e.target.id === 'hc-references-modal' || e.target.classList.contains('hc-modal-backdrop')) {{
                    window.closeReferencesModal(e);
                }}
            }};

            window.handleReferencesModalKeydown = function(e) {{
                if (e.key === 'Escape' || e.key === 'Esc') {{
                    window.closeReferencesModal(e);
                }}
            }};

            window.copySingleCitation = function(btn, text) {{
                if (navigator.clipboard && navigator.clipboard.writeText) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        const orig = btn.innerText;
                        btn.innerText = 'Copied!';
                        btn.style.color = '#059669';
                        btn.style.borderColor = '#059669';
                        setTimeout(function() {{
                            btn.innerText = orig;
                            btn.style.color = '';
                            btn.style.borderColor = '';
                        }}, 2000);
                    }});
                }}
            }};

            window.copyFullBibliography = function(btn) {{
                const bib = [
                    "1. Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464), 447, 453. https://doi.org/10.1126/science.aax2342",
                    "2. American Diabetes Association. (2024). Classification and diagnosis of diabetes: Standards of care in diabetes: 2024. Diabetes Care, 47(Suppl. 1), S20, S42. https://doi.org/10.2337/dc24-S002",
                    "3. Vickers, A. J., van Calster, B., & Steyerberg, E. W. (2016). Net benefit approaches to the evaluation of prediction models, molecular markers, and diagnostic tests. The BMJ, 352, i6. https://doi.org/10.1136/bmj.i6",
                    "4. Foulds, J. R., Islam, R., Keya, K. N., & Pan, S. (2024). Hierarchical Bayesian models to mitigate systematic disparities in prediction with proxy outcomes. Journal of the Royal Statistical Society: Series A, 189(1), 242, 265. https://doi.org/10.1093/jrsssa/qnae095",
                    "5. National Institute of Diabetes and Digestive and Kidney Diseases. (2022). The A1C test & diabetes. National Institutes of Health. https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test",
                    "6. Ghassemi, M., Oakden-Rayner, L., & Beam, A. L. (2021). The false hope of current approaches to explainable artificial intelligence in health care. The Lancet Digital Health, 3(11), e745, e750. https://doi.org/10.1016/S2589-7500(21)00208-9",
                    "7. Centers for Disease Control and Prevention, National Center for Health Statistics. (2021, 2024). National Health and Nutrition Examination Survey microdata files (2017 to 2023). U.S. Department of Health and Human Services. https://wwwn.cdc.gov/nchs/nhanes/",
                    "8. Heeringa, S. G., West, B. T., & Berglund, P. A. (2017). Applied survey data analysis (2nd ed.). Chapman and Hall/CRC. https://doi.org/10.1201/9781315153278",
                    "9. Nguyen, C. T. A. (2026). When training labels change who gets screened: Temporal evaluation of diagnosis-based versus biomarker-augmented labels in NHANES [Research poster]. University of Wisconsin, Madison. https://aansensei.dev/hiddencare"
                ].join(String.fromCharCode(10, 10));

                if (navigator.clipboard && navigator.clipboard.writeText) {{
                    navigator.clipboard.writeText(bib).then(function() {{
                        const span = btn.querySelector('span');
                        const orig = span ? span.innerText : btn.innerText;
                        if (span) span.innerText = 'Copied Full Bibliography!';
                        else btn.innerText = 'Copied!';
                        btn.style.color = '#059669';
                        btn.style.borderColor = '#059669';
                        setTimeout(function() {{
                            if (span) span.innerText = orig;
                            else btn.innerText = orig;
                            btn.style.color = '';
                            btn.style.borderColor = '';
                        }}, 2200);
                    }});
                }}
            }};
        }};
        initReferencesModal();


        const setFavicons = function() {{
            const icoUri = "{FAVICON_ICO_URI}";
            let links = document.querySelectorAll("link[rel*='icon']");
            if (links.length === 0) {{
                const link = document.createElement('link');
                link.rel = 'icon';
                link.type = 'image/x-icon';
                link.href = icoUri;
                document.head.appendChild(link);
            }} else {{
                links.forEach(function(l) {{
                    l.href = icoUri;
                }});
            }}
        }};
        setFavicons();
        setTimeout(setFavicons, 500);
        setTimeout(setFavicons, 1500);
        setTimeout(setFavicons, 3000);
    }}
}}
"""

clinical_theme = gr.themes.Base(
    primary_hue=gr.themes.colors.sky,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Inter"), "sans-serif"],
).set(
    body_background_fill="#ffffff",
    block_background_fill="#ffffff",
    block_border_color="#dbe7ef",
    body_text_color="#062033",
)

# Load data dictionary for methodology tab.
DICT_PATH = PROJECT_ROOT / "data" / "nhanes_dictionary.json"
dict_records = []
if DICT_PATH.exists():
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dict_records = json.load(f)
dict_df = pd.DataFrame(dict_records)


def on_capacity_change(capacity_pct, cost_test, benefit_early):
    kpi_html = render_simulator_kpi_cards(int(capacity_pct))
    plot_gain = build_capacity_gain_chart(int(capacity_pct))
    plot_nns = build_nns_chart(int(capacity_pct))
    econ_html = render_economic_ledger_html(
        int(capacity_pct), float(cost_test), float(benefit_early)
    )
    return kpi_html, plot_gain, plot_nns, econ_html


def on_margin_filter_change(filter_selection):
    return render_margin_table_html(filter_selection)


def on_economic_param_change(capacity_pct, cost_test, benefit_early):
    return render_economic_ledger_html(
        int(capacity_pct), float(cost_test), float(benefit_early)
    )


# Build the Gradio Application Blocks Layout
blocks_sig = inspect.signature(gr.Blocks.__init__).parameters
blocks_kwargs = {
    "theme": clinical_theme,
    "css": CLINICAL_CSS,
    "js": FORCE_LIGHT_JS,
    "title": "HiddenCare | Algorithmic Triage & Health Equity Lab",
}
if "head" in blocks_sig:
    blocks_kwargs["head"] = HEAD_HTML

with gr.Blocks(**blocks_kwargs) as demo:

    # Header with AanSensei logo, title, and lead (no cheesy quote)
    gr.HTML(render_masthead_html())

    # dieu huong tab
    with gr.Tabs(elem_id="hc-main-tabs"):

        # Tab 1: Interactive Research Lab (Comprehensive Single-Page Study)
        with gr.TabItem("Interactive Research Lab"):
            gr.HTML(render_hero_summary_cards())

            # Section 01: Capacity Allocation Simulator
            gr.HTML("""
            <div class="hc-section-card-header" id="sec-simulation" data-toc="01 • Capacity Simulator" style="margin-top: 28px;">
              <span class="hc-section-kicker">01 / Simulation Engine</span>
              <h2 class="hc-section-title">Screening Queue Triage Under Finite Capacity</h2>
              <p class="hc-section-desc">
                Adjust screening capacity to simulate how proxy-trained versus biomarker-augmented triage prioritizes 
                previously undiagnosed adults (N = 4,698 holdout).
              </p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=8):
                    capacity_slider = gr.Slider(
                        minimum=5,
                        maximum=50,
                        value=20,
                        step=1,
                        label="Screening Budget Capacity (% of Undiagnosed Holdout Cohort, N = 4,698)",
                    )
                with gr.Column(scale=4):
                    gr.Markdown("**Quick Budget Presets:**")
                    with gr.Row():
                        btn_10 = gr.Button("10% Budget", size="sm", elem_classes=["preset-btn"])
                        btn_20 = gr.Button("20% (Primary)", variant="primary", size="sm", elem_classes=["preset-btn", "preset-btn--primary"])
                        btn_30 = gr.Button("30% Budget", size="sm", elem_classes=["preset-btn"])

            sim_kpi_html = gr.HTML(value=render_simulator_kpi_cards(20))

            with gr.Row():
                with gr.Column(scale=6):
                    plot_gain = gr.Plot(value=build_capacity_gain_chart(20))
                    gr.HTML('<p class="hc-chart-caption"><strong>Cumulative yield:</strong> How many latent diabetes cases (HbA1c &ge; 6.5%) are identified as community screening capacity expands from 5% to 50%.<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')
                with gr.Column(scale=6):
                    plot_nns = gr.Plot(value=build_nns_chart(20))
                    gr.HTML('<p class="hc-chart-caption"><strong>Screening efficiency:</strong> Number of diagnostic blood tests needed to find one latent case. Lower values indicate higher testing efficiency.<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')

            # Section 02: The 61-Person Margin Inspector
            gr.HTML("""
            <div class="hc-section-card-header" id="sec-margin" data-toc="02 • 61-Person Margin" style="margin-top: 48px;">
              <span class="hc-section-kicker">02 / Boundary Analysis</span>
              <h2 class="hc-section-title">The 61-Person Margin: Who Swaps at the 20% Cutoff?</h2>
              <p class="hc-section-desc">
                At exactly 20% capacity (K = 939 slots), 61 individuals differ between Model A and Model B queues. 
                Inspect their joint rankings and individual clinical records.
              </p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=6):
                    plot_swap_bar = gr.Plot(value=build_margin_swap_comparison_chart())
                    gr.HTML('<p class="hc-chart-caption"><strong>Boundary swap precision:</strong> In the 61-person boundary swap at 20% budget, Model B achieves a 4.92% hit rate (3 / 61 cases) compared to Model A\'s 1.64% (1 / 61 cases).<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')
                with gr.Column(scale=6):
                    plot_scatter = gr.Plot(value=build_joint_ranking_scatter())
                    gr.HTML('<p class="hc-chart-caption"><strong>Joint priority ranking:</strong> Each dot represents a patient. Points above the diagonal line are prioritized higher by Model B than Model A.<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')

            with gr.Row():
                margin_filter = gr.Radio(
                    choices=[
                        "3 True Positive Cases Rescued by Label B",
                        "All 61 Model B Exclusive (Rescued Queue)",
                        "61 Model A Exclusive (Dropped by Label B)",
                    ],
                    value="3 True Positive Cases Rescued by Label B",
                    label="Inspect Marginal Patient Clinical Profiles (At K = 939 Boundary Cutoff)",
                )

            margin_table_display = gr.HTML(
                value=render_margin_table_html("3 True Positive Cases Rescued by Label B")
            )

            # Section 03: Health Equity & Access Audit
            gr.HTML("""
            <div class="hc-section-card-header" id="sec-equity" data-toc="03 • Health Equity Audit" style="margin-top: 48px;">
              <span class="hc-section-kicker">03 / Fairness & Disparity</span>
              <h2 class="hc-section-title">Health Equity Audit Across Insurance and Income Strata</h2>
              <p class="hc-section-desc">
                Evaluating whether training on clinical diagnosis history systematically penalizes individuals with lower healthcare access.
              </p>
            </div>
            """)

            gr.HTML(render_equity_callout_html())
            with gr.Row():
                with gr.Column():
                    plot_equity = gr.Plot(value=build_equity_bar_chart())
                    gr.HTML('<p class="hc-chart-caption"><strong>Health equity audit:</strong> Compares screening sensitivity between insured and uninsured populations, highlighting where biomarker training closes access-driven gaps.<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')

            # Section 04: Health Economics & Decision Curves
            gr.HTML("""
            <div class="hc-section-card-header" id="sec-economics" data-toc="04 • Health Economics" style="margin-top: 48px;">
              <span class="hc-section-kicker">04 / Policy Economics</span>
              <h2 class="hc-section-title">Decision Curve Analysis & Net Monetary Benefit</h2>
              <p class="hc-section-desc">
                Quantifying financial and health utility trade-offs across screening test costs and complication avoidance values.
              </p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=6):
                    cost_input = gr.Number(
                        value=25.0, label="Point-of-Care HbA1c Test Cost ($ USD)"
                    )
                with gr.Column(scale=6):
                    benefit_input = gr.Number(
                        value=8500.0,
                        label="Present Value of Early Intervention / Avoided Complication ($ USD)",
                    )

            with gr.Row():
                with gr.Column(scale=6):
                    plot_dca = gr.Plot(value=build_decision_curve_plot())
                    gr.HTML('<p class="hc-chart-caption"><strong>Decision curve analysis:</strong> Evaluates net clinical and economic benefit across decision threshold probabilities compared to universal or zero screening.<span style="display: block; font-size: 0.76rem; color: #64748b; margin-top: 4px;">&copy; 2026 Cao Thien An Nguyen &bull; GitHub: aansensei</span></p>')
                with gr.Column(scale=6):
                    econ_summary_display = gr.HTML(
                        value=render_economic_ledger_html(20, 25.0, 8500.0)
                    )

            # Section 05: Transition Portal to About & Methodology (Added to Table of Contents)
            gr.HTML("""
            <div class="hc-section-card-header hc-next-tab-card" id="sec-to-methodology" data-toc="05 • How to Cite &amp; Methodology" style="margin-top: 56px; margin-bottom: 24px; background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%); border: 1.5px solid #bae6fd; border-radius: var(--radius-md); padding: 26px 30px; box-shadow: var(--shadow-sm); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
              <div style="max-width: 820px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                  <span class="hc-section-kicker" style="margin: 0; color: #0284c7; font-weight: 700;">Part 2 / Academic Dossier</span>
                  <span style="display: inline-flex; align-items: center; padding: 2px 8px; background: #0284c7; color: #ffffff; font-size: 0.72rem; font-weight: 700; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em;">Poster &amp; Citations</span>
                </div>
                <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--navy-900); margin: 0 0 6px 0; font-family: var(--font-serif);">
                  05 &bull; How to Cite (APA 7th), Methodology, Research Poster &amp; Sources
                </h3>
                <p style="font-size: 0.90rem; color: var(--text-muted); margin: 0; line-height: 1.55;">
                  Inspect the vector research poster (36&times;24 in), review complex survey variance proofs, examine formal APA 7th literature citations, and explore author background.
                </p>
              </div>
              <button type="button" class="hc-cta-btn" onclick="window.switchToAboutTab &amp;&amp; window.switchToAboutTab()" style="padding: 12px 24px; font-size: 0.92rem; font-weight: 600; background: var(--accent); color: #ffffff; border: none; border-radius: var(--radius-sm); cursor: pointer; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25); transition: all 0.2s ease;">
                <span>Explore About &amp; Methodology</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
              </button>
            </div>
            """)

        # Tab 2: About & Methodology (Complete Narrative, Author & Disclaimers)
        with gr.TabItem("About & Methodology"):
            gr.HTML(render_about_page_html())
            if not dict_df.empty:
                gr.Markdown("### Interactive CDC NHANES Variable Codebook")
                gr.DataFrame(
                    value=dict_df[
                        [
                            "original_name",
                            "variable_name",
                            "release",
                            "file_source",
                            "unit",
                            "role",
                            "description",
                        ]
                    ],
                    headers=[
                        "Original Code",
                        "Clean Variable",
                        "Cycle",
                        "File Source",
                        "Unit",
                        "Analytical Role",
                        "Description",
                    ],
                    datatype=["str", "str", "str", "str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                )

    # Site-wide Institutional Editorial Footer
    gr.HTML(render_footer_html())

    # Event Listeners
    capacity_slider.change(
        fn=on_capacity_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[sim_kpi_html, plot_gain, plot_nns, econ_summary_display],
    )

    btn_10.click(fn=lambda: 10, outputs=capacity_slider)
    btn_20.click(fn=lambda: 20, outputs=capacity_slider)
    btn_30.click(fn=lambda: 30, outputs=capacity_slider)

    margin_filter.change(
        fn=on_margin_filter_change,
        inputs=[margin_filter],
        outputs=[margin_table_display],
    )

    cost_input.change(
        fn=on_economic_param_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[econ_summary_display],
    )

    benefit_input.change(
        fn=on_economic_param_change,
        inputs=[capacity_slider, cost_input, benefit_input],
        outputs=[econ_summary_display],
    )


if __name__ == "__main__":
    import inspect

    in_space = bool(os.environ.get("SPACE_ID"))
    server_port = 7860 if in_space else int(os.environ.get("PORT", 3000))
    server_name = "0.0.0.0" if in_space else "127.0.0.1"

    fav = str(FAVICON_PATH) if FAVICON_PATH.exists() else None

    launch_sig = inspect.signature(demo.launch).parameters
    launch_kwargs = {
        "server_name": server_name,
        "server_port": server_port,
    }
    if fav and "favicon_path" in launch_sig:
        launch_kwargs["favicon_path"] = fav
    if "head" in launch_sig:
        launch_kwargs["head"] = HEAD_HTML
    if "ssr" in launch_sig:
        launch_kwargs["ssr"] = False
    if "show_api" in launch_sig:
        launch_kwargs["show_api"] = False

    demo.queue().launch(**launch_kwargs)
    import time
    while True:
        time.sleep(3600)
