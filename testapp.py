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
st.title("Product H4 review demo")

# Add missing columns (if needed)
df['Review Status'] = df.get('Review Status', 'Not Reviewed')
df['h4nm_edit'] = df.get('h4nm_edit', None)
df['h4cd_edit'] = df.get('h4cd_edit', None)

# Navigation state to track current row
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
st.write(df.iloc[current_row][['PROD_ID', 'DISP_NM', 'SELECTED_H4_CD', 'SELECTED_H4_NM','PREDICTED_H4_CD_M1','PREDICTED_H4_NM_M1','PREDICTED_H4_CD_M2','PREDICTED_H4_NM_M2']])


# Allow user to update "Review Status"
status = st.radio(
    "Review Status",
    options=["M1","M2","Selected","DUMMY", "Reviewed"],
    index=0 if df.loc[current_row, "Review Status"] == "DUMMY" else 1
)
df.at[current_row, "Review Status"] = status

# If m1, allow `h4nm_edit` selection, auto-update `h4cd_edit`
if status == "M1":
    # Auto-update based on the value in the `PREDICTED_H4_NM_M1` column
    h4nm_selection = df.at[current_row, "PREDICTED_H4_NM_M1"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M1"]

if status == "M2":
    # Auto-update based on the value in the `PREDICTED_H4_NM_M1` column
    h4nm_selection = df.at[current_row, "PREDICTED_H4_NM_M2"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M2"]

if status == "Selected":
    # Auto-update based on the value in the `PREDICTED_H4_NM_M1` column
    h4nm_selection = df.at[current_row, "SELECTED_H4_NM"]
    df.at[current_row, "h4nm_edit"] = h4nm_selection
    df.at[current_row, "h4cd_edit"] = df.at[current_row, "SELECTED_H4_CD"]

# If reviewed, allow `h4nm_edit` selection, auto-update `h4cd_edit`
if status == "Reviewed":
    h4nm_selection = st.selectbox(
        "Select h4nm_edit:",
        # options=list(h4nm_to_h4cd.keys()),
        options=combined_options,
        key=f"h4nm_edit_{current_row}"
    )
    # Extract the key from the selection
    selected_key = h4nm_selection.split(" - ")[0]

    # Update the corresponding `h4nm_edit` and `h4cd_edit`
    df.at[current_row, "h4nm_edit"] = selected_key
    df.at[current_row, "h4cd_edit"] = h4cd_to_h4nm[selected_key]
    # df.at[current_row, "h4nm_edit"] = h4nm_selection
    # df.at[current_row, "h4cd_edit"] = h4nm_to_h4cd[h4nm_selection]

    st.write(f"Corresponding h4cd_edit: {df.at[current_row, 'h4cd_edit']}")

# # Add a text input for searching `h4nm_to_h4cd` dictionary keys

# # if status == "Reviewed":
# if status == "Reviewed":
#     st.write("Search and Select h4nm_edit:")
    
#     # Clear, concise prompt to guide user
#     search_term = st.text_input("", key=f"search_h4nm_{current_row}")
    
#     # Filter the options based on the search term (case-insensitive)
#     filtered_options = [k for k in h4nm_to_h4cd.keys() if search_term.lower() in k.lower()]

#     # Show a real-time dropdown list of matching options
#     if filtered_options:
#         h4nm_selection = st.selectbox(
#             "Matching results:",
#             options=filtered_options,
#             key=f"h4nm_edit_{current_row}"
#         )
#     else:
#         st.warning("No results found. Try refining your search.")
#         # Show all options if no match is found
#         h4nm_selection = st.selectbox(
#             "Select h4nm_edit:",
#             options=list(h4nm_to_h4cd.keys()),
#             key=f"h4nm_edit_{current_row}"
#         )

#     # Update the corresponding `h4nm_edit` and `h4cd_edit`
#     df.at[current_row, "h4nm_edit"] = h4nm_selection
#     df.at[current_row, "h4cd_edit"] = h4nm_to_h4cd[h4nm_selection]

#     # Display the corresponding `h4cd_edit`
#     st.write(f"Corresponding h4cd_edit: {df.at[current_row, 'h4cd_edit']}")

# Initialize the session state to track saved changes if not already initialized
if 'df' not in st.session_state:
    st.session_state.df = df.copy()  # Store a copy of the DataFrame in session state

# Button to save changes for the current row in the current page
if st.button("Save Changes", key=f"save_changes_{current_row}"):
    # Save the changes to the session state DataFrame
    st.session_state.df.at[current_row, "h4nm_edit"] = df.at[current_row, "h4nm_edit"]
    st.session_state.df.at[current_row, "h4cd_edit"] = df.at[current_row, "h4cd_edit"]
    st.success(f"Changes saved for row {current_row}")

st.write("Updated Data for the Current Row:")
st.dataframe(df.iloc[[current_row]][['PROD_ID', 'DISP_NM','Review Status', 'h4cd_edit', 'h4nm_edit']])

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
