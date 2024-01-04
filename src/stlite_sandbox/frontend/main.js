function sendValue(value) {
  Streamlit.setComponentValue(value)
}

const debounce = (callback, wait) => {
  let timeoutId = null;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      callback.apply(null, args);
    }, wait);
  };
}


/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */

const equals = (a, b) => {
  return JSON.stringify(a) === JSON.stringify(b);
}

const handleError = (e) => {
  sendValue(e.message);
  console.error(e);
}

const clearError = () => {
  sendValue("");
}

function onRender(event) {
  // Only run the render code the first time the component is loaded.
  const {code, requirements, height, scrollable} = event.detail.args

  let searchStr = "?embed=true" + (scrollable ? "" : "&embed_options=disable_scrolling");
  if (window.location.search !== searchStr) {
    window.location.search = searchStr;
  }

  if (!window.controller) {
    window.controller = stlite.mount({
        requirements: requirements || [],
        entrypoint: "streamlit_app.py",
        files: {
          "streamlit_app.py": code || "",
        },
        streamlitConfig: {
          "server.runOnSave": true,
          "client.showErrorDetails": false,
        },
    }, document.getElementById("root"))

    window.controller.disableToast();

    window.lastCode = code;
    window.lastRequirements = requirements;
  }

  // Update logic
  if (!equals(window.lastRequirements, requirements)) {
    window.controller.disableToast();
    window.controller.install(requirements || []).then(() => {
      clearError();
      window.controller.writeFile("streamlit_app.py", code + "\n\n" || "").then(clearError).catch(handleError);
    }).catch(handleError);
    window.lastRequirements = requirements;
  }

  if (window.lastCode !== code) {
    window.controller.disableToast();
    window.controller.writeFile("streamlit_app.py", code || "").then(clearError).catch(handleError);
    window.lastCode = code;
  }

  Streamlit.setFrameHeight(height || 100);
}

const debouncedOnRender = debounce(onRender, 1000);

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, debouncedOnRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100)
