import streamlit as st
on = st.toggle("select your idea")

if on:
    st.write("your idea is selected!!!")
    
    



color = st.select_slider("select a color of the rainbow", options =[ "red", "orange", "yellow", "green", "blue", "indigo", "violet",],)
st.write("My favorite color is", color)



start_color, end_color = st.select_slider(
    "Select a range of color wavelength",
    options=[
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
    ],
    value=("red", "blue"),
)
st.write("You selected wavelengths between", start_color, "and", end_color)



option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home Phone", "Mobile Phone", "Home Address", "SMS","WhatsApp"),
    index = None, 
    placeholder = "Select contact method ...",)
st.write(
    "You selected :" , option,)
if option is not None:
    (f"your select is {option} and  ecxiting!!!")
    
    
    


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    
col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable select box widget", key = "Disabled")
    st.radio("Set selectbox label visibility -->> ", key="Visibility", options = ["visible", "hidden", "collapsed"],)
    
    
with col2:
    option = st.selectbox("How would you like to be contacted?", ("Email", "Home Phone", "Mobile Phone", "Home Address", "SMS","WhatsApp"), label_visibility = st.session_state.visibility, disabled= st.session_state.disabled,)





option = ["North", "East", "South", "West"]
selection = st.segmented_control("Direction", option, selection_mode= "multi")

st.markdown(f"Your selected option is : {selection}.")




option_map = {0: ":material/add:",
1: ":material/zoom_in:",
2: ":material/zoom_out:",
3: ":material/zoom_out_map:",}

selection = st.segmented_control("Tool", options = option_map.keys(), format_func = lambda option: option_map[option], selection_mode= "single")

st.write( "Your selected option:" f" {None if selection is None else option_map[selection]}")













