# AT&T vs Verizon: margin and investment analysis (2010-2014)

**Course:** Introduction to Financial Statement Analysis and Reporting, HEC Lausanne (final project, individual, graded 5.0/6).
**Case:** Harvard Business School case 9-917-543, *AT&T and Verizon* (case material not included: copyrighted).

## Contents
| File | What it is |
|---|---|
| `ATT_Verizon_Analysis.xlsx` | 9-sheet Excel model, 313 formulas: income statements, wireless and wireline segments, balance sheets, data adjustments, margin trends |
| `ATT_Verizon_Final.pptx` | Final 20-slide deck with 7 native charts |
| `merge_blocks.py` | Python script (python-pptx) that merged the six per-question decks into the final deck, charts included |

## Questions answered (one block each)
1. **Industry trends:** wireless growth against structural wireline decline.
2. **Margin analysis:** EBITDA, EBIT and net-income margins for both firms.
3. **Data adjustments:** non-cash actuarial pension items stripped from EBITDA; Vodafone's 45% minority stake in Verizon Wireless.
4. **Investment policy:** estimated CapEx and investment intensity.
5. **Operating KPIs:** postpaid subscribers, ARPU, wireless segment margins.
6. **Synthesis:** DuPont ROE decomposition, ROIC against WACC, overall verdict.

## About `merge_blocks.py`
The original source file was lost; only its compiled bytecode (`merge_blocks.cpython-314.pyc`) survived.
The script was reconstructed from that bytecode on 23 November 2026 and verified: all three functions compile to **identical bytecode**, opcode for opcode.
The only change is that input and output paths are relative to this folder.

```bash
pip install python-pptx
python merge_blocks.py   # expects the six block decks in ./blocks/
```
