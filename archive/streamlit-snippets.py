"""
Streamlit code snippets previously included in README.md.
Archived for reference.
"""
import streamlit as st
import pandas as pd
import datetime

# Mock database
if "decision_logs_db" not in st.session_state:
    st.session_state.decision_logs_db = []

st.title("💧 Aquaflow Tracker - Decision Log Documentation")

with st.form("add_decision_form", clear_on_submit=True):
    st.subheader("New Decision Log")

    decision_title = st.text_input("Decision Title")
    description = st.text_area("Decision Description")
    decided_by = st.text_input("Decided By")

    submitted = st.form_submit_button("Save Decision")

    if submitted:
        new_decision_id = f"D{len(st.session_state.decision_logs_db)+1:03d}"

        decision_payload = {
            "decision_id": new_decision_id,
            "title": decision_title,
            "description": description,
            "decided_by": decided_by,
            "decision_date": str(datetime.date.today())
        }

        st.session_state.decision_logs_db.append(decision_payload)

        st.success(f"Decision {new_decision_id} saved successfully!")

st.write("### Decision Log Records")

if st.session_state.decision_logs_db:
    st.dataframe(pd.DataFrame(st.session_state.decision_logs_db))
else:
    st.info("No decision logs recorded yet.")


if "retrospective_db" not in st.session_state:
    st.session_state.retrospective_db = []

st.title("💧 Aquaflow Tracker - Sprint Retrospective Notes")

with st.form("add_retrospective_form", clear_on_submit=True):
    st.subheader("Sprint Retrospective")

    sprint_name = st.text_input("Sprint Name")
    went_well = st.text_area("What Went Well?")
    needs_improvement = st.text_area("Needs Improvement")
    action_items = st.text_area("Action Items")

    submitted = st.form_submit_button("Save Notes")

    if submitted:
        new_note_id = f"SR{len(st.session_state.retrospective_db)+1:03d}"

        retrospective_payload = {
            "note_id": new_note_id,
            "sprint": sprint_name,
            "went_well": went_well,
            "needs_improvement": needs_improvement,
            "action_items": action_items,
            "date": str(datetime.date.today())
        }

        st.session_state.retrospective_db.append(retrospective_payload)

        st.success(f"Sprint retrospective {new_note_id} saved successfully!")

st.write("### Sprint Retrospective Records")

if st.session_state.retrospective_db:
    st.dataframe(pd.DataFrame(st.session_state.retrospective_db))
else:
    st.info("No sprint retrospective notes recorded yet.")
