// ============================================================================
// MANUFACTURING SUPPORT ASSISTANT - JAVASCRIPT
// ============================================================================

// API Configuration
const API_BASE_URL = 'http://localhost:8002';

// DOM Elements - Get references to HTML elements we'll interact with
const chatContainer = document.getElementById('chatContainer');
const queryInput = document.getElementById('queryInput');
const sendButton = document.getElementById('sendButton');
const buttonText = sendButton.querySelector('.button-text');
const loadingSpinner = sendButton.querySelector('.loading-spinner');
const caseIdInput = document.getElementById('caseId');
const agentIdInput = document.getElementById('agentId');

// Store current response ID for feedback
let currentResponseId = null;

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// When page loads, set up event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Send button click handler
    sendButton.addEventListener('click', handleSendQuery);
    
    // Enter key handler for textarea (Shift+Enter for new line, Enter to send)
    queryInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent new line
            handleSendQuery();
        }
    });
    
    // Auto-resize textarea as user types
    queryInput.addEventListener('input', autoResizeTextarea);
    
    initializeAnalytics();
});

// ============================================================================
// MAIN QUERY HANDLING FUNCTION
// ============================================================================

/**
 * Handles sending a query to the backend API
 * This is the main function that orchestrates the entire chat flow
 */
async function handleSendQuery() {
    const query = queryInput.value.trim();
    const caseId = caseIdInput.value.trim();
    const agentId = agentIdInput.value.trim();
    
    // Validation - check required fields
    if (!query) {
        showError('Please enter a question or describe your issue.');
        return;
    }
    
    if (!caseId) {
        showError('Please enter a Case ID.');
        return;
    }
    
    if (!agentId) {
        showError('Please enter an Agent ID.');
        return;
    }
    
    try {
        // Step 1: Show user message in chat
        addUserMessage(query);
        
        // Step 2: Clear input and show loading state
        queryInput.value = '';
        setLoadingState(true);
        
        // Step 3: Call the API (this is where the magic happens!)
        const response = await callManufacturingAPI(query, caseId, agentId);
        
        // Step 4: Display the response
        addBotMessage(response);
        
    } catch (error) {
        // Step 5: Handle any errors gracefully
        console.error('Error processing query:', error);
        addErrorMessage('Sorry, I encountered an error. Please try again.');
    } finally {
        // Step 6: Always reset loading state
        setLoadingState(false);
        queryInput.focus(); // Return focus to input
    }
}

// ============================================================================
// API COMMUNICATION
// ============================================================================

/**
 * Makes the actual API call to your FastAPI backend
 * 
 * KEY CONCEPTS EXPLAINED:
 * - async/await: Modern way to handle asynchronous operations
 * - fetch(): Browser API for making HTTP requests
 * - JSON: Data format for API communication
 */
async function callManufacturingAPI(query, caseId, agentId) {
    // The fetch() function returns a Promise
    // await waits for the Promise to resolve before continuing
    const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // Convert JavaScript object to JSON string
        body: JSON.stringify({ 
            query: query,
            case_id: caseId,
            agent_id: agentId
        })
    });
    
    // Check if the request was successful
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // Convert JSON response back to JavaScript object
    const data = await response.json();
    return data;
}

// ============================================================================
// UI MANIPULATION FUNCTIONS
// ============================================================================

/**
 * Adds a user message to the chat
 * DOM MANIPULATION: Creating and inserting HTML elements dynamically
 */
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Adds a bot response to the chat
 * Handles both simple text and structured responses with citations
 */
