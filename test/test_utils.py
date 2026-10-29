from utils import print_table

def test_columns_widen_to_longest_value(capsys):
    print_table(["PLU", "Nama"], [["1001", "Susu Ultra Milk 1L"], ["1002", "Roti"]])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "PLU   Nama              "
    assert lines[1] == "-" * len(lines[0])
    assert lines[2] == "1001  Susu Ultra Milk 1L"
    assert lines[3] == "1002  Roti              "

def test_right_align_numbers(capsys):
    print_table(["Nama", "Qty"], [["Roti", 5], ["Susu", 120]], ["<", ">"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[2] == "Roti    5"
    assert lines[3] == "Susu  120"

def test_empty_rows_prints_header_only(capsys):
    print_table(["PLU", "Nama"], [])
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["PLU  Nama", "---------"]
