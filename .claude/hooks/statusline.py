#!/usr/bin/env python3
"""Status line script for Claude Code."""
import sys
import json
import os

try:
    # Read JSON from stdin
    data = json.load(sys.stdin)

    # Extract data
    cw = data.get('context_window', {})
    cost_data = data.get('cost', {})
    model = data.get('model', {}).get('display_name', 'Claude')
    current_dir = data.get('workspace', {}).get('current_dir', '')
    dir_name = os.path.basename(current_dir) if current_dir else ''

    # Calculate tokens
    total_input = cw.get('total_input_tokens', 0)
    total_output = cw.get('total_output_tokens', 0)
    total = total_input + total_output

    # Get cost
    total_cost = cost_data.get('total_cost_usd', 0)

    # Get percentages
    used_pct = cw.get('used_percentage')
    remaining_pct = cw.get('remaining_percentage')

    # Build status parts
    parts = []
    if dir_name:
        parts.append(dir_name)
    parts.append(model)
    parts.append(f'Tokens: {total}')
    parts.append(f'Cost: ${total_cost:.4f}')

    if used_pct is not None and remaining_pct is not None:
        parts.append(f'Context: {used_pct:.1f}% used ({remaining_pct:.1f}% remaining)')

    # Print status
    print(' | '.join(parts))

except Exception as e:
    # Fallback: show minimal info
    print(f'Claude Code | Error: {str(e)}')