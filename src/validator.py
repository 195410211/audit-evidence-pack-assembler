"""
Validator module for Evidence Pack Assembler.

Validates data integrity and business rules for controls, evidence, and owners.
"""

import datetime

ALLOWED_STATUSES = {'valid', 'stale', 'missing', 'draft'}

def parse_date(date_str: str) -> datetime.date:
    """
    Parse a date string in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to parse
        
    Returns:
        datetime.date object or None if invalid
    """
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except ValueError:
        return None

def validate_controls(controls: list) -> None:
    """
    Validate controls data.
    
    Args:
        controls: List of control dictionaries
        
    Raises:
        ValueError: If validation fails
    """
    if not controls:
        raise ValueError("No controls found")
        
    # Check for unique control_ids
    control_ids = [c['control_id'] for c in controls]
    if len(control_ids) != len(set(control_ids)):
        duplicates = [id for id in control_ids if control_ids.count(id) > 1]
        raise ValueError(f"Duplicate control_ids found: {set(duplicates)}")
    
    # Check required fields
    required_fields = ['framework', 'control_id', 'control_title', 'domain', 'owner_team', 'priority']
    for control in controls:
        for field in required_fields:
            if not control.get(field) or control[field].strip() == '':
                raise ValueError(f"Missing or empty required field '{field}' in control {control.get('control_id', 'unknown')}")

def validate_evidence(evidence: list, control_ids: set, owner_names: set) -> None:
    """
    Validate evidence data.
    
    Args:
        evidence: List of evidence dictionaries
        control_ids: Set of valid control IDs
        owner_names: Set of valid owner names
        
    Raises:
        ValueError: If validation fails
    """
    if not evidence:
        raise ValueError("No evidence found")
        
    # Check for unique evidence_ids
    evidence_ids = [e['evidence_id'] for e in evidence]
    if len(evidence_ids) != len(set(evidence_ids)):
        duplicates = [id for id in evidence_ids if evidence_ids.count(id) > 1]
        raise ValueError(f"Duplicate evidence_ids found: {set(duplicates)}")
    
    # Check each evidence record
    required_fields = ['evidence_id', 'control_id', 'evidence_title', 'evidence_type', 'file_reference', 'owner', 'status']
    for ev in evidence:
        # Required fields
        for field in required_fields:
            if not ev.get(field) or ev[field].strip() == '':
                raise ValueError(f"Missing or empty required field '{field}' in evidence {ev.get('evidence_id', 'unknown')}")
        
        # Status validation
        if ev['status'] not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{ev['status']}' in evidence {ev['evidence_id']}. Allowed: {ALLOWED_STATUSES}")
        
        # Owner validation
        if ev['owner'] not in owner_names:
            raise ValueError(f"Unknown owner '{ev['owner']}' in evidence {ev['evidence_id']}")
        
        # Date validation
        collected_date = parse_date(ev.get('collected_date', ''))
        if collected_date is None:
            raise ValueError(f"Invalid or missing collected_date in evidence {ev['evidence_id']}")
        
        # Review date is optional but if present must be valid
        review_date_str = ev.get('review_date', '')
        if review_date_str and parse_date(review_date_str) is None:
            raise ValueError(f"Invalid review_date in evidence {ev['evidence_id']}")

def validate_owners(owners: list) -> None:
    """
    Validate owners data.
    
    Args:
        owners: List of owner dictionaries
        
    Raises:
        ValueError: If validation fails
    """
    if not owners:
        raise ValueError("No owners found")
        
    # Check for unique owners
    owner_names = [o['owner'] for o in owners]
    if len(owner_names) != len(set(owner_names)):
        duplicates = [name for name in owner_names if owner_names.count(name) > 1]
        raise ValueError(f"Duplicate owners found: {set(duplicates)}")
    
    # Check required fields
    required_fields = ['owner', 'team', 'email']
    for owner in owners:
        for field in required_fields:
            if not owner.get(field) or owner[field].strip() == '':
                raise ValueError(f"Missing or empty required field '{field}' in owner {owner.get('owner', 'unknown')}")