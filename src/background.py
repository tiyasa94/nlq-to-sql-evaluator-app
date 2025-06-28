import streamlit as st
import os
import base64


def set_custom_title(title_text, color_code):
    st.markdown(
        f"<h1 style='color: {color_code}; text-align: center;'>{title_text}</h1>",
        unsafe_allow_html=True
    )


def set_custom_subtitle(title_text, color_code):
    st.markdown(f"<h4 style='color: {color_code};'>{title_text}</h4>", unsafe_allow_html=True)


def add_bg_from_local(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{image_data}");
                    background-size: cover;
                    background-position: center;
                    height: 100vh;
                    width: 100vw;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("Background image not found. Skipping...")



def add_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0049ff;
            color: white;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.2);
            z-index: 999;
        }
        </style>

        <div class="footer">
            © 2025 Text-to-SQL Pipeline Evaluator - Powered by watsonX
        </div>
        """,
        unsafe_allow_html=True,
    )        