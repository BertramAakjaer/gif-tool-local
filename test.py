import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import plotly.express as px  # For interactive charts
from PIL import Image  # For image handling
import io  # For in-memory image handling
from io import BytesIO


# --- Page Configuration (Optional but good practice) ---
st.set_page_config(
    page_title="Streamlit Feature Showcase",
    page_icon=":rocket:",  # Use an emoji or path to an image file
    layout="wide",  # "wide" or "centered" (default is centered)
    initial_sidebar_state="expanded",  # "auto", "expanded", or "collapsed"
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a showcase of Streamlit features!"
    }
)


# --- Sidebar ---
st.sidebar.header("Sidebar Controls")
sidebar_checkbox = st.sidebar.checkbox("Show/Hide Sidebar Section")

if sidebar_checkbox:
    st.sidebar.subheader("Sidebar Input")
    sidebar_radio = st.sidebar.radio("Choose an option:", ("A", "B", "C"))
    sidebar_select = st.sidebar.selectbox("Select from dropdown:", ["Option 1", "Option 2", "Option 3"])
    sidebar_multiselect = st.sidebar.multiselect("Multiselect:", ["Red", "Green", "Blue"])
    sidebar_slider = st.sidebar.slider("Sidebar Slider", 0, 100, 50)
    sidebar_number_input = st.sidebar.number_input("Sidebar Number Input", min_value=0, max_value=100, value=25)
    sidebar_date_input = st.sidebar.date_input("Sidebar Date", datetime.date(2024, 1, 1))
    sidebar_time_input = st.sidebar.time_input("Sidebar Time", datetime.time(12, 0))
    sidebar_file_uploader = st.sidebar.file_uploader("Sidebar File Uploader", type=["csv", "txt", "xlsx"])
    sidebar_color_picker = st.sidebar.color_picker("Sidebar Color Picker", "#ff0000")
    with st.sidebar.expander("Sidebar Expander"):  # Collapsible section in the sidebar
        st.write("This content is inside a sidebar expander.")
        st.write("You can put any widgets you want inside.")
    sidebar_text_input = st.sidebar.text_input("Sidebar text input", value = 'Text Input')



# --- Main Page ---
st.title("Streamlit Feature Showcase")


# --- Text Elements ---
st.header("Text Elements")
st.subheader("Subheader Example")
st.text("This is some plain text.")
st.markdown("**Bold** and *italic* text using Markdown.")
st.caption("This is a caption.")
st.code("import streamlit as st", language="python")
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')  # LaTeX for mathematical expressions
st.write("This uses `st.write()` and can display multiple arguments, including dataframes, plots, etc.")



# --- Input Widgets ---
st.header("Input Widgets")

col1, col2, col3 = st.columns(3)  # Create columns for layout

