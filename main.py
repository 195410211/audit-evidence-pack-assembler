import sys
import os
sys.path.append('src')

from loader import load_csv
from validator import validate_controls, validate_evidence, validate_owners, parse_date
from mapper import map_evidence_to_controls
from analyzer import analyze
from reporter import generate_report

def main():
    """
    Main entry point for the Evidence Pack Assembler.
    
    Orchestrates the loading, validation, mapping, analysis, and reporting of evidence data.
    """
    try:
        # Load data from CSV files
        controls = load_csv('data/controls.csv', ['framework', 'control_id', 'control_title', 'domain', 'owner_team', 'priority'])
        evidence = load_csv('data/evidence.csv', ['evidence_id', 'control_id', 'evidence_title', 'evidence_type', 'file_reference', 'owner', 'status', 'collected_date', 'review_date', 'notes'])
        owners = load_csv('data/owners.csv', ['owner', 'team', 'email'])
        
        # Prepare validation data
        control_ids = {c['control_id'] for c in controls}
        owner_names = {o['owner'] for o in owners}
        
        # Validate data
        validate_controls(controls)
        validate_evidence(evidence, control_ids, owner_names)
        validate_owners(owners)
        
        # Map evidence to controls
        mapping = map_evidence_to_controls(evidence)
        
        # Create owners dictionary for lookup
        owners_dict = {o['owner']: o for o in owners}
        
        # Analyze data
        analysis = analyze(controls, evidence, mapping, owners_dict)
        
        # Generate report
        generate_report(analysis, controls, owners_dict, 'output/evidence_inventory.md')
        
        # Print terminal summary
        print("Evidence Pack Assembler Summary:")
        print(f"Total Controls: {analysis['total_controls']}")
        print(f"Total Evidence Items: {analysis['total_evidence']}")
        print(f"Missing Evidence Controls: {analysis['missing_evidence_controls']}")
        print(f"Stale Evidence Items: {analysis['stale_evidence_count']}")
        print(f"Report generated at: output/evidence_inventory.md")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()