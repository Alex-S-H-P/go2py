from go2py.reader import Reader

FILE = "tests/go_code_to_read.go"

def test_reader():
    reader = Reader(FILE)
    assert reader.package == "example"
    assert len(reader.symbols) == 5, f"The reader detected {len(reader.symbols)} symbols. This might be more up to date than the test, check the go file."
    for funcid in range(4):
        assert f'Func{funcid}' in reader.symbols, f"Could not find Func{funcid}"
