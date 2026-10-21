# FlowPilot — Workflow Automation Engine

A lightweight **event-driven rules engine** demonstrating how CRM and customer success teams can automate repetitive tasks. Uses configuration-driven JSON rules and standard-library Python — no external APIs, keys or dependencies.

## Features
- Match events to configurable triggers
- Combine conditions with `equals`, `not_equals`, `contains`, `greater_than`, `less_than`
- Actions: assign owner, set priority, add a tag or create a follow-up task
- Run multiple applicable rules for an event
- Export JSON audit log and follow-up tasks CSV
- Unit tests for filtering, conditions, disabled rules and no mutation

## Quick start (Python 3.9+)
```bash
cd workflow-automation-engine
python engine.py --events data/events.json --rules data/rules.json --output output
python -m unittest discover -v
```

See `output/result.json` for full event state + audit trail and `output/tasks.csv` for created tasks.

## How to customize
Edit `data/rules.json` to define your own triggers, conditions and actions. Sample events are in `data/events.json`.

**Example:** A `lead_created` event with `deal_value > 5000` gets high priority, is assigned to senior sales and creates a discovery-call task. All sample companies and events are fictional.

## Notes
This prototype simulates tasks locally; it **does not** send emails, contact leads or integrate with a production CRM. Real-world implementation would add auth, queueing, idempotency, validated schemas, retries and audited API integrations.

## License
MIT
