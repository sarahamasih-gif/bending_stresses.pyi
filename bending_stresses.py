import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plot_stress(H, yNA, y_max, I, M, beam_type):
    y = np.linspace(0, H, 200)
    stress = M * (y - yNA) / I
    fig, ax = plt.subplots()
    ax.plot(stress, y)
    ax.axhline(yNA, color='red', linestyle='--')
    ax.axvline(0, color='black')
    ax.fill_betweenx(y, 0, stress, where=(stress >= 0), color='lightblue', alpha=0.6)
    ax.fill_betweenx(y, 0, stress, where=(stress < 0), color='lightblue', alpha=0.6)
    ax.set_xlabel('Stress (N/mm2)')
    ax.set_ylabel('Height from bottom (mm)')
    ax.set_title(f'{beam_type} - Max Stress {max(abs(stress)):.2f}')
    ax.grid(True)
    return fig

def get_M_and_beamtype():
    st.subheader("Support & Loading")
    choice = st.selectbox("Select Support Type", ["1. Simply Supported beam (UDL)", "2. Cantilever beam (UDL)", "3. Cantilever beam (Point Load)"])
    l = st.number_input("Enter length of beam in m", value=None, placeholder="Enter length...")
    w = st.number_input("Enter load (N or N/mm)", value=None, placeholder="Enter load...")
    
    if l is None or w is None:
        return None, None, None
    
    L = l * 1000
    if "1." in choice:
        M = (w * L**2) / 8
        beam_type = "SS_UDL"
        st.info(f"M = (w*L²)/8 = {M:.2f} N-mm")
    elif "2." in choice:
        M = (w * L**2) / 2
        beam_type = "Cantilever_UDL"
        st.info(f"M = (w*L²)/2 = {M:.2f} N-mm")
    else:
        M = (w * L)
        beam_type = "Cantilever_PtLOAD"
        st.info(f"M = w*L = {M:.2f} N-mm")
    
    return M, beam_type, L

st.set_page_config(layout="wide")
st.title("Bending Stress Calculator Dashboard")
section = st.sidebar.selectbox("Select Cross-Section", ["Rectangle", "T Section", "I Section", "L Section", "C Section"])

M, beam_type, L = get_M_and_beamtype()

if M is None:
    st.warning("Please enter length and load to continue")
    st.stop()

st.divider()

# --- RECTANGLE ---
if section == "Rectangle":
    st.header("Rectangle Section")
    col1, col2 = st.columns(2)
    with col1:
        b = st.number_input("Enter width b in mm", value=None, placeholder="Empty", key="R_b")
    with col2:
        h = st.number_input("Enter depth h in mm", value=None, placeholder="Empty", key="R_h")
    
    if b is not None and h is not None:
        I = (b * h**3) / 12
        yNA = h / 2
        H = h
        y_max = yNA
        sigma = (M * y_max) / I
        st.write(f"I = {I:.2f} mm⁴, yNA = {yNA:.2f} mm")
        st.success(f"Sigma = {sigma:.2f} N/mm²")
        st.pyplot(plot_stress(H, yNA, y_max, I, M, beam_type))

# --- T SECTION ---
elif section == "T Section":
    st.header("T Section")
    c1, c2 = st.columns(2)
    with c1:
        Fb = st.number_input("Flange width in mm", value=None, placeholder="Empty", key="T_Fb")
        Fh = st.number_input("Flange depth in mm", value=None, placeholder="Empty", key="T_Fh")
    with c2:
        Wb = st.number_input("Web width in mm", value=None, placeholder="Empty", key="T_Wb")
        Wh = st.number_input("Web depth in mm", value=None, placeholder="Empty", key="T_Wh")

    if None not in (Fb, Fh, Wb, Wh):
        Af = Fb*Fh; Aw = Wb*Wh
        yw = Wh/2; yf = Wh + (Fh/2)
        yNA = ((Af*yf)+(Aw*yw))/(Af+Aw)
        I = ((Fb*Fh**3)/12)+(Af*(yNA-yf)**2)+((Wb*Wh**3)/12)+(Aw*(yNA-yw)**2)
        H = Fh+Wh; y_max = max(yNA, H-yNA); sigma = (M*y_max)/I
        st.success(f"I={I:.2f}, yNA={yNA:.2f}, Sigma={sigma:.2f}")
        st.pyplot(plot_stress(H, yNA, y_max, I, M, beam_type))

