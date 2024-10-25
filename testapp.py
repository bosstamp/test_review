import pandas as pd
import streamlit as st

# Predefined mappings for h4cd and h4nm
df_dict = pd.read_csv('test_class.csv')
h4cd_to_h4nm = dict(zip(df_dict['HRCHY4_CD'], df_dict['HRCHY4_NM']))

combined_options = [f"{key} - {value}" for key, value in h4cd_to_h4nm.items()]
# Reverse the dictionary for the reverse mapping
h4nm_to_h4cd = {v: k for k, v in h4cd_to_h4nm.items()}

# Load the CSV data
df = pd.read_csv("test_file.csv")

# Streamlit Title
st.title("Product H4 Review Demo")

# Add missing columns (if needed)
df['Review Status'] = df.get('Review Status', 'Not Reviewed')
df['h4nm_edit'] = df.get('h4nm_edit', None)
df['h4cd_edit'] = df.get('h4cd_edit', None)

# Navigation state to track the current row
if 'current_row' not in st.session_state:
    st.session_state.current_row = 0

# Total rows
total_rows = len(df)

# Navigation buttons with disabled states for boundaries
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.current_row > 0:
        if st.button("◀ Back"):
            st.session_state.current_row -= 1
with col2:
    if st.session_state.current_row < total_rows - 1:
        if st.button("Next ▶"):
            st.session_state.current_row += 1

# Display current row number and progress
current_row = st.session_state.current_row
st.progress((current_row + 1) / total_rows)
st.write(f"Showing row {current_row + 1} of {total_rows}")

# Display data for the current row
st.write(df.iloc[current_row][['PROD_ID', 'DISP_NM', 'SELECTED_H4_CD', 'SELECTED_H4_NM', 'PREDICTED_H4_CD_M1', 'PREDICTED_H4_NM_M1', 'PREDICTED_H4_CD_M2', 'PREDICTED_H4_NM_M2']])

# Add "Approved" and "Pending" buttons
col3, col4 = st.columns([1, 1])
with col3:
    if st.button("Approved", key=f"approved_{current_row}"):
        df.at[current_row, "Review Status"] = "Approved"
        st.success("Status set to Approved")
with col4:
    if st.button("Pending", key=f"pending_{current_row}"):
        df.at[current_row, "Review Status"] = "Pending"
        st.warning("Status set to Pending")

# Allow user to update "Review Status" under the "Approved" and "Pending" buttons
status = st.radio(
    "Review Status",
    options=["M1", "M2", "Selected", "DUMMY", "Reviewed"],
    index=0 if df.loc[current_row, "Review Status"] == "DUMMY" else 1
)
df.at[current_row, "Review Status"] = status

# If M1, allow `h4nm_edit` selection, auto-update `h4cd_edit`
if status == "M1":
    h4nm_selection = df.at[current_row, "PREDICTED_H4_NM_M1"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M1"]

if status == "M2":
    h4nm_selection = df.at[current_row, "PREDICTED_H4_NM_M2"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M2"]

if status == "Selected":
    h4nm_selection = df.at[current_row, "SELECTED_H4_NM"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "SELECTED_H4_CD"]

if status == "Reviewed":
    h4nm_selection = st.selectbox(
        "Select h4nm_edit:",
        options=combined_options,
        key=f"h4nm_edit_{current_row}"
    )
    selected_key = h4nm_selection.split(" - ")[0]
    df.at[current_row, "h4nm_edit"] = selected_key
    df.at[current_row, "h4cd_edit"] = h4cd_to_h4nm[selected_key]
    st.write(f"Corresponding h4cd_edit: {df.at[current_row, 'h4cd_edit']}")

# Initialize session state to track saved changes if not already initialized
if 'df' not in st.session_state:
    st.session_state.df = df.copy()  # Store a copy of the DataFrame in session state

# Button to save changes for the current row in the current page
if st.button("Save Changes", key=f"save_changes_{current_row}"):
    st.session_state.df.at[current_row, "h4nm_edit"] = df.at[current_row, "h4nm_edit"]
    st.session_state.df.at[current_row, "h4cd_edit"] = df.at[current_row, "h4cd_edit"]
    st.success(f"Changes saved for row {current_row}")

st.write("Updated Data for the Current Row:")
st.dataframe(df.iloc[[current_row]][['PROD_ID', 'DISP_NM', 'Review Status', 'h4cd_edit', 'h4nm_edit']])

# Ensure the download button uses the updated DataFrame (with saved changes)
csv = st.session_state.df.to_csv(index=False, encoding="utf-8-sig")
csv_bytes = csv.encode('utf-8-sig')

# Download the latest version of the DataFrame with the saved changes from all pages
st.download_button(
    label="Download Latest Updated CSV",
    data=csv_bytes,
    file_name='latest_updated_test_file.csv',
    mime='text/csv',
)
