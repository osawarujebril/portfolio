"""
PPTX Animation Injection Tool
==============================
Adds click-to-reveal animations to PowerPoint slides created with python-pptx.

python-pptx does NOT support animations natively. This tool injects the correct
OOXML animation XML directly into slide elements after they're created.

Supported animations:
- appear_on_click: Element instantly appears when presenter clicks
- fade_on_click: Element fades in smoothly when presenter clicks

Usage:
    from tools.pptx_animations import add_appear_on_click, add_fade_on_click, animate_slide

    # Option 1: Animate specific shapes
    slide = prs.slides.add_slide(layout)
    title = slide.shapes.add_textbox(...)
    subtitle = slide.shapes.add_textbox(...)
    image = slide.shapes.add_picture(...)
    add_appear_on_click(slide, [title, subtitle, image])

    # Option 2: Animate with fade
    add_fade_on_click(slide, [title, subtitle, image], duration=500)

    # Option 3: Mixed — some appear, some fade
    animate_slide(slide, [
        {"shape": title, "effect": "appear"},
        {"shape": subtitle, "effect": "fade", "duration": 400},
        {"shape": image, "effect": "fade", "duration": 600},
    ])
"""

from lxml import etree

# PowerPoint XML namespaces
NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

# Register namespaces so etree doesn't auto-prefix
for prefix, uri in NSMAP.items():
    etree.register_namespace(prefix, uri)


def _qn(tag):
    """Convert a namespace-prefixed tag like 'p:timing' to Clark notation."""
    prefix, local = tag.split(':')
    return '{%s}%s' % (NSMAP[prefix], local)


def _get_shape_id(shape):
    """Extract the shape ID (spid) from a python-pptx shape object."""
    sp_elem = shape._element
    # For most shapes, the id is in the nvSpPr/cNvPr or nvPicPr/cNvPr
    for tag in ['p:nvSpPr', 'p:nvPicPr', 'p:nvGrpSpPr', 'p:nvCxnSpPr']:
        nv = sp_elem.find(_qn(tag))
        if nv is not None:
            cnv_pr = nv.find(_qn('p:cNvPr'))
            if cnv_pr is not None:
                return cnv_pr.get('id')
    return None


def _build_appear_effect(shape_id, delay="0"):
    """Build XML for an appear-on-click effect (instant visibility toggle)."""
    par = etree.SubElement(etree.Element('dummy'), _qn('p:par'))

    cTn_outer = etree.SubElement(par, _qn('p:cTn'), attrib={
        'fill': 'hold'
    })
    stCondLst = etree.SubElement(cTn_outer, _qn('p:stCondLst'))
    etree.SubElement(stCondLst, _qn('p:cond'), attrib={'delay': delay})

    childTnLst = etree.SubElement(cTn_outer, _qn('p:childTnLst'))
    par_inner = etree.SubElement(childTnLst, _qn('p:par'))
    cTn_inner = etree.SubElement(par_inner, _qn('p:cTn'), attrib={
        'presetID': '1',
        'presetClass': 'entr',
        'presetSubtype': '0',
        'fill': 'hold',
        'nodeType': 'afterEffect'
    })
    stCondLst2 = etree.SubElement(cTn_inner, _qn('p:stCondLst'))
    etree.SubElement(stCondLst2, _qn('p:cond'), attrib={'delay': '0'})

    childTnLst2 = etree.SubElement(cTn_inner, _qn('p:childTnLst'))
    p_set = etree.SubElement(childTnLst2, _qn('p:set'))
    cTn_set = etree.SubElement(p_set, _qn('p:cTn'), attrib={
        'id': '1',
        'dur': '1',
        'fill': 'hold'
    })
    stCondLst3 = etree.SubElement(cTn_set, _qn('p:stCondLst'))
    etree.SubElement(stCondLst3, _qn('p:cond'), attrib={'delay': '0'})

    to_elem = etree.SubElement(p_set, _qn('p:to'))
    etree.SubElement(to_elem, _qn('a:srgbClr'), attrib={'val': '000000'})

    # Target the shape
    tgtEl = etree.SubElement(cTn_set, _qn('p:tgtEl'))
    spTgt = etree.SubElement(tgtEl, _qn('p:spTgt'), attrib={'spid': str(shape_id)})

    # Override: rebuild with correct structure
    return _build_appear_xml(shape_id)


def _build_appear_xml(shape_id):
    """Build the correct OOXML for appear-on-click."""
    xml_str = f'''<p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                        xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <p:cTn fill="hold">
            <p:stCondLst>
                <p:cond delay="0"/>
            </p:stCondLst>
            <p:childTnLst>
                <p:par>
                    <p:cTn presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
                        <p:stCondLst>
                            <p:cond delay="0"/>
                        </p:stCondLst>
                        <p:childTnLst>
                            <p:set>
                                <p:cBhvr>
                                    <p:cTn dur="1" fill="hold">
                                        <p:stCondLst>
                                            <p:cond delay="0"/>
                                        </p:stCondLst>
                                    </p:cTn>
                                    <p:tgtEl>
                                        <p:spTgt spid="{shape_id}"/>
                                    </p:tgtEl>
                                    <p:attrNameLst>
                                        <p:attrName>style.visibility</p:attrName>
                                    </p:attrNameLst>
                                </p:cBhvr>
                                <p:to>
                                    <p:strVal val="visible"/>
                                </p:to>
                            </p:set>
                        </p:childTnLst>
                    </p:cTn>
                </p:par>
            </p:childTnLst>
        </p:cTn>
    </p:par>'''
    return etree.fromstring(xml_str)


