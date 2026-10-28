"""Warn on stale model evidence; strict only when --release is requested."""
import argparse
import json
from pathlib import Path
from validators import stale_records

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--release',action='store_true')
    parser.add_argument('--manifest',type=Path,default=ROOT/'evals/runs/manifest.json')
    args=parser.parse_args()
    missing=not args.manifest.is_file()
    manifest=json.loads(args.manifest.read_text(encoding='utf-8')) if not missing else {}
    stale=stale_records(ROOT,manifest)
    incomplete=missing or not manifest.get('skill_and_input_sha256')
    print(json.dumps({'status':'warning' if stale or incomplete else 'current',
                      'stale':stale,'missing_manifest':missing,'release_mode':args.release,
                      'message':'Assess which model cases need rerunning; ordinary documentation edits remain allowed.'},ensure_ascii=False,indent=2))
    raise SystemExit(1 if args.release and (stale or incomplete) else 0)

if __name__=='__main__':
    main()
