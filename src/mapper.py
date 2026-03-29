"""
Mapper module for Evidence Pack Assembler.

Maps evidence records to controls by control_id.
"""

def map_evidence_to_controls(evidence: list) -> dict:
    """
    Map evidence records to their corresponding controls.
    
    Args:
        evidence: List of evidence dictionaries
        
    Returns:
        Dictionary mapping control_id to list of evidence records
    """
    mapping = {}
    for ev in evidence:
        control_id = ev['control_id']
        if control_id not in mapping:
            mapping[control_id] = []
        mapping[control_id].append(ev)
    return mapping