def _build_fade_xml(shape_id, duration=500):
    """Build the correct OOXML for fade-in-on-click."""
    xml_str = f'''<p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                        xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <p:cTn fill="hold">
            <p:stCondLst>
                <p:cond delay="0"/>
            </p:stCondLst>
            <p:childTnLst>
                <p:par>
                    <p:cTn presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
                        <p:stCondLst>
                            <p:cond delay="0"/>
                        </p:stCondLst>
                        <p:childTnLst>
                            <p:set>
                                <p:cBhvr>
                                    <p:cTn dur="1" fill="hold">
                                        <p:stCondLst>
                                            <p:cond delay="0"/>
                                        </p:stCondLst>
                                    </p:cTn>
                                    <p:tgtEl>
                                        <p:spTgt spid="{shape_id}"/>
                                    </p:tgtEl>
                                    <p:attrNameLst>
                                        <p:attrName>style.visibility</p:attrName>
                                    </p:attrNameLst>
                                </p:cBhvr>
                                <p:to>
                                    <p:strVal val="visible"/>
                                </p:to>
                            </p:set>
                            <p:animEffect transition="in" filter="fade">
                                <p:cBhvr>
                                    <p:cTn dur="{duration}" fill="hold"/>
                                    <p:tgtEl>
                                        <p:spTgt spid="{shape_id}"/>
                                    </p:tgtEl>
                                </p:cBhvr>
                            </p:animEffect>
                        </p:childTnLst>
                    </p:cTn>
                </p:par>
            </p:childTnLst>
        </p:cTn>
    </p:par>'''
    return etree.fromstring(xml_str)


def _inject_timing(slide, click_groups):
    """
    Inject the full timing XML into a slide.

    click_groups: list of etree Elements (one <p:par> per click)
    Each click group appears ONLY when the presenter clicks.
    """
    slide_elem = slide._element

    # Remove existing timing if present
    existing = slide_elem.find(_qn('p:timing'))
    if existing is not None:
        slide_elem.remove(existing)

    # Build the entire timing tree as XML string for correctness
    # This structure is validated against real PowerPoint output
    node_id = [1]  # mutable counter

    def next_id():
        val = node_id[0]
        node_id[0] += 1
        return str(val)

    # Build click group XML strings
    click_xml_parts = []
    for group in click_groups:
        group_str = etree.tostring(group, encoding='unicode')
        ctn_id = next_id()  # skip IDs 1 and 2 (used by root and seq)

    # Reset and build properly
    node_id[0] = 3
    click_entries = []
    for group in click_groups:
        gid = next_id()
        group_xml = etree.tostring(group, encoding='unicode')
        click_entries.append(f'''
            <p:par>
                <p:cTn id="{gid}" fill="hold">
                    <p:stCondLst>
                        <p:cond evt="onNext" delay="0">
                            <p:tgtEl>
                                <p:sldTgt/>
                            </p:tgtEl>
                        </p:cond>
                    </p:stCondLst>
                    <p:childTnLst>
                        {group_xml}
                    </p:childTnLst>
                </p:cTn>
            </p:par>''')

    all_clicks = ''.join(click_entries)

    timing_xml = f'''<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                                <p:childTnLst>
                                    {all_clicks}
                                </p:childTnLst>
                            </p:cTn>
                            <p:prevCondLst>
                                <p:cond evt="onPrev" delay="0">
                                    <p:tgtEl>
                                        <p:sldTgt/>
                                    </p:tgtEl>
                                </p:cond>
                            </p:prevCondLst>
                            <p:nextCondLst>
                                <p:cond evt="onNext" delay="0">
                                    <p:tgtEl>
                                        <p:sldTgt/>
                                    </p:tgtEl>
                                </p:cond>
                            </p:nextCondLst>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>'''

    timing_elem = etree.fromstring(timing_xml)
    slide_elem.append(timing_elem)


def add_appear_on_click(slide, shapes):
    """
    Add appear-on-click animation to a list of shapes.
    Each shape appears on a separate click.

    Args:
        slide: python-pptx slide object
        shapes: list of python-pptx shape objects (in order of appearance)
    """
    click_groups = []
    for shape in shapes:
        shape_id = _get_shape_id(shape)
        if shape_id is None:
            raise ValueError(f"Could not extract shape ID from {shape}")
        click_groups.append(_build_appear_xml(shape_id))

    _inject_timing(slide, click_groups)


