import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

path = Path(__file__).resolve().parent / 'club_system.py'
home_dir = Path.cwd()
compile(path.read_text(encoding='utf-8'), str(path), 'exec')
spec = importlib.util.spec_from_file_location('club_system', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = ['PASS: Python 3.12.14 compilation and import (real tkinter import).']
def cli(inputs):
    stream = io.StringIO()
    with patch('builtins.input', side_effect=inputs), patch.object(m, 'show_thank_you_gui') as gui, contextlib.redirect_stdout(stream):
        m.main()
    assert gui.call_count == 1
    return stream.getvalue()

with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    text = cli(['1','Demo Event','2026-12-01','3','2','Demo Student','DEMO-001','1','3','DEMO-001','Demo Event','5','6','DEMO-001','7','4','DEMO-001','Demo Event','8'])
    assert 'Registered successfully.' in text and 'cancelled: Demo Event' in text
    c = m.Club('test'); c.load_data()
    assert c.get_events()[0].get_capacity() == 3 and c.get_students()[0].get_registered_events() == []
    assert len(c.get_transactions()) == 2
    results.append('PASS: scripted CLI add/enroll/register/view events/view activity/view history/cancel/exit, save and reload. Shutdown GUI mocked; not visually tested.')
    for cls, limit in [(m.Student,3),(m.ClubManager,6)]:
        s=cls('Demo','DEMO')
        for n in range(limit): s.can_register(); s.register(str(n))
        try: s.can_register()
        except ValueError: pass
        else: raise AssertionError('limit not enforced')
    results.append('PASS: regular limit 3 and manager limit 6; duplicate Student.register raises ValueError.')
    s=m.Student('Demo','DEMO'); s.register('A')
    try: s.register('A')
    except ValueError: pass
    else: raise AssertionError('duplicate allowed')
    text=cli(['3','DEMO-001','Demo Event','3','DEMO-001','Demo Event','8'])
    c=m.Club('test'); c.load_data()
    assert c.get_events()[0].get_capacity()==1 and c.get_students()[0].get_registered_events()==['Demo Event']
    results.append('CONFIRMED BUG: duplicate CLI registration consumes a seat before rejecting the duplicate (3 -> 1 for one registration).')
    e=m.Event('A','date',2); e.set_capacity(9)
    assert e.get_capacity()==2
    results.append('CONFIRMED BUG: Event.set_capacity does not change capacity.')
    Path('club_data.txt').write_text('E|Full|date|0\nS|R|Demo|DEMO|Full\n',encoding='utf-8')
    c=m.Club('test'); buf=io.StringIO()
    with contextlib.redirect_stdout(buf): c.load_data()
    assert 'Error loading saved data.' in buf.getvalue() and not c.get_events() and not c.get_students()
    results.append('CONFIRMED BUG: saved full event (capacity 0) prevents reload; subsequent records skipped.')
    os.chdir(home_dir)
print('\n'.join(results))
