class FeedbackPopupManager {
    constructor() {
        this.modalCreated = false;
        this.checkInterval = 300000; // 5 minutes
        this.init();
        console.log('FeedbackPopupManager initialized');
    }
 
    async init() {
        const path = window.location.pathname;
        if (path === '/' || path === '/menu') {
            console.log('Initializing feedback popup on:', path);
            
            // Check if we've already shown a popup today
            if (this.hasShownTodayPopup()) {
                console.log('Already shown popup today, skipping');
                return;
            }
 
            // Initial check with delay
            setTimeout(async () => {
                await this.checkForFeedback();
            }, 1500);
        }
    }
 
    hasShownTodayPopup() {
        const lastPopup = localStorage.getItem('lastFeedbackPopup');
        if (!lastPopup) return false;
 
        const lastDate = new Date(lastPopup);
        const today = new Date();
        return lastDate.toDateString() === today.toDateString();
    }
 
    async checkForFeedback() {
        try {
            console.log('Checking for active feedback questions...');
            
            // Skip if modal already exists
            if (document.getElementById('feedbackModal')) {
                console.log('Modal already exists, skipping check');
                return;
            }
 
            const response = await fetch('/api/active-feedback-questions');
            const data = await response.json();
            console.log('Feedback API response:', data);
 
            if (data.status === 'success' && data.question) {
                console.log('Found active question:', data.question);
                this.createAndShowModal(data.question);
                // Store the timestamp when we show a popup
                localStorage.setItem('lastFeedbackPopup', new Date().toISOString());
            }
        } catch (error) {
            console.error('Error checking for feedback:', error);
        }
    }
 
    getAnswerInput(question) {
        switch (question.type) {
            case 'yes-no':
                return `
                    <div class="btn-group w-100" role="group">
                        <input type="radio" class="btn-check feedback-autosubmit" name="response" 
                            value="yes" id="responseYes">
                        <label class="btn btn-outline-success" for="responseYes">Yes</label>
                        <input type="radio" class="btn-check feedback-autosubmit" name="response" 
                            value="no" id="responseNo">
                        <label class="btn btn-outline-danger" for="responseNo">No</label>
                    </div>`;
 
            case 'rating':
                return `
                    <div class="rating-group d-flex justify-content-between">
                        ${[1, 2, 3, 4, 5].map(num => `
                            <div class="text-center">
                                <input type="radio" class="btn-check feedback-autosubmit" name="response" 
                                    value="${num}" id="rating${num}">
                                <label class="btn btn-outline-primary px-3" for="rating${num}">${num}</label>
                            </div>
                        `).join('')}
                    </div>`;
 
            case 'text':
                return `
                    <div>
                        <textarea class="form-control mb-3" name="response" rows="3" 
                            placeholder="Please share your thoughts..."></textarea>
                        <button type="button" class="btn btn-primary w-100" 
                            onclick="feedbackPopup.submitFeedback()">Submit</button>
                    </div>`;
 
            default:
                return '<p class="text-danger">Unsupported question type</p>';
        }
    }
 
    createAndShowModal(question) {
        try {
            const existingModal = document.getElementById('feedbackModal');
            if (existingModal) {
                existingModal.remove();
            }
 
            const modalHtml = `
                <div class="modal fade" id="feedbackModal" tabindex="-1" aria-labelledby="feedbackModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="feedbackModalLabel">Quick Feedback</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p class="question-text mb-4">${question.text}</p>
                                <div class="answer-container" data-type="${question.type}" data-question-id="${question.id}">
                                    ${this.getAnswerInput(question)}
                                </div>
                            </div>
                            ${question.type === 'text' ? '' : 
                                `<div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                </div>`
                            }
                        </div>
                    </div>
                </div>`;
 
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            console.log('Modal HTML inserted into DOM');
 
            const modalElement = document.getElementById('feedbackModal');
            if (!modalElement) {
                throw new Error('Modal element not found after insertion');
            }
 
            // Add event listeners for auto-submit
            modalElement.querySelectorAll('.feedback-autosubmit').forEach(input => {
                input.addEventListener('change', () => {
                    this.submitFeedback();
                });
            });
 
            const modal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: false
            });
            modal.show();
 
            modalElement.addEventListener('hidden.bs.modal', function () {
                this.remove();
            });
 
        } catch (error) {
            console.error('Error creating/showing modal:', error);
        }
    }
 
    async submitFeedback() {
        const modal = document.getElementById('feedbackModal');
        const answerContainer = modal.querySelector('.answer-container');
        const questionId = answerContainer.dataset.questionId;
        const type = answerContainer.dataset.type;
 
        let response;
        if (type === 'text') {
            response = modal.querySelector('textarea[name="response"]').value.trim();
        } else {
            response = modal.querySelector('input[name="response"]:checked')?.value;
        }
 
        if (!response) {
            if (type === 'text') {
                alert('Please provide an answer');
            }
            return;
        }
 
        try {
            const result = await fetch('/api/submit-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question_id: questionId,
                    response: response
                })
            });
 
            const data = await result.json();
            
            if (data.status === 'success') {
                bootstrap.Modal.getInstance(modal).hide();
                this.showToast('Thank you!', 'Your feedback helps us improve.');
                // Store that we've submitted feedback today
                localStorage.setItem('lastFeedbackPopup', new Date().toISOString());
            } else {
                throw new Error(data.message || 'Failed to submit feedback');
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
            this.showToast('Error', error.message || 'Failed to submit feedback', 'danger');
        }
    }
 
    showToast(title, message, type = 'success') {
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${title}</strong><br>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>`;
 
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
 
        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHtml;
        const toast = toastElement.firstChild;
        container.appendChild(toast);
 
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 5000
        });
        bsToast.show();
 
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }
 }
 
 // Initialize feedback popup manager
 let feedbackPopup;
 document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded - creating feedback popup manager');
    feedbackPopup = new FeedbackPopupManager();
 });