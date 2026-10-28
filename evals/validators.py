"""Small data validators shared by local tests and release checks."""
import datetime
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse


def valid_repository(value):
    if value is None:
        return True
    parsed=urlparse(value) if isinstance(value,str) else None
    return bool(parsed and parsed.scheme=='https' and parsed.netloc and not parsed.username and not parsed.password)


def native_errors(records, skill_root):
    errors=[]
    if not isinstance(records,dict) or not isinstance(records.get('tests'),list):
        return ['tests must be an array']
    for row in records['tests']:
        if not isinstance(row,dict):
            errors.append('test record must be an object')
            continue
        identifier=row.get('id','<missing id>')
        if row.get('status') not in {'author_usage','pass','fail','not_run','skipped'}:
            errors.append(identifier+': invalid status')
        if row.get('status') not in {'author_usage','pass'}:
            continue
        required=['word_version','mathtype_version']
        if row['status']=='pass':
            required+=['os','entrypoint','tested_at','artifact']
        for key in required:
            value=row.get(key,'')
            if not isinstance(value,str) or not value.strip() or re.search(r'填写|unknown|not.run|待填|<.*>',value,re.I):
                errors.append(identifier+': missing actual '+key)
        for key in ['word_version','mathtype_version']:
            if not isinstance(row.get(key),str) or not re.search(r'\d',row[key]):
                errors.append(identifier+': version number required for '+key)
        if row['status']=='author_usage':
            continue
        try:
            datetime.date.fromisoformat(row.get('tested_at',''))
        except (ValueError,TypeError):
            errors.append(identifier+': invalid test date')
        artifact_value=row.get('artifact')
        artifact=(skill_root/artifact_value).resolve() if isinstance(artifact_value,str) else None
        if artifact is None or not artifact.is_relative_to(skill_root.resolve()) or not artifact.is_file():
            errors.append(identifier+': evidence file missing or outside skill')
    return errors


def text_hash(path):
    return hashlib.sha256(path.read_text(encoding='utf-8').replace('\r\n','\n').encode()).hexdigest()


def stale_records(root, manifest):
    stale=[]
    for relative, expected in manifest.get('skill_and_input_sha256',{}).items():
        path=(root/relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file() or text_hash(path)!=expected:
            stale.append(relative)
    return stale
