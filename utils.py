def print_table(headers, rows, align=None):
    # headers : list judul kolom, contoh ["PLU", "Nama", "Harga"]
    # rows    : list of list, satu list per baris, urutan sama dengan headers
    # align   : list "<" (rata kiri) atau ">" (rata kanan) per kolom; default semua kiri
    if align is None:
        align = ["<"] * len(headers)

    # Lebar kolom = teks terpanjang di kolom itu (judul atau isi)
    widths = []
    for i in range(len(headers)):
        width = len(str(headers[i]))
        for row in rows:
            width = max(width, len(str(row[i])))
        widths.append(width)

    def format_row(cells):
        parts = []
        for i in range(len(cells)):
            parts.append(f"{str(cells[i]):{align[i]}{widths[i]}}")
        return "  ".join(parts)

    header_line = format_row(headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(format_row(row))
