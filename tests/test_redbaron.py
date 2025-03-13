

from redbaron import RedBaron

def test_1():
    code = '''
def word_pattern(pattern: str, s: str) -> bool:
    pass  # This is just the signature; the implementation would follow.
    '''

    target = None
    red = RedBaron(code)
    for o in red:
        print(o.name, o.type)
        if o.type == "def" and o.name == "word_pattern":
            target = o

    target.help()
    target.value = '"""implementation"""\nprint("hi")\n'
    #target.value[0].help()
    #print(red.dumps())
    #assert False

