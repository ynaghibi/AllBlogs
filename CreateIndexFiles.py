
import os
from bs4 import BeautifulSoup

def process_directory(root_dir='.'):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Find HTML files EXCLUDING index.html as input
        html_files = [
            f for f in filenames 
            if (f.lower().endswith('.html') or f.lower().endswith('.xhtml'))
            and f.lower() != 'index.html'  # Only exclude as INPUT
        ]
        if not html_files:
            continue
        input_file = os.path.join(dirpath, html_files[0])
        output_file = os.path.join(dirpath, 'index.html')
        # Process WILL overwrite output index.html
        process_xhtml_file(input_file, output_file)

def process_xhtml_file(input_file, output_file):
    # Custom CSS content to append
    custom_css = """
:root {
    --bg-color: #121212;
    --text-color: #e0e0e0;
    --accent-color: #bb86fc;
    --border-color: #333;
    --code-bg: #1e1e1e;
    --item-bullet: #bb86fc;
    --math-color: #f5f5f5;
    --link-color: #82b1ff;
    --link-hover: #bb86fc;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 20px;
    max-width: 700px;
    margin: 0 auto;
	 zoom: 140%;
}

math {
    color: var(--math-color);
    margin: 15px 0;
    padding: 10px;
    background-color: #1e1e1e;
    border-radius: 4px;
}

div.lyx_code {
    font-family: 'Consolas', monospace;
    background-color: #252525;
    border-left: 3px solid #bb86fc;
    padding: 12px;
    border-radius: 3px;
    overflow-x: auto;
    font-size: 13px !important;
    line-height: 1.4 !important;
}

.lyx_code_item,
.lyx_code_item span,
.lyx_code_item b,
.lyx_code_item b span {
    color: #e0e0e0 !important;
    font-size: inherit !important;
    font-family: 'Consolas', monospace !important;
    letter-spacing: 0.3px !important;
}

.lyx_code_item b i,
.lyx_code_item i b {
    font-size: inherit !important;
    font-weight: bold !important;
    font-style: italic !important;
}

.toc,
.toc a,
.toc li,
.toc li a {
    color: var(--text-color);
    transition: color 0.2s ease;
}

.toc a:hover,
.toc li a:hover {
    color: var(--link-hover);
    text-decoration: underline;
}

.toc a:visited,
.toc a:active {
    color: var(--link-color);
}

div.float-figure img { 
    cursor: zoom-in; 
    transition: transform 0.3s ease;
}
div.float-figure img:hover {
    transform: scale(2.5);
    cursor: zoom-out;
	 z-index: 200;  /* higher order than sidebar */
	 position: relative;
}




.sidebar {
  height: 100%;
  width: 250px;
  position: fixed;
  z-index: 100;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  transition: 0.5s;
  padding-top: 60px;
}

.sidebar a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 15px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

.sidebar a:hover {
  color: #f1f1f1;
}

.sidebar .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

.openbtn {
  position: fixed;     /* Stay fixed while scrolling */
  top: 10px;           /* Distance from the top of the viewport */
  left: 10px;          /* Distance from the left edge */
  z-index: 1100;       /* Make sure it appears above the sidebar */
  background-color: #111;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  font-size: 18px;
}

.openbtn:hover {
  background-color: #444;
}

#main {
  transition: margin-left .5s;
  padding: 16px;
}

/* On smaller screens, where height is less than 450px, change the style of the sidenav (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidebar {padding-top: 15px;}
  .sidebar a {font-size: 18px;}
}
"""

    custom_sidebar = """
<div id="mySidebar" class="sidebar">
  <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">×</a>
  
  <a href="https://ynaghibi.github.io/AllBlogs/ML_Tutorials/Machine_Learning_For_Beginners/01_Introduction/">Intro</a>
  
  <a href="https://ynaghibi.github.io/AllBlogs/ML_Tutorials/Machine_Learning_For_Beginners/02_Small_Housing_Price_Project/">Small Housing Project</a>
  
  <a href="https://ynaghibi.github.io/AllBlogs/ML_Tutorials/Machine_Learning_For_Beginners/03_Big_Housing_Price_Project/">Big Housing Project</a>
  
</div>

<div id="main">
  <button class="openbtn" onclick="openNav()">☰ Contents</button> 
</div>

<script>
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}
</script>
"""

    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')

        # Find the style tag and append custom CSS
        style_tag = soup.find('style')
        if style_tag:
            style_tag.append(custom_css)
        else:
            new_style = soup.new_tag('style')
            new_style.string = custom_css
            soup.head.append(new_style)
		
			# Find the style tag and append custom CSS
        body_tag = soup.find('body')
        if body_tag:
            sidebar_soup = BeautifulSoup(custom_sidebar, 'html.parser')
            body_tag.insert(0, sidebar_soup)
            #body_tag.append(sidebar_soup) #alternative: at tag-bottom
            for elem in body_tag.find_all(recursive=False):
                if elem != sidebar_soup:
                    elem['class'] = elem.get('class', []) + ['main-content']

        # Remove empty math tags
        for math_tag in soup.find_all('math'):
            if not math_tag.contents or not math_tag.get_text(strip=True):
                parent = math_tag.parent
                if parent.name == 'div' and len(parent.contents) == 1:
                    parent.decompose()
                else:
                    math_tag.decompose()

        # Save to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Processed: {input_file} → {output_file}")

    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")

if __name__ == '__main__':
    # Process current directory and all subdirectories
    process_directory()