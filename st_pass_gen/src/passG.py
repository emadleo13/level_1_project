import streamlit as st
from src.pass_gens import PinGenerator, RandomPasswordGenerator, MemorablePasswordGenerator

st.image("./images/banner.jpg", width=400)
st.title("Password Generator")


option = st.radio("Select a password type:", ("Random password", "Memorable password", "PIN code"))

if option == "PIN code":
    length = st.slider("Select PIN length:",4, 32)
    
    generator = PinGenerator(length)
    
elif option == "Random password":
    length = st.slider("Select password length:",8,100)
    include_number= st.toggle("Include Numbers")
    include_symbol= st.toggle("Include Symbols")
    
    generator = RandomPasswordGenerator(length, include_number, include_symbol)
    
elif option == "Memorable password":
    num_of_words = st.slider("Select numbers od password:", 2,10)
    separator = st.text_input("Separator", value=":")
    capitalization = st.toggle("Capitalization")
    
    generator = MemorablePasswordGenerator(num_of_words, separator, capitalization)

password = generator.generate()
st.write(fr"our password is: ```{password}``` ")









