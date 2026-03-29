"""
Reporter module for Evidence Pack Assembler.

Generates Markdown reports from analysis results.
"""

from datetime import date

def generate_report(analysis: dict, controls: list, owners_dict: dict, output_path: str) -> None:
    """
    Generate a comprehensive Markdown report.
    
    Args:
        analysis: Analysis results dictionary
        controls: List of control dictionaries
        owners_dict: Dictionary mapping owner names to owner details
        output_path: Path to write the report file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Evidence Inventory Report\n\n")
        f.write(f"Generated on: {date.today()}\n\n")
        
        # Summary Metrics
        f.write("## Summary Metrics\n\n")
        f.write(f"- Total Controls: {analysis['total_controls']}\n")
        f.write(f"- Total Evidence Items: {analysis['total_evidence']}\n")
        f.write(f"- Mapped Controls: {analysis['mapped_controls']}\n")
        f.write(f"- Controls with Missing Evidence: {analysis['missing_evidence_controls']}\n")
        f.write(f"- Stale Evidence Count: {analysis['stale_evidence_count']}\n")
        f.write(f"- Draft-Only Controls: {analysis['draft_only_count']}\n")
        f.write(f"- Unknown-Control Evidence: {analysis['unknown_control_evidence_count']}\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write("This report provides a comprehensive overview of the current evidence inventory ")
        f.write("for compliance controls across multiple frameworks. It identifies gaps in evidence ")
        f.write("coverage, stale evidence requiring updates, and prioritized remediation actions.\n\n")
        
        # Priority Gaps
        f.write("## Priority Gaps\n\n")
        if analysis['prioritized_remediation']:
            for control in analysis['prioritized_remediation']:
                f.write(f"- **{control['control_id']}**: {control['control_title']} ")
                f.write(f"(Framework: {control['framework']}, Priority: {control['priority']})\n")
        else:
            f.write("No high-priority controls with missing evidence identified.\n")
        f.write("\n")
        
        # Stale Evidence
        f.write("## Stale Evidence\n\n")
        if analysis['stale_evidence']:
            for ev in analysis['stale_evidence']:
                f.write(f"- **{ev['evidence_id']}**: {ev['evidence_title']} ")
                f.write(f"(Control: {ev['control_id']}, Review Date: {ev['review_date']}, Owner: {ev['owner']})\n")
        else:
            f.write("No stale evidence identified.\n")
        f.write("\n")
        
        # Unknown-Control Evidence
        f.write("## Unknown-Control Evidence\n\n")
        if analysis['unknown_control_evidence']:
            for ev in analysis['unknown_control_evidence']:
                f.write(f"- **{ev['evidence_id']}**: {ev['evidence_title']} ")
                f.write(f"(Mapped to unknown control: {ev['control_id']}, Owner: {ev['owner']})\n")
        else:
            f.write("No evidence mapped to unknown controls.\n")
        f.write("\n")
        
        # Detailed Control-to-Evidence Mapping
        f.write("## Detailed Control-to-Evidence Mapping\n\n")
        f.write("| Framework | Control ID | Control Title | Evidence ID | Evidence Title | Status | Review Date | Owner |\n")
        f.write("|-----------|------------|---------------|-------------|----------------|--------|-------------|-------|\n")
        
        for control in sorted(controls, key=lambda c: (c['framework'], c['control_id'])):
            control_id = control['control_id']
            evs = analysis['mapping'].get(control_id, [])
            
            if not evs:
                f.write(f"| {control['framework']} | {control_id} | {control['control_title']} | - | - | missing | - | - |\n")
            else:
                for ev in evs:
                    owner_team = owners_dict.get(ev['owner'], {}).get('team', 'Unknown')
                    review_date = ev.get('review_date', 'N/A')
                    f.write(f"| {control['framework']} | {control_id} | {control['control_title']} | {ev['evidence_id']} | {ev['evidence_title']} | {ev['status']} | {review_date} | {ev['owner']} ({owner_team}) |\n")
        
        f.write("\n")
        
        # Remediation Recommendations
        f.write("## Remediation Recommendations\n\n")
        f.write("1. **Address Priority Gaps**: Focus on collecting evidence for high-priority controls with missing evidence.\n")
        f.write("2. **Update Stale Evidence**: Review and update evidence items with review dates older than 90 days.\n")
        f.write("3. **Validate Draft Evidence**: Convert draft evidence to valid status through appropriate review processes.\n")
        f.write("4. **Resolve Unknown Mappings**: Investigate and correct evidence mapped to non-existent controls.\n")
        f.write("5. **Regular Monitoring**: Schedule quarterly reviews to maintain evidence currency and completeness.\n")