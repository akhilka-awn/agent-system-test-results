import sys
import os
import re

def extract_body_content(html_text):
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html_text, re.DOTALL | re.IGNORECASE)
    return body_match.group(1) if body_match else ""

def extract_style_block(html_text):
    style_match = re.search(r"<style[^>]*>(.*?)</style>", html_text, re.DOTALL | re.IGNORECASE)
    return "<style>" + style_match.group(1) + "</style>" if style_match else ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_html_tabs.py file1.html,file2.html,...")
        sys.exit(1)

    file_list = sys.argv[1].split(",")
    tab_headers = []
    tab_contents = []
    shared_style = ""

    for idx, filepath in enumerate(file_list):
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if idx == 0:
            shared_style = extract_style_block(content)

        body = extract_body_content(content)
        tab_id = f"Tab{idx+1}"
        tab_name = os.path.basename(filepath)
        tab_headers.append(f'<button class="tablinks" onclick="openTab(event, \'{tab_id}\')">{tab_name}</button>')
        tab_contents.append(f'<div id="{tab_id}" class="tabcontent">\n{body}\n</div>')

    tabs_css = """
<style>
    body {margin-left: 10%; margin-right: 10%; font-family: Monaco, Tahoma;}
    .tab {
        overflow: hidden;
        border-bottom: 1px solid #ccc;
    }
    .tab button {
        background-color: #f1f1f1;
        float: left;
        border: none;
        outline: none;
        cursor: pointer;
        padding: 10px 20px;
        transition: 0.3s;
        font-size: 17px;
    }
    .tab button:hover {
        background-color: #ddd;
    }
    .tab button.active {
        background-color: #ccc;
    }
    .tabcontent {
        display: none;
        padding: 20px;
        border: 1px solid #ccc;
        border-top: none;
    }
</style>
"""

    tabs_js = """
<script>
function openTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tabbuttons = document.getElementsByClassName("tablinks");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
window.onload = function() {
    document.getElementsByClassName("tablinks")[0].click();
};
</script>
"""

    final_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Combined Test Results</title>
    {shared_style}
    {tabs_css}
</head>
<body>
<div class="tab">
    {''.join(tab_headers)}
</div>
{''.join(tab_contents)}
{tabs_js}
</body>
</html>
"""

    output_file = "combined_tabbed_output.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Tabbed HTML file generated: {output_file}")

if __name__ == "__main__":
    main()

