import streamlit as st


def parse_clippings_file(lines):
    clippings = []
    current_clipping = ''

    for line in lines:
        line = line.strip()

        if line:
            if line.startswith('=========='):
                if current_clipping:
                    clippings.append(current_clipping)
                current_clipping = ''
            else:
                current_clipping += line + '\n'

    if current_clipping:
        clippings.append(current_clipping)

    return clippings


def format_clipping(clipping, include_location):
    lines = clipping.strip().split('\n')
    book_info = lines[0]
    clipping_text = '\n'.join(lines[2:]).strip()

    if include_location:
        location_line = lines[1]
        location = location_line.split('|')[0].strip().replace(
            '- Your Highlight on', '')
        formatted_clipping = f"{clipping_text}  - {location}"
    else:
        formatted_clipping = clipping_text

    return formatted_clipping


def main():
    st.title("Kindle Clippings Extractor")

    st.sidebar.header("Options")
    input_file = st.sidebar.file_uploader(
        "Upload My Clippings.txt", type=["txt"])
    include_location = st.sidebar.checkbox("Include Page/Location Info")

    if input_file is not None:
        lines = input_file.read().decode("utf-8").splitlines()
        clippings = parse_clippings_file(lines)
        clippings_by_book = {}

        for clipping in clippings:
            lines = clipping.strip().split('\n')
            book_info = lines[0]
            if book_info in clippings_by_book:
                clippings_by_book[book_info].append(clipping)
            else:
                clippings_by_book[book_info] = [clipping]

        for book_info, clippings_list in clippings_by_book.items():
            with st.expander(book_info):
                for idx, clipping in enumerate(clippings_list, start=1):
                    formatted_clipping = format_clipping(
                        clipping, include_location)
                    st.write(f"{formatted_clipping}")


if __name__ == '__main__':
    main()
