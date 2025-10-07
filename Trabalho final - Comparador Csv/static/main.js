// JavaScript para melhorar a experiência do usuário
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona loading state nos formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
            }
        });
    });

    // Preview de arquivos CSV selecionados
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const parent = input.closest('.mb-3');
            
            // Remove preview anterior
            const existingPreview = parent.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            if (file) {
                const preview = document.createElement('div');
                preview.className = 'file-preview mt-2 p-2 bg-light rounded';
                preview.innerHTML = `
                    <small class="text-muted d-block">
                        <i class="fas fa-file-csv me-1"></i>
                        <strong>Arquivo:</strong> ${file.name}
                    </small>
                    <small class="text-muted d-block">
                        <i class="fas fa-weight me-1"></i>
                        <strong>Tamanho:</strong> ${formatFileSize(file.size)}
                    </small>
                `;
                parent.appendChild(preview);
            }
        });
    });

    // Auto-hide alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Tooltip para botões pequenos
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Confirmar exclusão (se implementado no futuro)
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });

    // Smooth scroll para âncoras
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Função para formatar tamanho de arquivo
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Função para copiar texto para clipboard
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Texto copiado para a área de transferência!', 'success');
        });
    }

    // Sistema de toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove o toast do DOM após ser ocultado
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    // Cria container de toast se não existir
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }

    // Validação de formulário em tempo real
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateInput(this);
            }
        });
    });

    function validateInput(input) {
        const value = input.value.trim();
        const type = input.type;
        let isValid = true;
        let message = '';

        // Validação por tipo
        switch(type) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                isValid = emailRegex.test(value);
                message = 'Digite um email válido';
                break;
            case 'password':
                isValid = value.length >= 6;
                message = 'A senha deve ter pelo menos 6 caracteres';
                break;
            case 'file':
                if (input.hasAttribute('accept')) {
                    const allowedTypes = input.getAttribute('accept').split(',');
                    const file = input.files[0];
                    if (file) {
                        const fileType = '.' + file.name.split('.').pop().toLowerCase();
                        isValid = allowedTypes.includes(fileType);
                        message = 'Tipo de arquivo não permitido';
                    }
                }
                break;
            default:
                if (input.hasAttribute('required')) {
                    isValid = value.length > 0;
                    message = 'Este campo é obrigatório';
                }
        }

        // Atualiza classes e feedback
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            const feedback = input.parentNode.querySelector('.invalid-feedback');
            if (feedback) feedback.remove();
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            
            let feedback = input.parentNode.querySelector('.invalid-feedback');
            if (!feedback) {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                input.parentNode.appendChild(feedback);
            }
            feedback.textContent = message;
        }
    }

    // Função para atualizar contadores em tempo real (se necessário)
    function updateCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-counter'));
            const current = parseInt(counter.textContent);
            if (current < target) {
                counter.textContent = Math.min(current + Math.ceil((target - current) / 10), target);
                setTimeout(updateCounters, 100);
            }
        });
    }

    // Inicializa contadores se existirem
    if (document.querySelector('[data-counter]')) {
        updateCounters();
    }
});