with col1:
    text_input = st.text_input("Text Input", "Enter text here...")
    number_input = st.number_input("Number Input", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    text_area = st.text_area("Text Area", "Enter multi-line text...")
    date_input = st.date_input("Date Input", datetime.date(2023, 7, 4))

with col2:
    time_input = st.time_input("Time Input", datetime.time(8, 45))
    checkbox = st.checkbox("Checkbox")
    radio = st.radio("Radio Buttons", ("Option 1", "Option 2", "Option 3"))
    select = st.selectbox("Select Box", ["Red", "Green", "Blue"])

with col3:
    multiselect = st.multiselect("Multiselect", ["Apple", "Banana", "Orange"], ["Apple", "Banana"])
    slider = st.slider("Slider", 0, 100, 25, 5)  # (label, min, max, default, step)
    color_picker = st.color_picker("Color Picker", "#00f900")

    uploaded_file = st.file_uploader("File Uploader", type=["csv", "png", "jpg"]) # Multiple file types

# Handling File Uploads
if uploaded_file is not None:
    # Check file type and handle accordingly
    if uploaded_file.type == "text/csv":
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV Data:")
        st.dataframe(df_uploaded)  # Show the uploaded CSV data
    elif uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.write("Unsupported file type.")


# --- Data Display ---
st.header("Data Display")

# Dataframe
st.subheader("DataFrame")
df = pd.DataFrame({
    'col1': [1, 2, 3, 4],
    'col2': [10, 20, 30, 40],
    'col3': ['A', 'B', 'C', 'D']
})
st.dataframe(df)  # Interactive table
# st.table(df) # Static table

# JSON
st.subheader("JSON")
json_data = {"key1": "value1", "key2": [1, 2, 3]}
st.json(json_data)

# Metrics
st.subheader("Metrics")
col1_m, col2_m, col3_m = st.columns(3)
col1_m.metric("Temperature", "70 °F", "1.2 °F")
col2_m.metric("Wind", "9 mph", "-8%")
col3_m.metric("Humidity", "86%", "4%")


# --- Charts ---
st.header("Charts")

# Generate some sample data for charts
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

# Streamlit's built-in charts
st.subheader("Streamlit Native Charts")
st.line_chart(chart_data)
st.area_chart(chart_data)
st.bar_chart(chart_data)

st.subheader("Plotly Chart (Interactive)")
fig = px.scatter(chart_data, x='a', y='b', color='c', title="Interactive Scatter Plot")
st.plotly_chart(fig, use_container_width=True)  # Make it full-width


# --- Media ---
st.header("Media")

# Image
st.subheader("Image")
try:
    image = Image.open("path/to/your/image.jpg") #REPLACE with your image
    st.image(image, caption="Example Image", use_column_width=True) #use the image
except FileNotFoundError:
    st.warning("Image not found.  Please replace 'path/to/your/image.jpg' with a valid image path.")
    # Create a sample image if the file is not found (good for testing)
    sample_image = Image.new("RGB", (200, 200), color="red")  # Create a red 200x200 image
    img_io = io.BytesIO()
    sample_image.save(img_io, 'JPEG')
    img_io.seek(0)
    st.image(img_io, caption="Sample Red Image", use_column_width=True)


# Video (requires a valid video file)
st.subheader("Video")
try:
    video_file = open('path/to/your/video.mp4', 'rb') #REPLACE with a valid path
    video_bytes = video_file.read()
    st.video(video_bytes)

except FileNotFoundError:
    st.warning("Video file not found.  Please replace 'path/to/your/video.mp4' with a valid video file path.")
    # Example with a placeholder (e.g., a YouTube video)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Classic placeholder :)


# Audio (requires a valid audio file)
st.subheader("Audio")
try:
    audio_file = open('path/to/your/audio.mp3', 'rb') # REPLACE with a valid path
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
except FileNotFoundError:
    st.warning("Audio file not found. Please replace 'path/to/your/audio.mp3' with a valid audio path.")
    # Provide a sample using a URL (less ideal, but better than nothing)
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")



# --- Layout ---
st.header("Layout")

# Columns
st.subheader("Columns")
col1, col2 = st.columns(2)  # Two columns
with col1:
    st.write("This is in column 1.")
with col2:
    st.write("This is in column 2.")

# Expander
st.subheader("Expander")
with st.expander("Click to expand"):
    st.write("Hidden content revealed!")

# Tabs
st.subheader("Tabs")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("Content for tab 1")
with tab2:
    st.write("Content for tab 2")
with tab3:
    st.write("Content for tab 3")

# Containers  (useful for grouping elements visually)
st.subheader("Containers")
with st.container():
    st.write("Inside a container.  Visually groups these elements.")
    st.button("Button inside container")


# --- Status Elements ---
st.header("Status Elements")

# Progress Bar
st.subheader("Progress Bar")
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.02)  # Simulate some work
    my_bar.progress(percent_complete + 1)

# Spinner
st.subheader("Spinner")
with st.spinner("Waiting for something..."):
    time.sleep(3)  # Simulate a long-running process
st.success("Done!")

# Balloons (for celebration!)
# st.balloons()  # Uncomment to show balloons

# Error/Warning/Info Messages
st.error("This is an error message.")
st.warning("This is a warning message.")
st.info("This is an informational message.")
st.success("This is a success message.")

# Exception Display
st.subheader("Exception")
try:
    1 / 0  # Cause an error
except Exception as e:
    st.exception(e)


# --- Chat elements ---
st.header("Chat Elements (Streamlit 1.26.0+)")
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

with st.chat_message("assistant"):
    st.write("Hello, I am here to answer your questions!")

user_input = st.chat_input("Say something")
if user_input:
    st.write(f"User said: {user_input}")


# --- Callbacks and State ---
st.header("Callbacks and Session State")

# Simple counter example with session state
if 'count' not in st.session_state:
    st.session_state.count = 0  # Initialize the counter

def increment_counter():
    st.session_state.count += 1

st.button("Increment", on_click=increment_counter)
st.write("Count = ", st.session_state.count)

# More complex example - storing a list in session state
if "my_list" not in st.session_state:
    st.session_state.my_list = []

add_to_list = st.text_input("Add to list")
if st.button("Add"):
    st.session_state.my_list.append(add_to_list)

st.write("List:", st.session_state.my_list)



# --- Placeholder ---
st.header("Placeholder")
placeholder = st.empty()  # Create an empty placeholder

# Now replace the placeholder with different content
with placeholder.container():
    st.write("This is the initial content.")
    st.button("Initial Button")

if st.button("Replace Content"):
    placeholder.empty()  # Clear the placeholder
    with placeholder.container():  # Re-use the placeholder
        st.write("This is the new content!")
        st.button("New Button")
    # placeholder.text("This is the new content!") # Or with a single element

# --- Form ---
st.header("Form")
with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")



# --- Utilities ---

st.header("Utilities")
st.write("Current time (using `st.experimental_rerun`):", datetime.datetime.now())

if st.button("Rerun the script"):
    st.experimental_rerun()

st.stop()  # Stop execution further down the script