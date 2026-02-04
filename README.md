\# 🦅 Legal Eagle AI

\### An Intelligent Contract Risk Audit System



!\[Python](https://img.shields.io/badge/Python-3.10+-blue.svg)

!\[AI Model](https://img.shields.io/badge/AI-Google\_Gemini\_1.5-orange.svg)

!\[Framework](https://img.shields.io/badge/Frontend-Streamlit-red.svg)



\*\*Legal Eagle AI\*\* protects everyday users from predatory legal documents. It is a hybrid intelligence system that reads PDF contracts, detects risks (financial traps, privacy violations), and verifies every warning against the original document text to prevent hallucinations.



---



\## 🚨 The Problem

Millions of people sign rental agreements, employment contracts, and NDAs without reading them because:

\* \*\*Complexity:\*\* Legal jargon ("Legalese") is intentionally confusing.

\* \*\*Length:\*\* 50-page documents cause "fatigue."

\* \*\*Cost:\*\* Hiring a lawyer for a simple review costs $300+.



This leads to users unknowingly agreeing to \*\*excessive late fees\*\*, \*\*invasive privacy clauses\*\*, and \*\*unfair termination rights\*\*.



\## 💡 The Solution

Legal Eagle AI acts as an automated legal auditor.

\* \*\*Instant Analysis:\*\* Upload a PDF and get a risk report in seconds.

\* \*\*Hybrid Architecture:\*\* Combines Rule-Based Logic (for speed) with Large Language Models (for reasoning).

\* \*\*Anti-Hallucination:\*\* Every risk flag is \*\*grounded\*\*—the system searches the PDF to find the \*exact\* sentence that proves the risk exists.



---



\## ⚙️ How It Works (The Pipeline)

1\.  \*\*Ingestion:\*\* Extracts text from PDF using `PyMuPDF` (cleaned of headers/footers).

2\.  \*\*Segmentation:\*\* Splits the "wall of text" into logical clauses/chunks.

3\.  \*\*Analysis:\*\* Sends chunks to \*\*Google Gemini 1.5 Flash\*\* with a strict prompt to identify risks and output JSON.

4\.  \*\*Verification:\*\* A Python script cross-references the AI's quotes with the original file. If the quote exists, it is marked \*\*✅ Verified\*\*.



---



\## 🚀 Features

\* \*\*Risk Scoring:\*\* Assigns a severity score (1-5) to every detected issue.

\* \*\*Simple Explanations:\*\* Translates complex legal terms into plain English.

\* \*\*Verbatim Citations:\*\* Shows exactly \*where\* in the document the bad clause is hiding.

\* \*\*Privacy-First:\*\* Documents are processed in memory and never stored.



---



\## 🛠️ Tech Stack

\* \*\*Language:\*\* Python 3.10

\* \*\*Frontend:\*\* Streamlit

\* \*\*PDF Engine:\*\* PyMuPDF (Fitz)

\* \*\*AI Model:\*\* Google Gemini 1.5 Flash (via API)

\* \*\*Environment Management:\*\* Python-dotenv



---
## 🎥 Demo

A short screen recording demonstrating the Legal Eagle AI workflow.

👉 [Click here to watch the demo](demo/legal-eagle-demo.mp4)


