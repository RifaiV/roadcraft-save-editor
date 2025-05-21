import zlib
import argparse
import hashlib 
import json
import panel as pn
import webview
import tkinter as tk
from tkinter import filedialog

WBITS_VALUE = -15
HEADER_LENGTH = 53
ZLIB_HEADER = b'\x78\x9c'

WRITE_DEBUG_FILES = False

def compute_md5(data):
    """Compute the MD5 hash of the given data."""
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash
    
def try_decompress_zlib_block(data, start_offset=0):
    """Try different decompression methods on the data starting at offset"""
    result = {}
    
    # Extract the data after the offset
    zlib_block = data[start_offset:]
    # read the first int32
    uncompressed_size = int.from_bytes(zlib_block[:4], byteorder='little')
    # read the second int32
    compressed_size = int.from_bytes(zlib_block[4:8], byteorder='little')
    #confirm next 2 bytes are zlib header
    if zlib_block[8:10] != ZLIB_HEADER:
        print("Not a zlib header")

    #decompress from here
    decompressed = zlib.decompress(zlib_block[10:], wbits=WBITS_VALUE)

    # return an object with the decompressed data and the sizes
    result['uncompressed_size'] = uncompressed_size
    result['compressed_size'] = compressed_size
    result['decompressed_bytes'] = decompressed

    return result

def decode_file(file_path):
    """Decode a file by decompressing its zlib blocks and return a single byte array."""
    try:
        with open(file_path, 'rb') as f:
            fileContent = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    print(f"File size: {len(fileContent)} bytes")

    md5 = compute_md5(fileContent[HEADER_LENGTH:])
    print(f"Original MD5 hash of compressed data from offset {HEADER_LENGTH}: {md5}")

    offset = HEADER_LENGTH
    decompressed_data = bytearray()

    while offset < len(fileContent):
        # Decompress the data at the current offset
        result = try_decompress_zlib_block(fileContent, start_offset=offset)
        decompressed_data.extend(result['decompressed_bytes'])
        offset += result['compressed_size'] + 8  # 8 bytes for the 2 int32s

    print(f"Total decompressed data size: {len(decompressed_data)} bytes")
    return fileContent, decompressed_data


def encode_file(content, decompressed_data):
    """Encode a file by compressing the decompressed data into chunks."""
    try:
        print("Rebuilding the file with the new compressed data...")

        new_zlib_data = b''
        chunk_size = 1024**2  # 1 MB
        offset = 0

        while offset < len(decompressed_data):
            # divide the data into chunks - probably not relevant until completesave gets huge
            chunk = decompressed_data[offset:offset + chunk_size]
            offset += chunk_size

            # compress chunk
            new_block_uncompressed_size_bytes = len(chunk).to_bytes(4, 'little')
            new_compressed_data = zlib.compress(chunk, level=-1, wbits=WBITS_VALUE)
            adler32 = zlib.adler32(chunk)
            adler32_bytes = adler32.to_bytes(4, 'big')

            new_block_compressed_size = len(new_compressed_data) + 6
            new_block_compressed_size_bytes = new_block_compressed_size.to_bytes(4, 'little')

            # Append the new block to the new data
            new_zlib_data += new_block_uncompressed_size_bytes + new_block_compressed_size_bytes + ZLIB_HEADER + new_compressed_data + adler32_bytes

        #rebuild header components
        original_filetype = content[:4]
        zero_bytes = b'\x00\x00\x00\x00'
        three_byte = b'\x03'
        new_total_compressed_size_bytes = len(new_zlib_data).to_bytes(4, 'little')
        new_total_uncompressed_size_bytes = len(decompressed_data).to_bytes(4, 'little')
        new_md5 = compute_md5(new_zlib_data)
        print(f"New MD5 hash of compressed data: {new_md5}")
        new_md5_bytes = new_md5.encode('utf-8')

        final_data = original_filetype + new_total_compressed_size_bytes + zero_bytes + new_total_uncompressed_size_bytes + zero_bytes + new_md5_bytes + three_byte + new_zlib_data

        with open('OutputSave', 'wb') as f:
            f.write(final_data)
        print("New compressed data with original header saved to OutputSave.")
        return True
    except Exception as e:
        print(f"Error during encoding: {e}")
        return False

