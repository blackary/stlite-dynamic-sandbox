function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  const {code, requirements, height} = event.detail.args

  if (!window.controller) {
    window.controller = stlite.mount({
        requirements: requirements || [],
        entrypoint: "streamlit_app.py",
        files: {
          "streamlit_app.py": code || "",
        }
    }, document.getElementById("root"))

    window.lastCode = code;
  }

  debugger;


  if (window.lastCode !== code) {
    window.controller.writeFile("streamlit_app.py", code || "");
    window.lastCode = code;
  }
  Streamlit.setFrameHeight(height || 100);
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100)
