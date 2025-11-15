import { EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { defaultKeymap, history } from "@codemirror/commands";
import { StreamLanguage } from "@codemirror/language";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags } from "@lezer/highlight";
import { linter, lintGutter } from "@codemirror/lint";

const techniqueSelect = document.getElementById('technique-select');
const datasetSelect = document.getElementById('dataset-select');
const promptsContainer = document.getElementById('prompts-container');
const loadPromptsBtn = document.getElementById('load-prompts-btn');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function configCodeMirror(idEditor, text) {
    const variablesRegex = /\{(.*?)\}/g;
    const requiredVariables = Array.from(text.matchAll(variablesRegex), match => match[1]);
    console.log("Required variables:", requiredVariables);

    const customHighlightLanguage = StreamLanguage.define({
        token(stream) {
            // Try to match the entire {text} block at once
            if (stream.match(/\{(.*?)\}/)) {
                return "atom"; // Apply the 'atom' tag
            }

            // If no match, just move to the next character
            stream.next();
            return null; // No tag
        }
    });

    // === Step 2: Define the CSS style for our tag ===
    // We create a style rule that says "anything tagged as 'atom' 
    // should be blue and bold."
    const customHighlightStyle = HighlightStyle.define([
        {
            tag: tags.atom, // The tag we used above
            color: "blue",
            fontWeight: "bold"
        }
    ]);

    const requiredKeywordLinter = (view) => {
        let diagnostics = [];
        const currentText = view.state.doc.toString();

        if (requiredVariables.length > 0) {
            const variables = Array.from(currentText.matchAll(variablesRegex), match => match[1]);
            console.log("Current variables:", variables);
            const errorKeywords = [];
            const hasCorrectSyntax = requiredVariables.every(element => {
                if (variables.includes(element)) {
                    return true;
                }

                errorKeywords.push(element);
                return false;
            });

            if (!hasCorrectSyntax) {
                console.log("Required variables");
                // If the keyword is missing, create a diagnostic.
                errorKeywords.forEach(missingKeyword => {
                    diagnostics.push({
                        from: 0, // Start of the error (beginning of doc)
                        to: view.state.doc.line(1).to, // End of the error (end of first line)
                        severity: "error",
                        message: `Syntax Error: Missing the '{${missingKeyword}}' keyword.`
                    });
                });
            }
        }

        return diagnostics;
    };

    // === Step 3: Bundle all extensions together ===
    const extensions = [
        history(),                // Adds undo/redo support
        keymap.of(defaultKeymap), // Adds basic keybindings (Enter, Tab, etc.)
        customHighlightLanguage,  // Use our custom language
        syntaxHighlighting(customHighlightStyle), // Apply our custom style\
        EditorView.lineWrapping,
        EditorView.updateListener.of((update) => {
            // This function runs for every single update.
            // We check if the document's text actually changed.
            if (update.docChanged) {
                setTimeout(() => {
                    // Get all diagnostic messages from the new state
                    const diagnostics = requiredKeywordLinter(update.view);

                    document.querySelector(`#${idEditor}-status`).classList.add('hidden');
                    if (diagnostics.length > 0) {
                        // We have errors!
                        console.log("Change detected WITH errors:");
                    } else {
                        // No errors found
                        console.log("Change detected, syntax is valid.");


                        const formData = new FormData();
                        formData.append('new_prompt', update.state.doc.toString());
                        formData.append('technique', techniqueSelect.value);
                        formData.append('dataset', datasetSelect.value);
                        formData.append('node', idEditor.replace('-prompt-editor', ''));

                        fetch('/update_prompt/', {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
                            }
                        }).then(response => {
                            return response.json();
                        }).then(data => {
                            console.log('Prompt updated successfully:', data);
                            document.querySelector(`#${idEditor}-status`).classList.remove('hidden');
                        }).catch(error => {
                            console.error('There was a problem with the fetch operation:', error);
                        });
                    }

                }, 500);
            }
        }),
        linter(requiredKeywordLinter), // Run our custom error-checking function
        lintGutter() // Show icons in the gutter
    ];

    // === Step 4: Create the editor ===
    new EditorView({
        state: EditorState.create({
            // This is the starting text
            doc: text,
            // Add all our features
            extensions: extensions
        }),
        // Tell CodeMirror which <div> to attach to
        parent: document.getElementById(idEditor)
    });
}


function capitalizeFirstLetter(str) {
    if (typeof str !== 'string' || str.length === 0) {
        return str; // Handle empty or non-string inputs
    }
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatText(text) {
    // Replace multiple spaces or tabs with a single space
    let formattedText = text.replace(/[ \t]+/g, ' ');

    // Replace multiple newlines with a single newline
    formattedText = formattedText.replace(/\n+/g, '\n');

    // Remove leading/trailing spaces or tabs around newlines
    formattedText = formattedText.replace(/[ \t]*\n[ \t]*/g, '\n');

    // Trim any leading or trailing whitespace from the entire string
    formattedText = formattedText.trim();

    // formattedText = formattedText.replace(
    //     /\{.*?\}/g,
    //     '<span class="text-blue-600">$0</span>'
    // );

    return formattedText;
}

loadPromptsBtn.addEventListener('click', async () => {
    const technique = techniqueSelect.value;
    const dataset = datasetSelect.value;

    if (technique === '' || dataset === '') {
        alert('Por favor, selecione uma técnica e um dataset.');
        return;
    }

    fetch(`/prompts-data/?technique=${technique}&dataset=${dataset}`)
        .then(response => response.json())
        .then(data => {
            const nodes = data.nodes_with_prompts.map(item => {
                const presentationNode = capitalizeFirstLetter(item.node.replaceAll('_', ' '))
                return `
                    <div className="flex justify-between mb-8">
                        <span class="w-[max-content] font-medium text-gray-900 text-lg">${presentationNode}</span>
                        <span id="${item.node}-prompt-editor-status" class="text-green-600 mt-1 hidden"><i class="fa-regular fa-circle-check"></i></span>
                        
                    </div>
                    <div id="${item.node}-prompt-editor" class="w-full border-2 border-gray-200 rounded-md p-2 focus:outline-none text-gray-800 mb-8"></div>
                `;
            });
            promptsContainer.innerHTML = nodes.join('');

            data.nodes_with_prompts.forEach(item => {
                configCodeMirror(`${item.node}-prompt-editor`, formatText(item.prompt));
            });
        });
});