import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Responsible AI Bias Audit",
    page_icon="⚖️",
    layout="wide"
)

st.title("Responsible AI and Bias Audit of a Chatbot")
st.write("A simple dashboard to evaluate chatbot fairness and bias.")

if "results" not in st.session_state:
    st.session_state.results = []

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Bias Audit", "Results", "About"]
)

if menu == "Dashboard":
    st.header("Project Dashboard")
    st.metric("Total Audits", len(st.session_state.results))
    st.write("### Project Objectives")
    st.write("- Identify possible chatbot bias.")
    st.write("- Compare chatbot responses.")
    st.write("- Evaluate fairness and accuracy.")
    st.write("- Suggest improvements.")

elif menu == "Bias Audit":
    st.header("Chatbot Bias Audit")

    with st.form("audit_form"):
        test_id = st.text_input("Test ID")
        category = st.selectbox(
            "Bias Category",
            ["Gender", "Language", "Age", "Accessibility", "Other"]
        )
        prompt_a = st.text_area("Prompt A")
        response_a = st.text_area("Chatbot Response A")
        prompt_b = st.text_area("Prompt B")
        response_b = st.text_area("Chatbot Response B")

        st.subheader("Evaluation (0 to 2)")
        fairness = st.selectbox("Fairness", [0, 1, 2])
        tone = st.selectbox("Respectful Tone", [0, 1, 2])
        relevance = st.selectbox("Relevance", [0, 1, 2])
        consistency = st.selectbox("Consistency", [0, 1, 2])
        accuracy = st.selectbox("Accuracy", [0, 1, 2])

        risk = st.selectbox("Risk Level", ["Low", "Medium", "High"])
        notes = st.text_area("Observations")
        submit = st.form_submit_button("Submit Audit")

    if submit:
        if not all([
            test_id.strip(), prompt_a.strip(), response_a.strip(),
            prompt_b.strip(), response_b.strip()
        ]):
            st.error("Please complete all required fields.")
        else:
            score = fairness + tone + relevance + consistency + accuracy

            st.session_state.results.append({
                "Test ID": test_id,
                "Category": category,
                "Score / 10": score,
                "Risk": risk,
                "Observations": notes,
                "Date": datetime.now().strftime("%Y-%m-%d")
            })

            st.success("Audit saved successfully!")
            st.metric("Audit Score", f"{score}/10")

elif menu == "Results":
    st.header("Audit Results")

    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("Test ID")["Score / 10"])

        st.download_button(
            "Download Results CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="bias_audit_results.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit results available yet.")

elif menu == "About":
    st.header("About This Project")
    st.write("Project: Responsible AI and Bias Audit of a Chatbot")
    st.write("Technology: Python, Streamlit and Pandas")
    st.write("Purpose: Evaluate chatbot fairness, tone and consistency.")
    st.write("Results depend on the test prompts and human evaluation.")
