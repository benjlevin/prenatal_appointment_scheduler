import streamlit as st
from datetime import datetime, timedelta

def parse_mmddyyyy(date_str):
    if len(date_str) != 8 or not date_str.isdigit():
        raise ValueError("Please enter the date in MMDDYYYY format (e.g., 05252025)")
    return datetime.strptime(date_str, "%m%d%Y")

def generate_schedule(edd_str, first_visit_str):
    try:
        edd = parse_mmddyyyy(edd_str)
        first_visit = parse_mmddyyyy(first_visit_str)
    except ValueError as e:
        return str(e), None

    schedule = []
    current_date = first_visit

    while current_date <= edd + timedelta(weeks=7):
        ga_days = (current_date - (edd - timedelta(weeks=40))).days
        ga_weeks = int(ga_days // 7)

        if ga_weeks < 28:
            interval = timedelta(weeks=4)
        elif 28 <= ga_weeks < 36:
            interval = timedelta(weeks=2)
        elif 36 <= ga_weeks < 42:
            interval = timedelta(weeks=1)
        elif 42 <= ga_weeks < 47:
            interval = timedelta(weeks=4)
        else:
            if ga_weeks >= 47:
                break
            
        visit_str = f"- Visit {len(schedule) + 1}: {ga_weeks}w on ~{current_date.strftime('%m/%d/%Y')}"
        schedule.append(visit_str)
        current_date += interval

    return None, "\n".join(schedule)

# Streamlit UI
st.title("🩺 Prenatal Appointment Schedule Generator")

edd_input = st.text_input("Estimated Due Date (MMDDYYYY):")
first_visit_input = st.text_input(
    "First Visit Date (MMDDYYYY):",
    value=datetime.today().strftime("%m%d%Y")
)

if st.button("Generate Schedule"):
    error, schedule = generate_schedule(edd_input, first_visit_input)
    if error:
        st.error(error)
    else:
        st.success("Schedule generated successfully!")
        st.text_area("Schedule:", value=schedule, height=300)
        st.download_button("Download Schedule as .txt", schedule, file_name="prenatal_schedule.txt")