# --- I SECTION ---
elif section == "I Section":
    st.header("I Section")
    c1, c2, c3 = st.columns(3)
    with c1:
        Fb1 = st.number_input("Bottom flange width mm", value=None, placeholder="Empty", key="I_Fb1")
        Fh1 = st.number_input("Bottom flange depth mm", value=None, placeholder="Empty", key="I_Fh1")
    with c2:
        Fb2 = st.number_input("Top flange width mm", value=None, placeholder="Empty", key="I_Fb2")
        Fh2 = st.number_input("Top flange depth mm", value=None, placeholder="Empty", key="I_Fh2")
    with c3:
        Wb = st.number_input("Web width mm", value=None, placeholder="Empty", key="I_Wb")
        Wh = st.number_input("Web depth mm", value=None, placeholder="Empty", key="I_Wh")
    
    if None not in (Fb1, Fh1, Fb2, Fh2, Wb, Wh):
        Af1=Fb1*Fh1; Af2=Fb2*Fh2; Aw=Wb*Wh
        yf1=Fh1/2; yw=Fh1+(Wh/2); yf2=Fh1+Wh+(Fh2/2)
        yNA=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Aw+Af2)
        I=((Fb1*Fh1**3)/12)+(Af1*(yNA-yf1)**2)+((Fb2*Fh2**3)/12)+(Af2*(yNA-yf2)**2)+((Wb*Wh**3)/12)+(Aw*(yNA-yw)**2)
        H=Fh1+Fh2+Wh; y_max=max(yNA, H-yNA); sigma=(M*y_max)/I
        st.success(f"yNA={yNA:.2f} mm, I={I:.2f} mm⁴, Sigma={sigma:.2f} N/mm²")
        st.pyplot(plot_stress(H, yNA, y_max, I, M, beam_type))

# --- L SECTION ---
elif section == "L Section":
    st.header("L Section")
    c1, c2 = st.columns(2)
    with c1:
        Fb = st.number_input("Flange width mm", value=None, placeholder="Empty", key="L_Fb")
        Fh = st.number_input("Flange depth mm", value=None, placeholder="Empty", key="L_Fh")
    with c2:
        Wb = st.number_input("Web width mm", value=None, placeholder="Empty", key="L_Wb")
        Wh = st.number_input("Web depth mm", value=None, placeholder="Empty", key="L_Wh")
    
    if None not in (Fb, Fh, Wb, Wh):
        Af=Fb*Fh; Aw=Wb*Wh
        yf=Fh/2; yw=Fh+(Wh)/2
        yNA=((Af*yf)+(Aw*yw))/(Af+Aw)
        I=((Fb*Fh**3)/12)+(Af*(yNA-yf)**2)+((Wb*Wh**3)/12)+(Aw*(yNA-yw)**2)
        H=Fh+Wh; y_max=max(yNA, H-yNA); sigma=(M*y_max)/I
        st.success(f"yNA={yNA:.2f}, I={I:.2f}, Sigma={sigma:.2f}")
        st.pyplot(plot_stress(H, yNA, y_max, I, M, beam_type))

# --- C SECTION ---
elif section == "C Section":
    st.header("C Section")
    c1, c2, c3 = st.columns(3)
    with c1:
        Fb1 = st.number_input("Bottom flange width mm", value=None, placeholder="Empty", key="C_Fb1")
        Fh1 = st.number_input("Bottom flange depth mm", value=None, placeholder="Empty", key="C_Fh1")
    with c2:
        Fb2 = st.number_input("Top flange width mm", value=None, placeholder="Empty", key="C_Fb2")
        Fh2 = st.number_input("Top flange depth mm", value=None, placeholder="Empty", key="C_Fh2")
    with c3:
        Wb = st.number_input("Web width mm", value=None, placeholder="Empty", key="C_Wb")
        Wh = st.number_input("Web depth mm", value=None, placeholder="Empty", key="C_Wh")

    if None not in (Fb1, Fh1, Fb2, Fh2, Wb, Wh):
        Af1=Fb1*Fh1; Af2=Fb2*Fh2; Aw=Wb*Wh
        yf1=Fh1/2; yw=Fh1+(Wh/2); yf2=Fh1+Wh+(Fh2/2)
        yNA=((Af1*yf1)+(Af2*yf2)+(Aw*yw))/(Af1+Aw+Af2)
        I=((Fb1*Fh1**3)/12)+(Af1*(yNA-yf1)**2)+((Fb2*Fh2**3)/12)+(Af2*(yNA-yf2)**2)+((Wb*Wh**3)/12)+(Aw*(yNA-yw)**2)
        H=Fh1+Fh2+Wh; y_max=max(yNA, H-yNA); sigma=(M*y_max)/I
        st.success(f"yNA={yNA:.2f}, I={I:.2f}, Sigma={sigma:.2f}")
        st.pyplot(plot_stress(H, yNA, y_max, I, M, beam_type))