"""
Analyzer module for Evidence Pack Assembler.

Analyzes evidence data for staleness, gaps, and other metrics.
"""

from datetime import date, timedelta
from validator import parse_date

def analyze(controls: list, evidence: list, mapping: dict, owners_dict: dict) -> dict:
    """
    Analyze the evidence data and compute various metrics.
    
    Args:
        controls: List of control dictionaries
        evidence: List of evidence dictionaries
        mapping: Dictionary mapping control_id to evidence lists
        owners_dict: Dictionary mapping owner names to owner details
        
    Returns:
        Dictionary containing analysis results
    """
    today = date.today()
    stale_threshold = today - timedelta(days=90)
    
    total_controls = len(controls)
    total_evidence = len(evidence)
    mapped_controls = len(mapping)
    
    # Find controls with missing evidence (no valid evidence)
    missing_evidence_controls = []
    draft_only_controls = []
    
    for control in controls:
        control_id = control['control_id']
        evs = mapping.get(control_id, [])
        
        has_valid = any(ev['status'] == 'valid' for ev in evs)
        has_draft = any(ev['status'] == 'draft' for ev in evs)
        
        if not has_valid:
            missing_evidence_controls.append(control)
            if has_draft:
                draft_only_controls.append(control_id)
    
    # Find stale evidence
    stale_evidence = []
    for ev in evidence:
        review_date_str = ev.get('review_date', '')
        if review_date_str:
            review_date = parse_date(review_date_str)
            if review_date and review_date < stale_threshold:
                stale_evidence.append(ev)
    
    # Find evidence mapped to unknown controls
    known_control_ids = {c['control_id'] for c in controls}
    unknown_control_evidence = [ev for ev in evidence if ev['control_id'] not in known_control_ids]
    
    # Prioritized remediation (high priority missing evidence)
    prioritized_remediation = [c for c in missing_evidence_controls if c['priority'] == 'High']
    
    return {
        'total_controls': total_controls,
        'total_evidence': total_evidence,
        'mapped_controls': mapped_controls,
        'missing_evidence_controls': len(missing_evidence_controls),
        'stale_evidence_count': len(stale_evidence),
        'draft_only_count': len(draft_only_controls),
        'unknown_control_evidence_count': len(unknown_control_evidence),
        'prioritized_remediation': prioritized_remediation,
        'stale_evidence': stale_evidence,
        'unknown_control_evidence': unknown_control_evidence,
        'mapping': mapping
    }