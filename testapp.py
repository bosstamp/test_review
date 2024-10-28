import pandas as pd
import streamlit as st

# Streamlit Title
st.title("Product H4 Review Demo")

# Function to save DataFrame to CSV for downloading
def get_csv_bytes(df):
    return df.to_csv(index=False, encoding="utf-8-sig").encode('utf-8-sig')

# Predefined mappings for h4cd and h4nm
df_dict = pd.read_csv('test_class.csv')
h4cd_to_h4nm = dict(zip(df_dict['HRCHY4_CD'], df_dict['HRCHY4_NM']))
combined_options = [f"{key} - {value}" for key, value in h4cd_to_h4nm.items()]

# Load data and store it in session state if not already loaded
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv("test_file.csv")
    st.session_state.df['Review Status'] = st.session_state.df.get('Review Status', 'Not Reviewed')
    st.session_state.df['h4nm_edit'] = st.session_state.df.get('h4nm_edit', None)
    st.session_state.df['h4cd_edit'] = st.session_state.df.get('h4cd_edit', None)

# Access the DataFrame in session state
df = st.session_state.df

# Track the current row for navigation
if 'current_row' not in st.session_state:
    st.session_state.current_row = 0

# Total rows
total_rows = len(df)

# # Navigation buttons with disabled states at boundaries
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


# Columns for displaying row data and action buttons
col1, col2, col3 = st.columns([3, 1, 1])

# Display data for the current row
with col1:
    st.write(df.iloc[current_row][['PROD_ID', 'DISP_NM', 'SELECTED_H4_CD', 'SELECTED_H4_NM', 
                                   'PREDICTED_H4_CD_M1', 'PREDICTED_H4_NM_M1', 
                                   'PREDICTED_H4_CD_M2', 'PREDICTED_H4_NM_M2']])

# Define and auto-save button actions in col2 and col3
with col2:
    if st.button("Approved", key=f"approved_{current_row}"):
        df.at[current_row, "Review Status"] = "Approved"
        status = "Approved"
        df.at[current_row, "h4nm_edit"] = df.at[current_row, "SELECTED_H4_NM"]
        df.at[current_row, "h4cd_edit"] = df.at[current_row, "SELECTED_H4_CD"]
        st.session_state.df = df.copy()  # Auto-save on click

    if st.button("Use M1", key=f"status_m1_{current_row}"):
        df.at[current_row, "Review Status"] = "M1"
        status = "M1"
        df.at[current_row, "h4nm_edit"] = df.at[current_row, "PREDICTED_H4_NM_M1"]
        df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M1"]
        st.session_state.df = df.copy()  # Auto-save on click

    if st.button("Use M2", key=f"status_m2_{current_row}"):
        df.at[current_row, "Review Status"] = "M2"
        status = "M2"
        df.at[current_row, "h4nm_edit"] = df.at[current_row, "PREDICTED_H4_NM_M2"]
        df.at[current_row, "h4cd_edit"] = df.at[current_row, "PREDICTED_H4_CD_M2"]
        st.session_state.df = df.copy()  # Auto-save on click
    
    if st.button("DUMMY", key=f"dummy_{current_row}"):
        df.at[current_row, "Review Status"] = "DUMMY"
        status = "Dummy"
        df.at[current_row, "h4nm_edit"] = None  # Set h4nm_edit to None
        df.at[current_row, "h4cd_edit"] = None  # Set h4cd_edit to None
        st.session_state.df = df.copy()  # Auto-save on click

    if st.checkbox("Manual Assignment", key=f"manual_assignment_{current_row}"):
        df.at[current_row, "Review Status"] = "Reviewed"
        status = "Reviewed"
        st.session_state.df = df.copy()
        # h4nm_selection = st.selectbox(
        #     "Select h4nm_edit:",
        #     options=combined_options,
        #     key=f"h4nm_edit_{current_row}"
        # )
        # selected_key = h4nm_selection.split(" - ")[0]
        # df.at[current_row, "h4nm_edit"] = selected_key
        # df.at[current_row, "h4cd_edit"] = h4cd_to_h4nm[selected_key]
        # st.session_state.df = df.copy()  # Auto-save on assignment
    else:
        status = df.at[current_row, "Review Status"]

with col3:
    if st.button("Pending", key=f"pending_{current_row}"):
        df.at[current_row, "Review Status"] = "Pending"
        status = "Pending"
        df.at[current_row, "h4nm_edit"] = None  # Set h4nm_edit to None
        df.at[current_row, "h4cd_edit"] = None  # Set h4cd_edit to None
        st.session_state.df = df.copy()  # Auto-save on click
    else:
        status = df.at[current_row, "Review Status"]

if status == "Reviewed":
        h4nm_selection = st.selectbox(
            "Select h4nm_edit:",
            options=combined_options,
            key=f"h4nm_edit_{current_row}"
        )
        selected_key = h4nm_selection.split(" - ")[0]
        df.at[current_row, "h4nm_edit"] = selected_key
        df.at[current_row, "h4cd_edit"] = h4cd_to_h4nm[selected_key]
        st.session_state.df = df.copy()  # Auto-save on assignment
# Display the updated review status for the current row
st.write(f"Review Status: {df.at[current_row, 'Review Status']}")

st.write("Updated Data for the Current Row:")
st.dataframe(df.iloc[[current_row]][['PROD_ID', 'DISP_NM', 'Review Status', 'h4cd_edit', 'h4nm_edit']])
# Download button to download the updated DataFrame
csv_bytes = get_csv_bytes(st.session_state.df)
st.download_button(
    label="Download Latest Updated CSV",
    data=csv_bytes,
    file_name='latest_updated_test_file.csv',
    mime='text/csv',
)
