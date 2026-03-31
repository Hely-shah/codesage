from codesage.embeddings.representation import build_representation
from codesage.db.models import CodeUnit


def test_representation_contains_markers():
    u = CodeUnit(repo_id='r', file_id=1, unit_type='function', name='f', qualname='f', signature='f()', start_line=1, end_line=2, language='python', docstring='doc', code='def f():
  pass', content_hash='x')
    s = build_representation(u, 'a.py')
    assert 'DOCSTRING:' in s
    assert 'CODE:' in s