def process_file(file_path):
    """Process a file by decoding and then encoding it."""
    fileContent, decompressed_data = decode_file(file_path)

    if fileContent and decompressed_data:
        if WRITE_DEBUG_FILES:
            with open('OutputRaw_block_all_test', 'wb') as f:
                f.write(decompressed_data)
            print("Decompressed data written to OutputRaw_block_all_test for testing.")

        # Assuming its a completesave, we will try to parse the decompressed data as JSON
        handle_completesave(decompressed_data, fileContent)


def decode_completesave_json(decompressed_data):
    json_data = json.loads(decompressed_data.decode('utf-8'))
    print("Parsed JSON data:")
    print(json.dumps(json_data, indent=3, default=repr)[:900]) 
    return json_data

def convert_completesave_json_to_bytes(json_data):
    bytes = json.dumps(
        json_data,
        indent=3,
        ensure_ascii=False,
        separators=(',', ': ')
    ).encode('utf-8')
    print("Modified JSON data has been re-encoded.")


    if WRITE_DEBUG_FILES:
        with open('Output_json_rebuilt', 'wb') as f:
            f.write(bytes)
    return bytes

def handle_completesave(decompressed_data, fileContent):
    """Parse the decompressed data as JSON, display a UI for editing, and return the modified data."""
    try:
        json_data = decode_completesave_json(decompressed_data)
        editor = pn.widgets.JSONEditor(value=json_data, sizing_mode='stretch_both', mode='form')

        def toggle_mode(event):
            if editor.mode == 'form':
                editor.mode = 'text'
                toggle_button.name = "Switch to Simple Form Mode"
            else:
                editor.mode = 'form'
                toggle_button.name = "Switch to Free Text Mode"

        toggle_button = pn.widgets.Button(name="Switch to Free Text Mode", button_type="primary")
        toggle_button.on_click(toggle_mode)

        save_status = pn.pane.Markdown("", sizing_mode='stretch_width')

        def save_changes(event):
            save_status.object = "Saving changes, please wait..."
            print("Save requested...")
            nonlocal json_data
            json_data = editor.value

            decompressed_data_edited = convert_completesave_json_to_bytes(json_data)
            saveResult = encode_file(fileContent, decompressed_data_edited)

            if saveResult:
                save_status.object = "Changes saved to OutputSave! Rename it to CompleteSave and replace the original file."
            else:
                save_status.object = "Error saving changes. Please check the console for details."
                return

        save_button = pn.widgets.Button(name="Save Changes to New File", button_type="primary")
        save_button.on_click(save_changes)

        header = pn.pane.HTML("<h2 style='font-size: 20px; font-weight: bold;'>NakedSave</h2>"
        "<h3>Roadcraft Completesave Editor</h3>"
        "<p>Use this tool to edit your completesave file, usually found at %AppData%/Local/Saber/RoadCraftGame/storage/steam/user/&lt;YOUR_STEAM_USER_ID&gt;/Main/save</p>"
        "<p>BACK UP YOUR SAVES FIRST. This tool keeps the file format correct but you can still break things by putting silly values in.</p>"
        , sizing_mode='stretch_width')
        app = pn.Column(header, pn.Row(toggle_button, save_button, save_status ), editor)

        def start_server(window):
            server = pn.serve(app, show=False, start=True, port=55870, threaded=True)  
            def on_window_closed():
                print("Webview window closed. Stopping the server...")
                server.stop()   
            window.events.closing += on_window_closed

        window = webview.create_window("JSON Editor", f"http://localhost:55870", width=1050, height=950)

        webview.start(start_server, window)

    except Exception as e:
        print(f"Error handling alleged completesave file: {e}")

    return decompressed_data

def main():
    parser = argparse.ArgumentParser(description='Completesave editor for Roadcraft.')
    parser.add_argument('file', nargs='?', help='Path to the CompleteSave file to decompress')
    args = parser.parse_args()

    if not args.file:
        print("No file argument provided. Opening file picker...")
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(
            title="Select Roadcraft CompleteSave file",
            filetypes=[("CompleteSave File", "*.*")]
        )
        if not file_path:
            print("No file selected. Exiting.")
            return
        args.file = file_path

    process_file(args.file)

if __name__ == "__main__":
    main()