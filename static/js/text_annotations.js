// static/js/text_annotations.js
document.addEventListener("DOMContentLoaded", function () {
  // Add styles for annotated text
  const highlightStyle = document.createElement("style");
  highlightStyle.textContent = `
        .trix-content .annotated-text {
            background-color: #fff3cd;
            border-bottom: 2px solid #ffc107;
            padding: 2px 0;
            border-radius: 2px;
            cursor: help;
            position: relative;
        }

        .trix-content .annotated-text:hover::after {
            content: attr(data-annotation);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #333;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 14px;
            white-space: nowrap;
            z-index: 1000;
            margin-bottom: 4px;
        }

        .trix-content .annotated-text:hover::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: #333;
            margin-bottom: -2px;
        }
    `;
  document.head.appendChild(highlightStyle);

  // First add the styles to document head
  const modalStyle = document.createElement("style");
  modalStyle.textContent = `
        .annotation-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        }
        
        .annotation-modal-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 400px;
            max-width: 90%;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .annotation-modal h3 {
            margin: 0 0 15px 0;
            font-size: 18px;
        }
        
        .annotation-modal textarea {
            width: 100%;
            min-height: 100px;
            margin: 10px 0;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
        }
        
        .annotation-modal select {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .annotation-modal-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 15px;
        }
        
        .annotation-modal button {
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            border: none;
            font-size: 14px;
        }
        
        .annotation-modal .btn-save {
            background: #007bff;
            color: white;
        }
        
        .annotation-modal .btn-cancel {
            background: #6c757d;
            color: white;
        }
        
        .selected-text-preview {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
            border: 1px solid #dee2e6;
        }
    `;
  document.head.appendChild(modalStyle);

  const trixEditor = document.querySelector("trix-editor");
  if (!trixEditor) {
    console.log("No trix editor found");
    return;
  }

  // Add annotation button to toolbar
  const toolbar = document.querySelector("trix-toolbar .trix-button-row");
  if (!toolbar) {
    console.log("No toolbar found");
    return;
  }

  const annotationGroup = document.createElement("span");
  annotationGroup.className = "trix-button-group";
  annotationGroup.setAttribute("data-trix-button-group", "annotation-tools");

  const annotateButton = document.createElement("button");
  annotateButton.type = "button";
  annotateButton.className =
    "trix-button trix-button--icon trix-button--icon-note";
  annotateButton.setAttribute("data-trix-action", "addAnnotation");
  annotateButton.title = "Add Note";

  // Add note icon styles
  const iconStyle = document.createElement("style");
  iconStyle.textContent = `
        .trix-button--icon-note::before {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>');
        }
    `;
  document.head.appendChild(iconStyle);

  annotationGroup.appendChild(annotateButton);
  toolbar.appendChild(annotationGroup);

  // Function to get stanza ID (keeping existing implementation)
  function getStanzaId() {
    const urlMatch = window.location.pathname.match(/\/stanza\/(\d+)\//);
    if (urlMatch) return urlMatch[1];

    const form = document.querySelector("#stanza_form");
    if (form) {
      const objectId =
        form.getAttribute("data-object-id") ||
        form.querySelector('input[name="object_id"]')?.value;
      if (objectId) return objectId;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const objectId = urlParams.get("object_id");
    if (objectId) return objectId;

    const breadcrumbs = document.querySelector(".breadcrumbs");
    if (breadcrumbs) {
      const match = breadcrumbs.textContent.match(/Stanza\s+(\d+)/);
      if (match) return match[1];
    }

    const hiddenId = document.querySelector(
      'input[name="stanza_id"], input[name="id"]',
    )?.value;
    if (hiddenId) return hiddenId;

    console.error("Could not find stanza ID. URL:", window.location.href);
    return null;
  }

  // Handle annotation button click
  annotateButton.addEventListener("click", function (event) {
    console.log("Annotation button clicked");
    event.preventDefault();

    const editor = trixEditor.editor;
    const selectedRange = editor.getSelectedRange();

    if (selectedRange[0] === selectedRange[1]) {
      alert("Please select some text to annotate");
      return;
    }

    const selectedText = editor.getDocument().getStringAtRange(selectedRange);
    console.log("Selected text:", selectedText);

    const stanzaId = getStanzaId();
    console.log("Stanza ID:", stanzaId);

    console.log("Selection details:", {
      text: selectedText,
      range: selectedRange,
      fullText: editor.getDocument().toString(),
      start: selectedRange[0],
      end: selectedRange[1],
    });

    if (!stanzaId) {
      alert("Could not determine which stanza to annotate");
      return;
    }

    // Create and append modal
    const modal = document.createElement("div");
    modal.className = "annotation-modal";
    modal.innerHTML = `
            <div class="annotation-modal-content">
                <h3>Add Annotation</h3>
                <div class="selected-text-preview">
                    Selected text: <strong>${selectedText}</strong>
                </div>
                <textarea id="annotation-text" 
                    placeholder="Enter your annotation..."
                    autofocus></textarea>
                <select id="annotation-type">
                    <option value="note">Editorial Note</option>
                    <option value="translation">Translation</option>
                    <option value="variant">Textual Variant</option>
                    <option value="reference">Cross Reference</option>
                </select>
                <div class="annotation-modal-buttons">
                    <button type="button" class="btn-cancel">Cancel</button>
                    <button type="button" class="btn-save">Save</button>
                </div>
            </div>
        `;

    document.body.appendChild(modal);
    console.log("Modal created and appended");

    // Focus the textarea
    setTimeout(() => {
      const textarea = modal.querySelector("#annotation-text");
      if (textarea) {
        textarea.focus();
      }
    }, 100);

    // Handle modal buttons
    modal.querySelector(".btn-cancel").addEventListener("click", () => {
      console.log("Cancel clicked");
      modal.remove();
    });

    modal.querySelector(".btn-save").addEventListener("click", () => {
      console.log("Save clicked");
      const annotationText = modal.querySelector("#annotation-text").value;
      const annotationType = modal.querySelector("#annotation-type").value;

      if (!annotationText.trim()) {
        alert("Please enter an annotation");
        return;
      }

      // Get CSRF token
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
      )?.value;
      if (!csrfToken) {
        console.error("No CSRF token found");
        alert("Security token missing");
        return;
      }

      // Prepare the data
      const formData = new FormData();
      formData.append("stanza_id", stanzaId);
      formData.append("selected_text", selectedText);
      formData.append("annotation", annotationText);
      formData.append("annotation_type", annotationType);
      formData.append("from_pos", selectedRange[0]);
      formData.append("to_pos", selectedRange[1]);
      formData.append("csrfmiddlewaretoken", csrfToken);

      // Log what we're sending
      console.log("Sending annotation data:", {
        stanza_id: stanzaId,
        selected_text: selectedText,
        annotation: annotationText,
        annotation_type: annotationType,
        from_pos: selectedRange[0],
        to_pos: selectedRange[1],
      });

      // Add loading state to save button
      const saveButton = modal.querySelector(".btn-save");
      const originalButtonText = saveButton.textContent;
      saveButton.textContent = "Saving...";
      saveButton.disabled = true;

      fetch("/text-annotations/create/", {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
        credentials: "same-origin", // Important for CSRF
      })
        .then((response) => {
          console.log("Response status:", response.status);
          return response
            .json()
            .then((data) => ({ status: response.status, data }));
        })
        .then(({ status, data }) => {
          console.log("Server response:", status, data);
          if (status === 200 && data.success) {
            // Create the annotated span with proper attributes and styling
            editor.setSelectedRange(selectedRange);
            const annotatedSpan = `
                <span 
                    class="annotated-text" 
                    data-annotation-id="${data.annotation_id}" 
                    data-annotation="${annotationText}"
                    data-annotation-type="${annotationType}"
                >${selectedText}</span>
            `;
            editor.insertHTML(annotatedSpan);

            // Close the modal
            modal.remove();

            // Show success message
            const successMessage = document.createElement("div");
            successMessage.className = "annotation-success-message";
            successMessage.textContent = "Annotation saved successfully";
            successMessage.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #28a745;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                z-index: 10000;
            `;
            document.body.appendChild(successMessage);
            setTimeout(() => successMessage.remove(), 3000);

            // Add hover listener for the newly created annotation
            const newAnnotation = editor.element.querySelector(
              `[data-annotation-id="${data.annotation_id}"]`,
            );
            if (newAnnotation) {
              newAnnotation.addEventListener("mouseenter", function (e) {
                const tooltip = document.createElement("div");
                tooltip.className = "annotation-tooltip";
                tooltip.innerHTML = `
                        <strong>${annotationType}:</strong><br>
                        ${annotationText}
                    `;
                tooltip.style.cssText = `
                        position: absolute;
                        background: #333;
                        color: white;
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-size: 14px;
                        z-index: 1000;
                        max-width: 300px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    `;

                const rect = newAnnotation.getBoundingClientRect();
                tooltip.style.left = `${rect.left}px`;
                tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;

                document.body.appendChild(tooltip);

                newAnnotation.addEventListener(
                  "mouseleave",
                  function () {
                    tooltip.remove();
                  },
                  { once: true },
                );
              });
            }
          } else {
            throw new Error(data.error || "Failed to save annotation");
          }
        });
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Function to load existing annotations
  function loadExistingAnnotations() {
    const stanzaId = getStanzaId();
    if (!stanzaId) return;

    fetch(`/text-annotations/get/${stanzaId}/`)
      .then((response) => response.json())
      .then((annotations) => {
        annotations.forEach((annotation) => {
          // Find the text node containing this annotation
          const editor = document.querySelector("trix-editor").editor;
          const content = editor.getDocument().toString();
          const index = content.indexOf(annotation.selected_text);

          if (index !== -1) {
            const range = [index, index + annotation.selected_text.length];
            editor.setSelectedRange(range);
            const annotatedSpan = `
                            <span 
                                class="annotated-text" 
                                data-annotation-id="${annotation.id}" 
                                data-annotation="${annotation.annotation}"
                                data-annotation-type="${annotation.annotation_type}"
                            >${annotation.selected_text}</span>
                        `;
            editor.insertHTML(annotatedSpan);
          }
        });
      })
      .catch((error) => console.error("Error loading annotations:", error));
  }

  // Call this after the editor is initialized
  loadExistingAnnotations();
});

document.addEventListener("DOMContentLoaded", function () {
  // Add styles for annotations
  const style = document.createElement("style");
  style.textContent = `
        .annotated-text {
            background-color: #fff3cd;
            border-bottom: 2px solid #ffc107;
            cursor: help;
        }

        #sidebar {
            transition: transform 0.3s ease-in-out;
        }

        #sidebar.active {
            transform: translateX(0) !important;
        }
        
        .annotation-loading {
            padding: 1rem;
            color: #666;
            font-style: italic;
        }
    `;
  document.head.appendChild(style);

  // Function to show annotation
  window.showAnnotation = function (event, element) {
    event.preventDefault();
    const sidebar = document.getElementById("sidebar");
    const annotationId = element.getAttribute("data-annotation-id");

    // Show loading state
    sidebar.classList.add("active");
    document.getElementById("notation-text").innerHTML =
      '<div class="annotation-loading">Loading annotation...</div>';

    // Fetch annotation data
    fetch(`/text-annotations/annotation/${annotationId}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        // Update sidebar content
        document.getElementById("notation-text").innerHTML = `
                    <div class="annotation-content">
                        <div class="annotation-type text-sm text-gray-600 mb-2">
                            ${data.annotation_type}
                        </div>
                        <div class="annotation-text">
                            ${data.annotation}
                        </div>
                    </div>
                `;
      })
      .catch((error) => {
        console.error("Error loading annotation:", error);
        document.getElementById("notation-text").innerHTML = `
                    <div class="error-message text-red-500">
                        Failed to load annotation. Please try again.
                    </div>
                `;
      });
  };

  // Close sidebar when clicking close button
  const closeButton = document.getElementById("close-button");
  if (closeButton) {
    closeButton.addEventListener("click", function () {
      document.getElementById("sidebar").classList.remove("active");
    });
  }

  // Close sidebar when clicking outside
  document.addEventListener("click", function (event) {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    const isClickInside = sidebar.contains(event.target);
    const isAnnotationClick = event.target.closest(".annotated-text");

    if (
      !isClickInside &&
      !isAnnotationClick &&
      sidebar.classList.contains("active")
    ) {
      sidebar.classList.remove("active");
    }
  });
});
