import streamlit as st
from real_time_infer import predict_attack
import shap
import matplotlib.pyplot as plt
from real_time_infer import explain_prediction

import os
import google.generativeai as genai
genai.configure(api_key="AIzaSyDiL5wA12s7b6JYL2Nu4AuI94ov-I9xX0c")  # Replace with your actual key


def ask_llm(query):
    try:
        st.write("🔍 Asking Gemini AI...")
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-001")
        response = model.generate_content(f"{query}\n\nPlease explain in 8-10 bullet points. Keep it concise and clear.")
        return response.text
    except Exception as e:
        print("❌ Gemini Error:", e)
        return f"❌ Gemini Error: {e}"

# Page configuration
st.set_page_config(page_title="🛡️ IoT Intrusion Detection", page_icon="🔒", layout="centered")

# Custom CSS for better appearance
# Custom CSS
st.markdown("""
<style>
    body {
        background-color: #111827;
        color: #e5e7eb;
    }
    .main {
        background-color: #1f2937;
        color: #f9fafb;
    }
    h1, h2, h3, h4 {
        color: #22d3ee;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #10b981;
        color: white;
        font-weight: 600;
        padding: 10px 16px;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #059669;
        color: #fff;
    }
    .stSuccess, .stInfo, .stWarning {
        font-size: 16px;
        padding: 10px;
        border-radius: 6px;
        background-color: #1e3a8a;
        color: #dbeafe;
    }
    .css-1v0mbdj p {
        font-size: 15px;
        line-height: 1.6;
    }
    .stMarkdown {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔒 IoT Intrusion Detection System")

# Instruction
st.markdown("### Enter network traffic data to detect potential threats:")

# Organized input fields
col1, col2 = st.columns(2)

with col1:
    duration = st.number_input("⏱️ Duration", min_value=0)
    protocol = st.selectbox("📡 Protocol", [0, 1, 2], format_func=lambda x: ["TCP", "UDP", "ICMP"][x])
    service = st.selectbox("🛠️ Service", [0, 1, 2, 3], format_func=lambda x: ["HTTP", "FTP", "DNS", "Telnet"][x])
    flag = st.selectbox("🚩 Flag", [0, 1, 2, 3], format_func=lambda x: ["SF", "REJ", "S0", "RSTR"][x])
    src_bytes = st.number_input("📤 Source Bytes", min_value=0)
    dst_bytes = st.number_input("📥 Destination Bytes", min_value=0)
    land = st.selectbox("🌐 Land", [0, 1])

with col2:
    wrong_fragment = st.number_input("🚧 Wrong Fragment", min_value=0)
    urgent = st.number_input("🚨 Urgent Packets", min_value=0)
    hot = st.number_input("🔥 Hot Count", min_value=0)
    num_failed_logins = st.number_input("❌ Failed Logins", min_value=0)
    logged_in = st.selectbox("🔑 Logged In", [0, 1])
    count = st.number_input("🔢 Connection Count", min_value=0)
    srv_count = st.number_input("📊 Service Count", min_value=0)

# Sliders for rates
st.markdown("### Connection Rates:")
col3, col4 = st.columns(2)

with col3:
    serror_rate = st.slider("🚨 Serror Rate", 0.0, 1.0)
    rerror_rate = st.slider("⚠️ Rerror Rate", 0.0, 1.0)

with col4:
    diff_srv_rate = st.slider("🔀 Diff Service Rate", 0.0, 1.0)
    same_srv_rate = st.slider("🔄 Same Service Rate", 0.0, 1.0)

# Additional counts
st.markdown("### Destination Host Info:")
col5, col6 = st.columns(2)
with col5:
    dst_host_count = st.number_input("🌍 Dst Host Count", min_value=0)
with col6:
    dst_host_srv_count = st.number_input("🌐 Dst Host Service Count", min_value=0)

# Compile inputs
sample = {
    'duration': duration,
    'protocol': protocol,
    'service': service,
    'flag': flag,
    'src_bytes': src_bytes,
    'dst_bytes': dst_bytes,
    'land': land,
    'wrong_fragment': wrong_fragment,
    'urgent': urgent,
    'hot': hot,
    'num_failed_logins': num_failed_logins,
    'logged_in': logged_in,
    'count': count,
    'srv_count': srv_count,
    'serror_rate': serror_rate,
    'rerror_rate': rerror_rate,
    'diff_srv_rate': diff_srv_rate,
    'same_srv_rate': same_srv_rate,
    'dst_host_count': dst_host_count,
    'dst_host_srv_count': dst_host_srv_count,
}

# Attack metadata (your existing dictionaries here)
attack_descriptions = {
    "normal": "Normal traffic. No threats detected.",
    "neptune": "DoS via TCP SYN flooding to exhaust server resources.",
    "smurf": "ICMP flooding using spoofed broadcast pings.",
    "guess_passwd": "Brute-force login attempts detected.",
    "buffer_overflow": "Exploit attempt using memory overflow vulnerability.",
    "portsweep": "Port scanning behavior to find open services.",
    "nmap": "Scanning tools like Nmap detected.",
    "teardrop": "Teardrop fragment attack attempting to crash targets.",
    "warezclient": "Unauthorized file access or downloads.",
    "satan": "Security scanning using tools like Satan."
}

# attack_precautions = {
#     "normal": ["All systems functioning as expected."],
#     "neptune": ["Enable SYN cookies.", "Rate-limit new connections.", "Deploy firewalls with DoS rules."],
#     "smurf": ["Disable IP-directed broadcasts.", "Use ingress filtering on routers."],
#     "guess_passwd": ["Enable 2FA.", "Limit login retries.", "Monitor login logs."],
#     "buffer_overflow": ["Patch vulnerable services.", "Use modern frameworks.", "Monitor unusual memory spikes."],
#     "portsweep": ["Use port-scan detection tools.", "Block suspicious IPs.", "Restrict unnecessary services."],
#     "nmap": ["Detect and alert aggressive scans.", "Use honeypots to mislead scanners."],
#     "teardrop": ["Update kernel/OS to mitigate known vulnerabilities."],
#     "warezclient": ["Limit file transfer privileges.", "Use antivirus with auto-quarantine."],
#     "satan": ["Harden network services.", "Block known scanners.", "Log and alert scan attempts."]
# }

# Predict button
if st.button("🔎 Detect Intrusion"):
    label = predict_attack(sample)
    st.session_state['label'] = label
    st.session_state['last_label'] = label
    st.success(f"**🛡️ Detected:** {label.upper()}")
    st.info(f"**📖 Description:** {attack_descriptions.get(label, 'N/A')}")

    # 🔍 SHAP Explanation
    # SHAP Explanation
    st.markdown("### 🔍 Why did the model predict this?")
    shap_values, input_df = explain_prediction(sample)

    # SHAP Force Plot
    shap.initjs()
    st.pyplot(
        shap.force_plot(
            base_value=shap_values[0].mean(),
            shap_values=shap_values[0][0],
            features=input_df,
            matplotlib=True,
            show=False
        ),
        bbox_inches="tight"
    )

    # ✅ Natural Language Explanation (Insert here)
    st.markdown("### 🧠 Model Explanation in Words")

    top_features = shap_values[0][0]
    top_indices = abs(top_features).argsort()[::-1][:5]

    explanation_lines = []
    for i in top_indices:
        feature = input_df.columns[i]
        value = input_df.iloc[0, i]
        impact = top_features[i]
        direction = "increased" if impact > 0 else "decreased"
        explanation_lines.append(f"- **{feature} = {value}** → {direction} the likelihood of this attack.")

    st.markdown("The model made this prediction based on these key inputs:")
    for line in explanation_lines:
        st.markdown(line)

# ✨ Ask AI block - completely outside the above condition
if 'last_label' in st.session_state:
    with st.expander("💬 Ask AI About This Attack"):
        default_question = f"What is {st.session_state['last_label']} attack and how to prevent it?"
        user_query = st.text_input("Ask a custom question:", value=default_question, key="ai_input")

        if 'ai_response' not in st.session_state:
            st.session_state['ai_response'] = ""

        if st.button("📢 Ask AI", key="ask_button"):
            if user_query.strip():
                st.session_state['ai_response'] = ask_llm(user_query)
            else:
                st.warning("Please enter a question.")

        if st.session_state['ai_response']:
            st.success(st.session_state['ai_response'])

    # Precautions
    # if 'label' in st.session_state:
    #     precautions = attack_precautions.get(st.session_state['label'], ["No precautions available."])
    #     with st.expander("⚠️ Recommended Precautions"):
    #         for tip in precautions:
    #             st.markdown(f"- {tip}")
    #
