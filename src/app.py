import streamlit as st
import time
from embedder import Embedder
from search_engine import SearchEngine

# 1. Page Configuration: Sets the browser tab title and layout
st.set_page_config(
    page_title="Doc Search Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# 2. Session State: To hold the query input
if 'query_input' not in st.session_state:
    st.session_state.query_input = ""

def set_query(text):
    """Callback to update the search box when an example is clicked"""
    st.session_state.query_input = text

# 3. Sidebar: Controls
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=50)
    st.header("Search Settings")
    
    # Let user pick how many results they want
    top_k = st.slider("Number of Results", min_value=1, max_value=10, value=3)
    
    st.divider()
    # Example Queries
    st.subheader("💡 Try an Example")
    st.caption("Click to quick-search:")
    
    st.markdown("**🪐 Sci.Space**")
    if st.button("🚀 Space Missions"):
        set_query("space shuttle launch orbit failure")
    if st.button("🌌 Astronomy"):
        set_query("hubble telescope deep field galaxy")
    if st.button("🌑 Moon Landing"):
        set_query("apollo lunar module dust")

    st.markdown("**🖥️ Comp.Graphics**")
    if st.button("🧊 3D Rendering"):
        set_query("ray tracing polygon shading algorithms")
    if st.button("🎨 Image Formats"):
        set_query("jpeg compression vs tiff quality")
    if st.button("🎮 Virtual Reality"):
        set_query("virtual reality head mounted display optics")

    st.divider()
    status_placeholder = st.empty()

# 4. Load Engine (Cached so it doesn't reload on every click)
@st.cache_resource
def load_engine():
    # Shows a spinner while loading
    with st.spinner('Loading 20 Newsgroups Dataset & AI Models...'):
        embedder = Embedder()
        engine = SearchEngine()
        doc_ids, embeddings, metadata = embedder.process_documents()
        engine.build_index(doc_ids, embeddings, metadata)
    return embedder, engine

# Initialize
try:
    embedder, engine = load_engine()
    status_placeholder.success("✅ System Ready")
except Exception as e:
    status_placeholder.error("❌ Error Loading System")
    st.error(f"Failed to load: {e}")
    st.stop()

# 5. Main Interface
st.title("🔍 Multi-document Embedding Search Engine with Caching")
st.markdown("##### Semantic Search over Documents")

# Search Bar (Connected to Session State)
col1, col2 = st.columns([4, 1])
with col1:
    # key='query_input' binds this widget to st.session_state.query_input
    query = st.text_input(
        "Enter your search query...", 
        placeholder="Type here or select an example from the sidebar...",
        key="query_input"
    )
with col2:
    st.write("") 
    st.write("") 
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# 6. Search Logic
if search_button or query:
    if not query:
        st.warning("Please enter a query first.")
    else:
        start_time = time.time()
        
        query_vec = embedder.embed_query(query)
        results = engine.search(query, query_vec, top_k=top_k)
        
        end_time = time.time()
        
        st.write(f"Found {len(results)} results for **'{query}'** in **{end_time - start_time:.4f} seconds**")
        st.divider()

        for i, res in enumerate(results):
            with st.container():
                c1, c2 = st.columns([1, 5])
                with c1:
                    st.metric(label="Relevance", value=f"{res['score']:.1%}")
                    st.caption(f"`{res['doc_id']}`")
                with c2:
                    st.subheader(f"Result #{i+1}")
                    st.markdown(f"**Insight:** {res['explanation']['why_this']}")
                    with st.expander("📄 View Document Excerpt", expanded=True):
                        st.info(res['preview'])
                st.divider()