import io

import streamlit as st



from data_loader import (
    load_data,
    load_config,
    load_multimodal,
    merge_sensor_into_main,
    validate_data,
)
from analysis import run_eda, run_mixed_model
from plotting import plot_trajectories, plot_sensor_feature
from llm_writer import generate_methods_results_text
from report_generator import build_markdown_report


st.set_page_config(page_title="AI Outcomes Synthesizer", layout="wide")

st.title("AI Outcomes Synthesizer for Longitudinal Mental-Health Studies (Multimodal)")

st.write(
    "Upload a longitudinal clinical dataset and a JSON config. "
    "This app merges sensor features, runs a mixed-effects model, "
    "and generates AI-assisted draft text for Methods, Results, and an Executive Summary."
)

col1, col2 = st.columns(2)

with col1:
    csv_file = st.file_uploader(
        "Upload clinical CSV data",
        type=["csv"],
        help="Use clinical_longitudinal_data.csv for the demo.",
    )
with col2:
    config_file = st.file_uploader(
        "Upload JSON config",
        type=["json"],
        help="Use config_example.json for the demo.",
    )

if csv_file and config_file:
    try:
        config = load_config(config_file)
        df = load_data(csv_file)

        modalities = load_multimodal(config)
        df = merge_sensor_into_main(df, config, modalities)

        valid, msg = validate_data(df, config)
        if not valid:
            st.error(msg)
        else:
            st.success("Data, multimodal inputs, and config loaded successfully.")

            st.subheader("Data Preview (Clinical + Sensor)")
            st.dataframe(df.head())

            text_df = modalities.get("text")
            if text_df is not None:
                st.subheader("Text Notes Preview")
                st.dataframe(text_df.head())

            if st.button("Run Analysis"):
                with st.spinner("Running EDA and mixed-effects model..."):
                    eda_summary = run_eda(df, config)
                    model_text, model_summary = run_mixed_model(df, config)

                st.subheader("Descriptive Statistics")
                st.json(eda_summary["overall_desc"])

                st.subheader("Trajectory Plot (Outcome)")
                fig = plot_trajectories(df, config)
                st.pyplot(fig)

                sensor_features = ["avg_steps", "sleep_hours", "phone_usage_minutes"]
                for feat in sensor_features:
                    if feat in df.columns:
                        st.subheader(f"Sensor Feature: {feat}")
                        fig_feat = plot_sensor_feature(df, feat, config)
                        st.pyplot(fig_feat)

                st.subheader("Model Summary (Text)")
                st.text(model_text)

                text_examples = None
                if text_df is not None and not text_df.empty:
                    sample = text_df.sample(n=min(5, len(text_df)))["note_text"].tolist()
                    text_examples = "\n".join(f"- {t}" for t in sample)

                with st.spinner("Generating AI-assisted Methods, Results, and Summary..."):
                    sections = generate_methods_results_text(
                        config,
                        model_summary,
                        text_examples=text_examples,
                    )

                st.subheader("Methods (Draft)")
                st.write(sections.get("methods", ""))

                st.subheader("Results (Draft)")
                st.write(sections.get("results", ""))

                st.subheader("Executive Summary (Draft)")
                st.write(sections.get("executive_summary", ""))

                report_md = build_markdown_report(
                    config,
                    eda_summary,
                    model_text,
                    sections,
                )
                b = io.BytesIO(report_md.encode("utf-8"))

                st.download_button(
                    label="Download Markdown Report",
                    data=b,
                    file_name="longitudinal_multimodal_report.md",
                    mime="text/markdown",
                )
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload both a clinical CSV dataset and a JSON config to proceed.")
