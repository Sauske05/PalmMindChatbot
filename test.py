import streamlit as st

# Initialize session state to track if the button is clicked

# Main panel
st.title("Main Panel")
st.write("Click the button below to display the form in the sidebar.")

# Button in the main panel
if st.button("Show Form"):
    st.session_state.button_clicked = True

# Sidebar with a form
if st.session_state.button_clicked:
    with st.sidebar:
        st.header("Sidebar Form")
        name = st.text_input("Enter your name")
        age = st.number_input("Enter your age", min_value=0, max_value=100)
        submit_button = st.button("Submit Form")

        # Process form data
        if submit_button:
            st.write(f"Name: {name}")
            st.write(f"Age: {age}")
            st.write("Form has been submitted. Thank you!")
else:
    with st.sidebar:
        st.write("Form will be displayed here after clicking the button.")
