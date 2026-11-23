# Merge the six per-question decks of the AT&T vs Verizon project into one final presentation.
#
# Reconstructed on 23.11.2026 from the compiled bytecode that survived on disk
# (__pycache__/merge_blocks.cpython-314.pyc): the original .py source was lost. Logic, function names,
# constants and messages are identical to the bytecode. Only change: BLOCKS and OUT are relative to this
# folder instead of the original absolute Windows paths.
import copy
import re
from pathlib import Path

from pptx import Presentation
from pptx.parts.chart import ChartPart  # noqa: F401  (imported in the original)
from pptx.opc.package import Part, XmlPart
from pptx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
BLOCKS = [
    str(HERE / "blocks" / "Block1_Industry_Trends.pptx"),
    str(HERE / "blocks" / "Block2_Margin_Analysis.pptx"),
    str(HERE / "blocks" / "Block3_Data_Adjustments.pptx"),
    str(HERE / "blocks" / "Block4_Investment_Policy.pptx"),
    str(HERE / "blocks" / "Block5_Operating_KPIs.pptx"),
    str(HERE / "blocks" / "Block6_Synthesis.pptx"),
]
OUT = str(HERE / "ATT_Verizon_Final.pptx")

CHART_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACK_RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/package"


def _next_partname_safe(dest_pkg, tmpl, already_used):
    """Return next available PackURI for `tmpl`, accounting for in-flight additions."""
    prefix = tmpl[:(tmpl % 42).find("42")]
    existing = {str(p.partname) for p in dest_pkg.iter_parts() if str(p.partname).startswith(prefix)}
    existing |= already_used
    n = 1
    while True:
        candidate = tmpl % n
        if candidate not in existing:
            return PackURI(candidate)
        n += 1


def copy_slide_into(dest_prs, src_slide, used_partnames):
    """Copy src_slide (with its chart parts) into dest_prs.  Updates used_partnames in-place."""
    dest_pkg = dest_prs.part.package

    # Blank layout, then empty its shape tree
    new_slide = dest_prs.slides.add_slide(dest_prs.slide_layouts[6])
    sp_tree = new_slide.shapes._spTree
    for el in list(sp_tree):
        sp_tree.remove(el)

    rId_map = {}

    for old_rId, rel in list(src_slide.part.rels.items()):
        if rel.is_external:
            continue
        reltype = rel.reltype
        src_target = rel.target_part

        if reltype == RT.CHART:
            # Copy the chart part under a fresh name
            chart_tmpl = "/ppt/charts/chart%d.xml"
            new_chart_pn = _next_partname_safe(dest_pkg, chart_tmpl, used_partnames)
            used_partnames.add(str(new_chart_pn))

            new_chart = XmlPart.load(new_chart_pn, CT.DML_CHART, dest_pkg, src_target.blob)

            # Copy the chart's own sub-parts (embedded workbook, styles, colours)
            for c_rId, c_rel in list(src_target.rels.items()):
                if c_rel.is_external:
                    continue
                sub_src = c_rel.target_part

                raw = str(sub_src.partname)
                # e.g. /ppt/embeddings/Microsoft_Excel_Worksheet3.xlsx -> ..._Worksheet%d.xlsx
                base_no_num = re.sub(r"\d+(\.[^.]+)$", r"%d\1", raw)

                if "%d" not in base_no_num:
                    base_no_num = re.sub(r"(\.[^.]+)$", r"%d\1", raw)

                sub_pn = _next_partname_safe(dest_pkg, base_no_num, used_partnames)
                used_partnames.add(str(sub_pn))

                new_sub = Part(sub_pn, sub_src.content_type, dest_pkg, sub_src.blob)
                new_chart.relate_to(new_sub, c_rel.reltype)

            new_rId = new_slide.part.relate_to(new_chart, RT.CHART)
            rId_map[old_rId] = new_rId
            continue

        # Other parts (images, media…), except the slide layout: copy under a fresh name
        if reltype not in (RT.SLIDE_LAYOUT,):
            try:
                raw = str(src_target.partname)
                base_no_num = re.sub(r"\d+(\.[^.]+)$", r"%d\1", raw)
                if "%d" not in base_no_num:
                    base_no_num = re.sub(r"(\.[^.]+)$", r"%d\1", raw)
                new_pn = _next_partname_safe(dest_pkg, base_no_num, used_partnames)
                used_partnames.add(str(new_pn))
                new_part = Part(new_pn, src_target.content_type, dest_pkg, src_target.blob)
                new_rId = new_slide.part.relate_to(new_part, reltype)
                rId_map[old_rId] = new_rId
            except Exception:
                continue

    # Copy the shapes and re-point every r:id to the new relationships
    rid_attr = "{%s}id" % REL_NS
    for el in src_slide.shapes._spTree:
        el_copy = copy.deepcopy(el)
        for node in el_copy.iter():
            old = node.get(rid_attr)
            if old and old in rId_map:
                node.set(rid_attr, rId_map[old])
        sp_tree.append(el_copy)

    # Keep the source slide background
    src_bg = src_slide._element.find(qn("p:bg"))
    if src_bg is not None:
        new_el = new_slide._element
        old_bg = new_el.find(qn("p:bg"))
        if old_bg is not None:
            new_el.remove(old_bg)
        new_el.insert(0, copy.deepcopy(src_bg))

    return new_slide


def merge(block_paths, output_path):
    dest = Presentation(block_paths[0])

    # Part names already present in the destination package
    dest_pkg = dest.part.package
    used = {str(p.partname) for p in dest_pkg.iter_parts()}

    for path in block_paths[1:]:
        src = Presentation(path)
        for src_slide in src.slides:
            copy_slide_into(dest, src_slide, used)

    dest.save(output_path)


if __name__ == "__main__":
    merge(BLOCKS, OUT)

    final = Presentation(OUT)
    print("Saved: %s" % OUT)
    print("Total slides: %d" % len(final.slides))
    for i, sl in enumerate(final.slides, 1):
        ok_charts = broken = 0
        for sh in sl.shapes:
            if not sh.has_chart:
                continue
            try:
                len(sh.chart.series)
                ok_charts += 1
            except Exception:
                broken += 1
        status = ""
        if broken:
            status = " *** %d BROKEN chart(s)" % broken
        elif ok_charts:
            status = " [%d chart(s) OK]" % ok_charts
        print("  Slide %2d: %3d shapes%s" % (i, len(sl.shapes), status))