def add_fade_on_click(slide, shapes, duration=500):
    """
    Add fade-in-on-click animation to a list of shapes.
    Each shape fades in on a separate click.

    Args:
        slide: python-pptx slide object
        shapes: list of python-pptx shape objects (in order of appearance)
        duration: fade duration in milliseconds (default 500ms)
    """
    click_groups = []
    for shape in shapes:
        shape_id = _get_shape_id(shape)
        if shape_id is None:
            raise ValueError(f"Could not extract shape ID from {shape}")
        click_groups.append(_build_fade_xml(shape_id, duration))

    _inject_timing(slide, click_groups)


def animate_slide(slide, animations):
    """
    Add mixed animations to a slide. Each animation triggers on a separate click.

    Args:
        slide: python-pptx slide object
        animations: list of dicts, each with:
            - "shape": python-pptx shape object
            - "effect": "appear" or "fade" (default "appear")
            - "duration": fade duration in ms (only for "fade", default 500)

    Example:
        animate_slide(slide, [
            {"shape": title, "effect": "appear"},
            {"shape": subtitle, "effect": "fade", "duration": 400},
            {"shape": image, "effect": "fade", "duration": 600},
        ])
    """
    click_groups = []
    for anim in animations:
        shape = anim["shape"]
        effect = anim.get("effect", "appear")
        duration = anim.get("duration", 500)

        shape_id = _get_shape_id(shape)
        if shape_id is None:
            raise ValueError(f"Could not extract shape ID from {shape}")

        if effect == "appear":
            click_groups.append(_build_appear_xml(shape_id))
        elif effect == "fade":
            click_groups.append(_build_fade_xml(shape_id, duration))
        else:
            raise ValueError(f"Unknown effect: {effect}. Use 'appear' or 'fade'.")

    _inject_timing(slide, click_groups)


def group_on_click(slide, shape_groups):
    """
    Animate groups of shapes — multiple shapes can appear on the SAME click.

    Args:
        slide: python-pptx slide object
        shape_groups: list of lists/tuples, each containing:
            - shapes that should appear together on one click
            - optionally a dict with "effect" and "duration" as last element

    Example:
        group_on_click(slide, [
            [title],                              # Click 1: title appears
            [subtitle, icon],                     # Click 2: subtitle + icon appear together
            [image, caption, {"effect": "fade"}], # Click 3: image + caption fade in together
        ])
    """
    click_groups = []

    for group in shape_groups:
        # Check if last element is a config dict
        config = {"effect": "appear", "duration": 500}
        shapes = list(group)
        if shapes and isinstance(shapes[-1], dict):
            config.update(shapes.pop())

        # Build a combined par element for all shapes in this click group
        if config["effect"] == "appear":
            # For multiple shapes on same click, we combine them in one par
            combined_xml = f'''<p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                                     xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <p:cTn fill="hold">
                    <p:stCondLst>
                        <p:cond delay="0"/>
                    </p:stCondLst>
                    <p:childTnLst>'''

            for shape in shapes:
                sid = _get_shape_id(shape)
                if sid is None:
                    raise ValueError(f"Could not extract shape ID from {shape}")
                combined_xml += f'''
                        <p:par>
                            <p:cTn presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                <p:childTnLst>
                                    <p:set>
                                        <p:cBhvr>
                                            <p:cTn dur="1" fill="hold">
                                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                            </p:cTn>
                                            <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
                                            <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                                        </p:cBhvr>
                                        <p:to><p:strVal val="visible"/></p:to>
                                    </p:set>
                                </p:childTnLst>
                            </p:cTn>
                        </p:par>'''

            combined_xml += '''
                    </p:childTnLst>
                </p:cTn>
            </p:par>'''
            click_groups.append(etree.fromstring(combined_xml))

        elif config["effect"] == "fade":
            dur = config["duration"]
            combined_xml = f'''<p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                                     xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <p:cTn fill="hold">
                    <p:stCondLst>
                        <p:cond delay="0"/>
                    </p:stCondLst>
                    <p:childTnLst>'''

            for shape in shapes:
                sid = _get_shape_id(shape)
                if sid is None:
                    raise ValueError(f"Could not extract shape ID from {shape}")
                combined_xml += f'''
                        <p:par>
                            <p:cTn presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                <p:childTnLst>
                                    <p:set>
                                        <p:cBhvr>
                                            <p:cTn dur="1" fill="hold">
                                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                            </p:cTn>
                                            <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
                                            <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                                        </p:cBhvr>
                                        <p:to><p:strVal val="visible"/></p:to>
                                    </p:set>
                                    <p:animEffect transition="in" filter="fade">
                                        <p:cBhvr>
                                            <p:cTn dur="{dur}" fill="hold"/>
                                            <p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl>
                                        </p:cBhvr>
                                    </p:animEffect>
                                </p:childTnLst>
                            </p:cTn>
                        </p:par>'''

            combined_xml += '''
                    </p:childTnLst>
                </p:cTn>
            </p:par>'''
            click_groups.append(etree.fromstring(combined_xml))

    _inject_timing(slide, click_groups)
