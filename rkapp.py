import streamlit as st
import pandas as pd
import os

# File to store patient data
DATA_FILE = "patients_data.csv"

# Initialize the CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Name", "Age", "Gender", "Contact", 
        "Blood Type", "Allergies", "Medical History"
    ])
    df.to_csv(DATA_FILE, index=False)

# Load existing data
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit App
st.title("🏥 Patient Health Records")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Add Patient", "View Patients"])
df = load_data()

if menu == "Add Patient":
    st.subheader("Add New Patient Record")
    
    with st.form("patient_form"):
        name = st.text_input("Full Name*")
        age = st.number_input("Age*", min_value=0, max_value=120)
        gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
        contact = st.text_input("Contact Number*")
        blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
        allergies = st.text_input("Allergies (if any)")
        medical_history = st.text_area("Medical History")
        
        submitted = st.form_submit_button("Save Patient")
        
        if submitted:
            if not name or not age or not gender or not contact:
                st.error("Please fill required fields (*)!")
            else:
                new_patient = pd.DataFrame([{
                    "Name": name,
                    "Age": age,
                    "Gender": gender,
                    "Contact": contact,
                    "Blood Type": blood_type,
                    "Allergies": allergies,
                    "Medical History": medical_history
                }])
                df = pd.concat([df, new_patient], ignore_index=True)
                save_data(df)
                st.success("Patient record saved!")

elif menu == "View Patients":
    st.subheader("View Patient Records")
    
    # Search by name
    search_name = st.text_input("Search by Name")
    if search_name:
        filtered_df = df[df["Name"].str.contains(search_name, case=False)]
    else:
        filtered_df = df
    
    # Display data
    st.dataframe(filtered_df)
    
    # Download data as CSV
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="patients_data.csv",
        mime="text/csv"
    )