function addBotMessage(response) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    // Generate unique response ID if not provided
    const responseId = response.response_id || `response_${Date.now()}`;
    currentResponseId = responseId;
    
    // Build the message content
    let content = `<div class="message-content">`;
    
    // Main response text
    if (response.response) {
        content += `<p>${escapeHtml(response.response)}</p>`;
    }
    
    // Add troubleshooting steps if available
    if (response.steps && response.steps.length > 0) {
        content += `
            <div class="troubleshooting-steps">
                <h4>🔧 Troubleshooting Steps</h4>
                <ol>
                    ${response.steps.map(step => `<li>${escapeHtml(step)}</li>`).join('')}
                </ol>
            </div>
        `;
    }
    
    // Add confidence indicator
    if (response.confidence) {
        const confidencePercent = typeof response.confidence === 'number' ? response.confidence : Math.round(response.confidence * 100);
        content += `
            <div class="confidence-indicator">
                <span class="confidence-label">Confidence:</span>
                <span class="confidence-value">${confidencePercent}%</span>
            </div>
        `;
    }
    
    // Add disclaimers if available
    if (response.disclaimers && response.disclaimers.length > 0) {
        content += `
            <div class="disclaimers">
                <h4>⚠️ Important Notes</h4>
                <ul>
                    ${response.disclaimers.map(disclaimer => `<li>${escapeHtml(disclaimer)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Add citations if they exist
    if (response.sources && response.sources.length > 0) {
        content += `
            <div class="citations">
                <h4>📚 Sources</h4>
                ${response.sources.map(source => `
                    <div class="citation">
                        <div class="citation-source">${escapeHtml(source.document || 'Technical Document')}</div>
                        <div>${escapeHtml(source.content || source.text || '')}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // Add feedback buttons
    content += `
        <div class="feedback-container">
            <span class="feedback-label">Was this helpful?</span>
            <button class="feedback-button" onclick="submitFeedback('${responseId}', 'like')">
                👍 <span>Yes</span>
            </button>
            <button class="feedback-button" onclick="submitFeedback('${responseId}', 'dislike')">
                👎 <span>No</span>
            </button>
        </div>
    `;
    
    content += `</div>`;
    messageDiv.innerHTML = content;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Shows an error message in the chat
 */
function addErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="error-message">
                ⚠️ ${escapeHtml(message)}
            </div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Shows a temporary error message at the top
 */
function showError(message) {
    // Remove any existing error
    const existingError = document.querySelector('.temp-error');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message temp-error';
    errorDiv.textContent = message;
    
    chatContainer.insertBefore(errorDiv, chatContainer.firstChild);
    
    // Remove error after 3 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// ============================================================================
// UI HELPER FUNCTIONS
// ============================================================================

/**
 * Controls the loading state of the send button
 * CONCEPT: UI State Management - showing user that something is happening
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        sendButton.disabled = true;
        buttonText.style.display = 'none';
        loadingSpinner.style.display = 'inline';
    } else {
        sendButton.disabled = false;
        buttonText.style.display = 'inline';
        loadingSpinner.style.display = 'none';
    }
}

/**
 * Auto-scrolls chat to show latest message
 */
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Auto-resizes textarea based on content
 */
function autoResizeTextarea() {
    queryInput.style.height = 'auto';
    queryInput.style.height = Math.min(queryInput.scrollHeight, 120) + 'px';
}

/**
 * Escapes HTML to prevent XSS attacks
 * SECURITY: Always escape user input before displaying it
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Submits feedback to the backend API
 */
async function submitFeedback(responseId, feedbackType) {
    const caseId = caseIdInput.value.trim();
    const agentId = agentIdInput.value.trim();
    
    try {
        const response = await fetch(`${API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                response_id: responseId,
                case_id: caseId,
                agent_id: agentId,
                feedback_type: feedbackType
            })
        });
        
        if (response.ok) {
            // Update button states to show feedback was submitted
            const feedbackButtons = document.querySelectorAll(`[onclick*="${responseId}"]`);
            feedbackButtons.forEach(button => {
                button.disabled = true;
                if (button.onclick.toString().includes(feedbackType)) {
                    button.classList.add(`active-${feedbackType}`);
                }
            });
            
            console.log(`✅ Feedback submitted: ${feedbackType} for response ${responseId}`);
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
}

// ============================================================================
// ANALYTICS PANEL FUNCTIONALITY
// ============================================================================

let analyticsPanel = null;
let analyticsToggle = null;
let closeAnalytics = null;

/**
 * Initialize analytics panel event listeners
 */
function initializeAnalytics() {
    analyticsPanel = document.getElementById('analyticsPanel');
    analyticsToggle = document.getElementById('analyticsToggle');
    closeAnalytics = document.getElementById('closeAnalytics');
    
    if (analyticsToggle) {
        analyticsToggle.addEventListener('click', toggleAnalyticsPanel);
    }
    
    if (closeAnalytics) {
        closeAnalytics.addEventListener('click', closeAnalyticsPanel);
    }
}

/**
 * Toggle analytics panel visibility
 */
function toggleAnalyticsPanel() {
    if (analyticsPanel) {
        analyticsPanel.classList.toggle('open');
        if (analyticsPanel.classList.contains('open')) {
            fetchAnalytics();
        }
    }
}

/**
 * Close analytics panel
 */
function closeAnalyticsPanel() {
    if (analyticsPanel) {
        analyticsPanel.classList.remove('open');
    }
}

/**
 * Fetch analytics data from the backend
 */
async function fetchAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/performance`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const analyticsData = await response.json();
            displayAnalytics(analyticsData);
        } else {
            console.error('Failed to fetch analytics:', response.statusText);
            displayAnalyticsError();
        }
    } catch (error) {
        console.error('Error fetching analytics:', error);
        displayAnalyticsError();
    }
}

/**
 * Display analytics data in the panel
 */
function displayAnalytics(data) {
    // Update metric cards
    const satisfactionRate = document.getElementById('satisfactionRate');
    const totalResponses = document.getElementById('totalResponses');
    const helpfulResponses = document.getElementById('helpfulResponses');
    
    if (satisfactionRate) {
        satisfactionRate.textContent = `${data.satisfaction_rate}%`;
    }
    
    if (totalResponses) {
        totalResponses.textContent = data.total_responses;
    }
    
    if (helpfulResponses) {
        helpfulResponses.textContent = data.helpful_responses;
    }
    
    // Update recent feedback list
    displayRecentFeedback(data.recent_feedback);
}

/**
 * Display recent feedback in the panel
 */
function displayRecentFeedback(feedbackList) {
    const feedbackContainer = document.getElementById('recentFeedbackList');
    
    if (!feedbackContainer) return;
    
    if (!feedbackList || feedbackList.length === 0) {
        feedbackContainer.innerHTML = '<div class="no-feedback">No positive feedback available yet</div>';
        return;
    }
    
    const feedbackHTML = feedbackList.map(feedback => `
        <div class="feedback-item">
            <div class="feedback-meta">
                <span class="feedback-case">Case: ${escapeHtml(feedback.case_id)}</span>
                <span class="feedback-agent">Agent: ${escapeHtml(feedback.agent_id)}</span>
            </div>
            <div class="feedback-comment">
                ${escapeHtml(feedback.comment || 'Positive feedback received')}
            </div>
        </div>
    `).join('');
    
    feedbackContainer.innerHTML = feedbackHTML;
}

/**
 * Display error message when analytics fetch fails
 */
function displayAnalyticsError() {
    const satisfactionRate = document.getElementById('satisfactionRate');
    const totalResponses = document.getElementById('totalResponses');
    const helpfulResponses = document.getElementById('helpfulResponses');
    
    if (satisfactionRate) satisfactionRate.textContent = 'Error';
    if (totalResponses) totalResponses.textContent = 'Error';
    if (helpfulResponses) helpfulResponses.textContent = 'Error';
    
    const feedbackContainer = document.getElementById('recentFeedbackList');
    if (feedbackContainer) {
        feedbackContainer.innerHTML = '<div class="no-feedback">Unable to load feedback data</div>';
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

// Focus on input when page loads
window.addEventListener('load', function() {
    queryInput.focus();
});
