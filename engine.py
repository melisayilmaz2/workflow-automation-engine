"""Simple event-based workflow rule engine. Pure Python, no external services."""
import argparse
import csv
import json
from datetime import datetime,timezone
from pathlib import Path

ALLOWED_OPERATORS={'equals','not_equals','contains','greater_than','less_than'}
ALLOWED_ACTIONS={'assign_owner','set_priority','add_tag','create_task'}

def matches(conditions, event):
    for cond in conditions:
        key=cond['field']; op=cond['operator'];target=cond['value'];actual=event.get(key)
        if op not in ALLOWED_OPERATORS:raise ValueError(f'Unknown operator: {op}')
        if op=='equals':ok=actual==target
        elif op=='not_equals':ok=actual!=target
        elif op=='contains':ok=isinstance(actual,(str,list)) and target in actual
        else:
            try: a,b=float(actual),float(target)
            except (ValueError,TypeError):ok=False
            else:ok=(a>b) if op=='greater_than' else (a<b)
        if not ok:return False
    return True

def apply_action(event, action, tasks):
    name=action['type'];value=action['value']
    if name not in ALLOWED_ACTIONS:raise ValueError(f'Unknown action: {name}')
    if name=='assign_owner':event['owner']=str(value)
    elif name=='set_priority':event['priority']=str(value)
    elif name=='add_tag':
        event.setdefault('tags',[])
        if value not in event['tags']:event['tags'].append(value)
    elif name=='create_task':tasks.append({'lead_id':event.get('id'),'task':str(value),'owner':event.get('owner','Unassigned'),'status':'open'})

def run_workflows(events,rules):
    output=[];tasks=[];audit=[]
    for original in events:
        event=json.loads(json.dumps(original))
        for rule in rules:
            if not rule.get('enabled',True) or rule['trigger']!=event.get('event_type'):continue
            if matches(rule.get('conditions',[]),event):
                for action in rule['actions']:apply_action(event,action,tasks)
                audit.append({'event_id':event.get('id'),'rule':rule['name'],'actions':len(rule['actions'])})
        output.append(event)
    return {'processed_events':output,'tasks':tasks,'audit_log':audit,'summary':{'total_events':len(output),'rules_triggered':len(audit),'tasks_created':len(tasks)}}

def main():
    parser=argparse.ArgumentParser(description='Event-driven sales operations automation')
    parser.add_argument('--events',default='data/events.json');parser.add_argument('--rules',default='data/rules.json');parser.add_argument('--output',default='output')
    args=parser.parse_args()
    with Path(args.events).open(encoding='utf8') as f: events=json.load(f)
    with Path(args.rules).open(encoding='utf8') as f: rules=json.load(f)
    result=run_workflows(events,rules)
    dest=Path(args.output);dest.mkdir(parents=True,exist_ok=True)
    (dest/'result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    with (dest/'tasks.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=['lead_id','task','owner','status']);writer.writeheader();writer.writerows(result['tasks'])
    print(json.dumps(result['summary'],indent=2));print(f'Saved {dest / "result.json"} and {dest / "tasks.csv"}')
if __name__=='__main__':main()
