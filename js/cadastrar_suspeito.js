'use strict';

const form = document.querySelector('#suspectForm');
const cpfInput = document.querySelector('#cpf');
const birthInput = document.querySelector('#nascimento');
const message = document.querySelector('#formMessage');

// Impede selecionar uma data de nascimento futura.
if (birthInput) {
  birthInput.max = new Date().toISOString().split('T')[0];
}

// Aplica a máscara 000.000.000-00 enquanto o usuário digita.
cpfInput?.addEventListener('input', (event) => {
  const digits = event.target.value.replace(/\D/g, '').slice(0, 11);
  let formatted = digits;

  if (digits.length > 9) {
    formatted = digits.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2}).*/, '$1.$2.$3-$4');
  } else if (digits.length > 6) {
    formatted = digits.replace(/^(\d{3})(\d{3})(\d{1,3}).*/, '$1.$2.$3');
  } else if (digits.length > 3) {
    formatted = digits.replace(/^(\d{3})(\d{1,3}).*/, '$1.$2');
  }

  event.target.value = formatted;
  event.target.classList.remove('invalid');
});

// Remove o destaque de erro assim que o usuário corrige um campo.
form?.querySelectorAll('input').forEach((input) => {
  input.addEventListener('input', () => input.classList.remove('invalid'));
  input.addEventListener('change', () => input.classList.remove('invalid'));
});

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  message.textContent = '';
  message.classList.remove('success');

  const requiredFields = [...form.querySelectorAll('[required]')];
  let firstInvalidField = null;

  requiredFields.forEach((field) => {
    const empty = !field.value.trim();
    const cpfIncomplete = field.id === 'cpf' && field.value.replace(/\D/g, '').length !== 11;
    const invalid = empty || cpfIncomplete || !field.checkValidity();

    field.classList.toggle('invalid', invalid);
    if (invalid && !firstInvalidField) firstInvalidField = field;
  });

  if (firstInvalidField) {
    message.textContent = firstInvalidField.id === 'cpf' && firstInvalidField.value
      ? 'Digite um CPF com 11 números.'
      : 'Verifique os campos obrigatórios antes de continuar.';
    firstInvalidField.focus();
    return;
  }

  if (birthInput.value && new Date(`${birthInput.value}T00:00:00`) > new Date()) {
    birthInput.classList.add('invalid');
    message.textContent = 'A data de nascimento não pode estar no futuro.';
    birthInput.focus();
    return;
  }

  // Tudo certo: envia o formulário de verdade para o Flask (/salvar-suspeito).
  // form.submit() não dispara o evento "submit" de novo, então não há laço.
  form.submit();
});
